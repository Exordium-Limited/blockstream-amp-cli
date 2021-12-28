import amp.api as api
import json
import requests


def list(asset_uuid, **kwargs):
    # Asset distribution list
    # The assignments for the asset. Expect this to be empty unless you have
    # already created assignments.
    url = api.getUrl(f"assets/{asset_uuid}/distributions")
    response = requests.get(url, headers=api.getAuthenticationHeaders())
    print(json.loads(response.text))
    assert response.status_code == 200
    assignments = json.loads(response.text)
    print("\nAsset dsitributions:")
    print("------------------")
    for assignment in assignments:
        print(json.dumps(assignment, indent=4))


ls = list


def details(asset_uuid, distribution_id, **kwargs):
    # Get distribution info
    # The assignments for the asset. Expect this to be empty unless you have
    # already created assignments.
    url = api.getUrl(f"assets/{asset_uuid}/distributions/{distribution_id}")
    response = requests.get(url, headers=api.getAuthenticationHeaders())
    print(json.loads(response.text))
    assert response.status_code == 200
    assignments = json.loads(response.text)
    print("\Distribution:")
    print("------------------")
    for assignment in assignments:
        print(json.dumps(assignment, indent=4))


def prepare(asset_uuid, **kwargs):
    # Request the data needed to carry out a distribution.
    # Returns json data that should be saved to file. The path to the file should be passed as an
    # argument to a Python client that carries out the distribution itself. The client will be
    # supplied to users of the api and will handle the distribution transactions and post back
    # the resulting transaction data to the distributions/confirm endpoint after it has
    # sufficient confirmations.
    # NOTE: The url intentionally ends with a '/'
    url = api.getUrl(f"assets/{asset_uuid}/distributions/create/")
    response = requests.get(url, headers=api.getAuthenticationHeaders())
    assert response.status_code == 200
    distribution_data = json.loads(response.text)
    # The json data in distribution_data would then be saved to a file for use in the Python client
    # that carries out the distribution itself.
    print(json.dumps(distribution_data, indent=4))


def cancel(asset_uuid, distribution_id, **kwargs):
    # Distribution cancel
    url = api.getUrl(f"assets/{asset_uuid}/distributions/{distribution_id}/cancel")
    response = requests.delete(url, headers=api.getAuthenticationHeaders())
    assert response.status_code == 200
    assignment = json.loads(response.text)
    print("\Cancellation details:")
    print("-------------------")
    print(json.dumps(assignment, indent=4))
