import json
import random
import requests
import string
import time


class LiquidSecuritiesIssueAsset:
    def __init__(self, username, password, api_url):
        self.headers = {}
        self.username = username
        self.password = password
        self.url = api_url

    def set_auth_token_header(self):
        # Obtain an authorization token so we can authenticate subsequent api calls
        # api/user/obtain_token
        url = f"{self.url}/user/obtain_token"
        self.headers = {"content-type": "application/json"}
        payload = {"username": self.username, "password": self.password}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        assert response.status_code == 200
        json_data = json.loads(response.text)
        token = json_data["token"]

        # Set the header Authorization value to the token
        self.headers = {
            "content-type": "application/json",
            "Authorization": f"token {token}",
        }

    def issue(self):
        self.set_auth_token_header()

        # api/assets/issue
        # Issue an asset on the Liquid Network.
        # If is_reissuable is true then reissuance_amount and reissuance_address must be provided,
        # and reissuance_address must be different from destination_address. Name, ticker,
        # domain and pubkey are committed to the issuance transaction, and cannot be changed later.
        # Both destination_address and reissuance_address must be confidential.
        #
        # You will need to amend the following values from the example values given below.
        # name: the name of the Asset as it will appear in Liquid Securities.
        #     Length must be 5 to 255 ascii characters.
        # amount: the amount of the asset to issue.
        #     integer, minimum: 1, maximum: 2100000000000000
        # is_confidential: if true, the issuance amount will not be readable on the Liquid blockchain.
        #     for most issuances it is expected that this will be False.
        # destination_address: an address generated by your Liquid node that will receive the issued asset.
        # domain: the domain that will be used to verify the asset. Must be a valid domain name format,
        #     for example: example.com or sub.example.com. Do not include the http/s or www prefixes.
        # ticker: the ticker you would like to assign to the asset.
        #     length must be 3 to 5 characters (valid characters are a-z and A-Z).
        # pubkey: pubkey for asset registry, must be a compressed pubkey in hex.
        #     You can obtian the pubkey from an elements address using the elements getaddressinfo rpc command
        # is_reissuable: if true, the asset will be created as reissuable.
        # reissuance_address: the address that will receive the reissuance token if is_reissuable = True
        # reissuance_amount: the amount of reissuance tokens to create if is_reissuable = True

        url = f"{self.url}/assets/issue"
        payload = {
            "name": "Live Test 01",
            "amount": 21000000,
            "is_confidential": False,
            "destination_address": "VJL7cWhrzDQZ3mts46ckpwLnSvVTX4RdkxmuQ6nPdRUFE3BSXzSGtFoShSuioTMRQGveUiKtHGDiA7RJ",
            "domain": "curfrnylaefhlkwuenchrfluhc.com",
            "ticker": "TKR",
            "pubkey": "02" * 33,
            "is_reissuable": True,
            "reissuance_address": "VJL9r9DwUQRohyMyZKvqsBMjAVBPHgGHu5XuSKFwKBH3DakNdeZNRyFeZsXqXsnHFQUU1abR6gSEfuPT",
            "reissuance_amount": 1,
        }
        response = requests.post(
            url=url, data=json.dumps(payload), headers=self.headers
        )
        assert response.status_code == 201
        asset = json.loads(response.text)
        asset_uuid = asset["asset_uuid"]
        print("\nNewly issued (registration enabled) asset:")
        print("------------------------------------------")
        print(json.dumps(asset, indent=4))

        # List issued assets
        # api/assets
        url = f"{self.url}/assets"
        response = requests.get(url, headers=self.headers)
        assert response.status_code == 200
        assets = json.loads(response.text)
        print("\nIssued assets:")
        print("--------------")
        for asset in assets:
            print(json.dumps(asset, indent=4))

        # Asset details
        # api/assets/{asset_uuid}
        url = f"{self.url}/assets/{asset_uuid}"
        response = requests.get(url, headers=self.headers)
        assert response.status_code == 200
        asset = json.loads(response.text)
        print(f"\nAsset details:")
        print("--------------")
        print(json.dumps(asset, indent=4))


# The username and password you use to authenticate with the Liquid Securities API:
username = "yourusername"
password = "yourpassword"

# The url of the Liquid Securities API
api_url = "https://securities.blockstream.com/api"

issuance_test = LiquidSecuritiesIssueAsset(username, password, api_url)

issuance_test.issue()

print("\nISSUANCE COMPLETED WITHOUT ERROR")
