import amp.api as api
import json
import requests


def list(**kwargs):
    """List issued assets"""
    url = api.getUrl("assets")
    response = requests.get(url, headers=api.getAuthenticationHeaders())
    assert response.status_code == 200
    assets = json.loads(response.text)
    print("\nIssued assets:")
    print("--------------")
    for asset in assets:
        print(json.dumps(asset, indent=4))


ls = list


def edit(asset_uuid, endpoint, **kwargs):
    # Edit an asset
    from urllib.parse import urlparse

    endpoint = urlparse(endpoint)
    url = api.getUrl(f"assets/{asset_uuid}/edit")
    payload = {"issuer_authorization_endpoint": endpoint.geturl()}
    response = requests.put(
        url, data=json.dumps(payload), headers=api.getAuthenticationHeaders()
    )
    assert response.status_code == 200
    register_authorized = json.loads(response.text)
    print("\nEdited asset summary:")
    print("----------------------------")
    print(json.dumps(register_authorized, indent=4))


def authorize(asset_uuid, **kwargs):
    # Register the asset as an Authorized Asset
    # api/assets/{asset_uuid}/register-authorized
    url = api.getUrl(f"assets/{asset_uuid}/register-authorized")
    response = requests.get(url, headers=api.getAuthenticationHeaders())
    assert response.status_code == 200
    register_authorized = json.loads(response.text)
    print("\nRegister authorized summary:")
    print("----------------------------")
    print(json.dumps(register_authorized, indent=4))


def lock(asset_uuid, **kwargs):
    # Lock an asset
    # api/assets/{assetUuid}/lock
    url = api.getUrl(f"assets/{asset_uuid}/lock")
    response = requests.put(url, headers=api.getAuthenticationHeaders())
    assert response.status_code == 200
    res = json.loads(response.text)
    print(f"\nResponse: {res}")


def unlock(asset_uuid, **kwargs):
    # Unlock an asset
    # api/assets/{assetUuid}/unlock
    url = api.getUrl(f"assets/{asset_uuid}/unlock")
    response = requests.put(url, headers=api.getAuthenticationHeaders())
    assert response.status_code == 200
    res = json.loads(response.text)
    print(f"\nResponse: {res}")


def register(asset_uuid, **kwargs):
    # Register the asset as an Authorized Asset
    # api/assets/{asset_uuid}/register-authorized
    url = api.getUrl(f"assets/{asset_uuid}/register")
    response = requests.get(url, headers=api.getAuthenticationHeaders())
    print(response.text)
    assert response.status_code == 200
    register_authorized = json.loads(response.text)
    print("\nRegister asset summary:")
    print("----------------------------")
    print(json.dumps(register_authorized, indent=4))


def issue(**kwargs):
    url = api.getUrl(f"assets/issue")
    # Archive EXO Token
    # payload = {'name': 'EXO Token Europe',
    #             'amount': 9826337,
    #             'is_confidential': False,
    #             'destination_address': 'VJLAAdkHSHTWBkf6KLggSDcDo42JHWiVZhTeKyhqS9LswsTtRwx53QoC9b2UTg32VjRv7WDHZx8UM6YH',
    #             'domain': 'exordium.co',
    #             'ticker': 'EXOeu',
    #             'precision': 0,
    #             'pubkey': '030cff26f9c0d365f090e24917277e23269d7ef5d7f06dec9f09de9255b8950208',
    #             'is_reissuable': True,
    #             'reissuance_address': 'VJL8KBYBuW9PLnpNUK2pVs87pDAT2PMwnB2EvKMpJLMazwy8KaEKdjYtvPpmhjWNiBam7su3u5Qq6t8z',
    #             'reissuance_amount': 1,
    #             'transfer_restricted': True}
    # payload = {'name': 'EXO Token US',
    #             'amount': 3942222,
    #             'is_confidential': False,
    #             'destination_address': 'VJLHsGNtFuue3xfdHDjY7SAjA8CmMRCs85xJLQHbaRsMhdFxsJXsMrrFoQPMwMzoQyf4nyKSnNdynzPv',
    #             'domain': 'exordium.co',
    #             'ticker': 'EXOus',
    #             'precision': 0,
    #             'pubkey': '025d743bc53ee8b260a65ee0ce4ac7363c8ea7feda7785db1f36cfb19f49015147',
    #             'is_reissuable': True,
    #             'reissuance_address': 'VJL7nf7p54wsCfivaMJzX9dNMJFkpMKFdWGzBG8HePncupSRhkA5NNuqMGd3scdTHM37HHX1PpZuLKfp',
    #             'reissuance_amount': 1,
    #             'transfer_restricted': True}
    # response = requests.post(url=url, data=json.dumps(payload), headers=api.getAuthenticationHeaders())
    # assert response.status_code == 201
    # asset = json.loads(response.text)
    # asset_uuid = asset['asset_uuid']
    # print('\nNewly issued (registration enabled) asset:')
    # print('------------------------------------------')
    # print(json.dumps(asset, indent=4))
    print("Nothing to issue sorry")


def reissue(asset_uuid, amount, **kwargs):
    url = api.getUrl(f"assets/{asset_uuid}/reissue-request")
    payload = {"amount_to_reissue": int(amount)}
    response = requests.post(
        url, data=json.dumps(payload), headers=api.getAuthenticationHeaders()
    )
    assert response.status_code == 200
    distribution_data = json.loads(response.text)
    # The json data in distribution_data would then be saved to a file for use in the Python client
    # that carries out the distribution itself.
    print(json.dumps(distribution_data, indent=4))


def details(asset_uuid, **kwargs):
    # Asset details
    url = api.getUrl(f"assets/{asset_uuid}")
    response = requests.get(url, headers=api.getAuthenticationHeaders())
    assert response.status_code == 200
    asset = json.loads(response.text)
    print(f"\nAsset details:")
    print("--------------")
    print(json.dumps(asset, indent=4))


def treasury_list(asset_uuid, **kwargs):
    # Asset details
    # api/assets/{asset_uuid}/treasury-addresses
    url = api.getUrl(f"assets/{asset_uuid}/treasury-addresses")
    response = requests.get(url, headers=api.getAuthenticationHeaders())
    assert response.status_code == 200
    asset = json.loads(response.text)
    print(f"\nAsset Treasury Addresses:")
    print("--------------")
    print(json.dumps(asset, indent=4))


def treasury_add(asset_uuid, address, **kwargs):
    url = api.getUrl(f"assets/{asset_uuid}/treasury-addresses/add")
    payload = [address]
    response = requests.post(
        url=url, data=json.dumps(payload), headers=api.getAuthenticationHeaders()
    )
    assert response.status_code == 200
    print("\nRegistered Treasury Address:")
    print("------------------------------------------")
    print(address)
    print(response.text)


def owners(asset_uuid, **kwargs):
    # Asset Ownerships
    # api/assets/{asset_uuid}/ownerships
    url = api.getUrl(f"assets/{asset_uuid}/ownerships")
    response = requests.get(url, headers=api.getAuthenticationHeaders())
    assert response.status_code == 200
    asset = json.loads(response.text)
    print(f"\nAsset ownerships:")
    print("--------------")
    print(json.dumps(asset, indent=4))


def utxos_list(asset_uuid, **kwargs):
    # Asset UTXO
    # api/assets/{asset_uuid}/ownerships
    url = api.getUrl(f"assets/{asset_uuid}/utxos")
    response = requests.get(url, headers=api.getAuthenticationHeaders())
    assert response.status_code == 200
    asset = json.loads(response.text)
    print(f"\nAsset UTXO:")
    print("--------------")
    print(json.dumps(asset, indent=4))


utxos_ls = utxos_list


def utxos_block(asset_uuid, txid, vout, **kwargs):
    url = api.getUrl(f"assets/{asset_uuid}/utxos/blacklist")
    payload = [{"txid": txid, "vout": int(vout)}]
    response = requests.post(
        url=url, data=json.dumps(payload), headers=api.getAuthenticationHeaders()
    )
    print(response.text)
    assert response.status_code == 200
    asset = json.loads(response.text)
    print("\nBlacklisted UTXO:")
    print("------------------------------------------")
    print(json.dumps(asset, indent=4))


def remove(asset_uuid, **kwargs):
    # Remove Asset
    url = api.getUrl(f"assets/{asset_uuid}/delete")
    response = requests.delete(url, headers=api.getAuthenticationHeaders())
    assert response.status_code == 204
    asset = json.loads(response.text)
    print(f"\nAsset deleted:")
    print("--------------")
    print(json.dumps(asset, indent=4))


rm = remove
