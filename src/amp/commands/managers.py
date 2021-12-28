import amp.api as api
import json
import requests


def associate(manager_id, asset_uuid, **kwargs):
    # Associate the Investment Manager with an asset
    url = api.getUrl(f"managers/{manager_id}/assets/{asset_uuid}/add")
    response = requests.put(url, headers=api.getAuthenticationHeaders())
    resp = json.loads(response.text)
    print(json.dumps(resp, indent=4))


def create(username, password):
    # Create the Investment Manager user
    # Note: only 1 is allowed per Issuer at the present time
    url = api.getUrl("managers/create")
    payload = {"username": username, "password": password}
    response = requests.post(
        url=url, data=json.dumps(payload), headers=api.getAuthenticationHeaders()
    )
    resp = json.loads(response.text)
    print(json.dumps(resp, indent=4))

    manager_id = resp["id"]

    # Unlock the IM user (is created as locked by default)
    url = api.getUrl(f"managers/{manager_id}/unlock")
    response = requests.put(url, headers=api.getAuthenticationHeaders())
    resp = json.loads(response.text)
    print("Newly created manager (Issuer view:)")
    print(json.dumps(resp, indent=4))

    # Check the manager was created and unlocked
    url = api.getUrl("managers")
    response = requests.get(url, headers=api.getAuthenticationHeaders())
    resp = json.loads(response.text)
    print(json.dumps(resp, indent=4))

    # Now get the Investment Manager's API Token for them to use
    headers_manager = api.getAuthenticatedHeaders(username=username, password=password)

    # Check that the IM account works
    url = api.getUrl("managers/me")
    response = requests.get(url, headers=headers_manager)
    resp = json.loads(response.text)
    print("Newly created manager (Manager view:)")
    print(json.dumps(resp, indent=4))

    token = api.extractTokenFromHeaders(headers_manager)

    print(
        f"\nThe Investment Manager user was created.\nThey should use this API Token to access Liquid Securities:\n{token}"
    )
