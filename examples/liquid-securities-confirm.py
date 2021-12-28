#!/usr/bin/env pyhton3

import argparse
import json
import logging
import re
import requests
import time
import sys


MIN_SUPPORTED_ELEMENTS_VERSION = 170001  # 0.17.0.1
CLIENT_SCRIPT_VERSION = 2  # 0.0.2
COMMANDS = ["reissue", "distribute", "burn"]


# adapted from https://github.com/Blockstream/liquid_multisig_issuance
class RPCHost(object):
    def __init__(self, url):
        self.session = requests.Session()
        if re.match(r".*\.onion/*.*", url):
            self.session.proxies = {
                "http": "socks5h://localhost:9050",
                "https": "socks5h://localhost:9050",
            }
        self.url = url

    def call(self, rpc_method, *params):
        payload = json.dumps(
            {"method": rpc_method, "params": list(params), "jsonrpc": "2.0"}
        )
        connected = False
        max_tries = 5
        for tries in range(max_tries):
            try:
                response = self.session.post(
                    self.url, headers={"content-type": "application/json"}, data=payload
                )
                connected = True
                break
            except requests.exceptions.ConnectionError:
                time.sleep(10)

        if not connected:
            raise Exception("Failed to connect for remote procedure call.")

        if not response.status_code in (200, 500):
            raise Exception(
                f"RPC connection failure: {response.status_code} {response.reason}"
            )

        response_json = response.json()
        if "error" in response_json and response_json["error"]:
            raise Exception(f'Error in RPC call: {response_json["error"]}')
        return response_json["result"]


def get_auth_headers(base_url, username, password):
    logging.debug("Obtaining token")
    url = base_url.format("user/obtain_token")
    headers = {"content-type": "application/json"}
    payload = {"username": username, "password": password}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    assert response.status_code == 200
    token = json.loads(response.text).get("token")
    return {"content-type": "application/json", "Authorization": f"token {token}"}


def wait_for_confirmation(rpc, txid):
    # wait for 2 confirmations
    logging.warning(
        f"Transaction sent, waiting for transaction {txid} to be confirmed (expected 2 minutes)"
    )
    step_sec = 15
    max_sec = 10 * 60  # FIXME: this may need to be increased
    for i in range(max_sec // step_sec):
        time.sleep(step_sec)
        if rpc.call("gettransaction", txid).get("confirmations", 0) > 1:
            return True
    logging.error(f"Transaction {txid} was not confirmed after {max_sec // 60} minutes")
    return False


def check_version(rpc):
    # TODO: log both to CLI (args.verbose) and to file (DEBUG)
    logging.debug(f"Script version: {CLIENT_SCRIPT_VERSION:06}")

    node_version = rpc.call("getnetworkinfo").get("version", 0)
    if node_version < MIN_SUPPORTED_ELEMENTS_VERSION:
        logging.error(
            f"Node version ({node_version:06}) not supported (min: {MIN_SUPPORTED_ELEMENTS_VERSION:06})"
        )
        sys.exit(1)

    logging.debug(f"Connected to Elements node, version: {node_version:06}")


def check_client_script(fj):
    min_supported_client_script_version = fj.get(
        "min_supported_client_script_version", 0
    )
    if min_supported_client_script_version < CLIENT_SCRIPT_VERSION:
        logging.error(
            f"Client script version ({CLIENT_SCRIPT_VERSION:06}) not supported (min: {min_supported_client_script_version:06})"
        )
        sys.exit(1)


def check_command(fj, command):
    # Check 'command' field in the json file
    script_command = fj.get("command")
    if script_command != command:
        logging.error(
            f"You have asked to perform a {command} but you have provided the wrong type of file for this action."
        )
        sys.exit(1)


def check_lost_output(base_url, headers, asset_uuid):
    # Wait for transactions propagation
    logging.info("Wait for 60 seconds ...")
    time.sleep(60)
    # Check lost outputs
    logging.debug("Check lost outputs.")
    balance_url = base_url.format(f"assets/{asset_uuid}/balance")
    response = requests.get(balance_url, headers=headers)

    if response.status_code != 200:
        logging.error(
            f'The Liquid Securities API "balance" failed. '
            f"Transaction will not be sent."
        )
        sys.exit(1)

    if response.json()["lost_outputs"] != []:
        logging.error(
            f'The Liquid Securities API "balance" returned some lost outputs. '
            f"Transaction will not be sent."
        )
        sys.exit(1)


def check_utxos(rpc, expected_utxos, expect_all=True):
    utxos = rpc.call("listunspent")
    local_utxos = [{"txid": x["txid"], "vout": x["vout"]} for x in utxos]
    num_found_utxos = sum(x in local_utxos for x in expected_utxos)
    if num_found_utxos == 0 or (expect_all and num_found_utxos != len(expected_utxos)):
        logging.error(f"Missing UTXO")
        sys.exit(1)


def check_assignments(base_url, headers, asset_uuid, distribution_uuid):
    # Check if distribution is confirmed searching in all assignments
    logging.debug("Check for confirmed distribution.")
    assignments_url = base_url.format(f"assets/{asset_uuid}/assignments")
    response = requests.get(assignments_url, headers=headers)

    if response.status_code != 200:
        logging.error(
            f'The Liquid Securities API "assignments details" failed. '
            f"Distribution transaction will not be sent."
        )
        sys.exit(1)

    assignment_found = False
    for assignment in response.json():
        if assignment["distribution_uuid"] == distribution_uuid:
            assignment_found = True
            if assignment["is_distributed"]:
                logging.error(
                    f"This distribution has already been carried out and the transaction confirmed. "
                    f"Distribution transaction will not be sent."
                )
                sys.exit(1)

    if not assignment_found:
        logging.error(
            f'The Liquid Securities API "assignments details" did not included any assignment for the distribution uuid. '
            f"Distribution transaction will not be sent."
        )
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Make transactions with the treasury node, and then confirm them to the Liquid Securities Server."
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Be more verbose. Can be used multiple times.",
    )

    parser.add_argument(
        "-u", "--username", help="Liquid Securities API username", required=True
    )
    parser.add_argument(
        "-p", "--password", help="Liquid Securities API password", required=True
    )
    parser.add_argument(
        "-n",
        "--node-url",
        help="Elements node URL, eg http://USERNAME:PASSWORD@HOST:PORT/",
        required=True,
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True
    for action in COMMANDS:
        action_parser = subparsers.add_parser(action)
        action_parser.add_argument(
            "-f",
            "--filename",
            type=argparse.FileType("r"),
            help=f"text file containing the output of the {action} request API calls",
        )
        if action == "reissue":
            action_parser.add_argument(
                "--have-split-reissuance-token",
                action="store_true",
                help="Advanced option, use it only if requested by Liquid Securities support",
            )

    args = parser.parse_args()

    if args.verbose == 0:
        logging.root.setLevel(logging.INFO)
    elif args.verbose > 0:
        logging.root.setLevel(logging.DEBUG)

    rpc = RPCHost(args.node_url)
    check_version(rpc)

    fj = json.load(args.filename)

    logging.debug(f"Opened file {args.filename}: {json.dumps(fj)}")

    check_client_script(fj)
    check_command(fj, args.command)

    base_url = fj.get("base_url")
    asset_uuid = fj.get("asset_uuid")
    asset_id = fj.get("asset_id")

    headers = get_auth_headers(base_url, args.username, args.password)

    # The following checks are meant to mitigate the chance to run the script
    # improperly, which may lead to undesired outcomes, or eventually
    # non-recoverable states.

    check_lost_output(base_url, headers, asset_uuid)

    if args.command == "reissue":
        # reissuance specific checks
        amount = fj.get("amount")
        reissuance_utxos = fj.get("reissuance_utxos")
        check_utxos(
            rpc, reissuance_utxos, expect_all=(not args.have_split_reissuance_token)
        )

        # call the reissueasset on the node and wait for confirmation
        reissuance_output = rpc.call("reissueasset", asset_id, amount)
        found = wait_for_confirmation(rpc, reissuance_output["txid"])
        if not found:
            sys.exit(1)

        # register reissue on the Liquid Securities platform
        details = rpc.call("gettransaction", reissuance_output["txid"]).get("details")
        issuances = rpc.call("listissuances")
        listissuances = [
            issuance
            for issuance in issuances
            if issuance["txid"] == reissuance_output["txid"]
        ]

        confirm_payload = {
            "details": details,
            "reissuance_output": reissuance_output,
            "listissuances": listissuances,
        }
        # TODO: write confirm payload to a file
        logging.info(f'calling "reissue-confirm" with payload: {confirm_payload}')

        confirm_url = base_url.format(f"assets/{asset_uuid}/reissue-confirm")
        response = requests.post(
            confirm_url, data=json.dumps(confirm_payload), headers=headers
        )

        if response.status_code != 200:
            logging.error(
                f'The transaction ({reissuance_output["txid"]}) has been broadcast, but the Liquid Securities API "reissue-confirm" failed. '
                f"You will need to resend the payload again. "
                f"Do not run this script again as it will send the transaction again."
            )
            sys.exit(1)

        logging.info("Reissuance confirmed successfully")

    elif args.command == "distribute":
        # distribution specific checks
        distribution_uuid = fj.get("distribution_uuid")
        check_assignments(base_url, headers, asset_uuid, distribution_uuid)

        # call the sendmany on the node and wait for confirmation
        map_address_amount = fj.get("map_address_amount")
        map_address_asset = fj.get("map_address_asset")
        txid = rpc.call(
            "sendmany",
            "",
            map_address_amount,
            0,
            "",
            [],
            False,
            1,
            "UNSET",
            map_address_asset,
        )
        found = wait_for_confirmation(rpc, txid)
        if not found:
            sys.exit(1)

        # register distribution on the Liquid Securities platform
        details = rpc.call("gettransaction", txid).get("details")
        tx_data = {"details": details, "txid": txid}
        listunspent = rpc.call("listunspent")
        change_data = [
            u for u in listunspent if u["asset"] == asset_id and u["txid"] == txid
        ]

        confirm_payload = {"tx_data": tx_data, "change_data": change_data}
        # TODO: write confirm payload to a file
        logging.info(f'calling "distribution-confirm" with payload: {confirm_payload}')

        confirm_url = base_url.format(
            f"assets/{asset_uuid}/distributions/{distribution_uuid}/confirm"
        )
        response = requests.post(
            confirm_url, data=json.dumps(confirm_payload), headers=headers
        )

        if response.status_code != 200:
            logging.error(
                f'The transaction ({txid}) has been broadcast, but the Liquid Securities API "distribution-confirm" failed. '
                f"You will need to resend the payload again. "
                f"Do not run this script again as it will send the transaction again."
            )
            sys.exit(1)

        logging.info("Distribution confirmed successfully")

    elif args.command == "burn":
        amount = fj.get("amount")

        utxos = fj.get("utxos")
        check_utxos(rpc, utxos)

        local_amount = float(rpc.call("getbalance")[asset_id])
        if local_amount < amount:
            logging.error("local balance is lower than requested amount")
            sys.exit(1)

        txid = rpc.call("destroyamount", asset_id, amount)

        found = wait_for_confirmation(rpc, txid)
        if not found:
            sys.exit(1)

        # register distribution on the Liquid Securities platform
        tx_data = {"txid": txid}
        listunspent = rpc.call("listunspent")
        change_data = [
            u for u in listunspent if u["asset"] == asset_id and u["txid"] == txid
        ]

        confirm_payload = {"tx_data": tx_data, "change_data": change_data}

        # TODO: write confirm payload to a file
        # we will have info about burn and about new change (if exists)
        logging.info(f'calling "burn-confirm" with payload: {confirm_payload}')

        confirm_url = base_url.format(f"assets/{asset_uuid}/burn-confirm")
        response = requests.post(
            confirm_url, data=json.dumps(confirm_payload), headers=headers
        )

        if response.status_code != 200:
            logging.error(
                f'The transaction ({txid}) has been broadcast, but the Liquid Securities API "burn-confirm" failed. '
                f"You will need to resend the payload again. "
                f"Do not run this script again as it will send the transaction again."
            )
            sys.exit(1)

        logging.info("Burn confirmed successfully")

    else:
        logging.error("Unimplemented command!")


if __name__ == "__main__":
    main()
