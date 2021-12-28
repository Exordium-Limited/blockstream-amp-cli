import amp.api as api
import json
import requests


def list(**kwargs):
    # Category list
    url = api.getUrl("categories")
    response = requests.get(url, headers=api.getAuthenticationHeaders())
    assert response.status_code == 200
    categories = json.loads(response.text)
    print("\nCategories list:")
    print("----------------")
    for category in categories:
        print(json.dumps(category, indent=4))


ls = list


def create(category_name, category_description, **kwargs):
    # Category add
    url = api.getUrl("categories/add")
    payload = {"name": category_name, "description": category_description}
    response = requests.post(
        url, data=json.dumps(payload), headers=api.getAuthenticationHeaders()
    )
    assert response.status_code == 201
    category = json.loads(response.text)
    category_id = int(category["id"])
    print("\nNew category:")
    print("-------------")
    print(json.dumps(category, indent=4))


def register(category_id, user_id, **kwargs):
    # Registered user category - add registered user to category
    url = api.getUrl(f"categories/{category_id}/registered_users/{user_id}/add")
    response = requests.put(url, headers=api.getAuthenticationHeaders())
    print(response.text)
    assert response.status_code == 200
    res = json.loads(response.text)
    print(f"\nResponse: {res}")


def unregister(category_id, user_id, **kwargs):
    # Registered user category - add registered user to category
    url = api.getUrl(f"categories/{category_id}/registered_users/{user_id}/remove")
    response = requests.put(url, headers=api.getAuthenticationHeaders())
    assert response.status_code == 200
    res = json.loads(response.text)
    print(f"\nResponse: {res}")


def associate(category_id, asset_uuid, **kwargs):
    # Add the Category to the Asset as a requirement
    url = api.getUrl(f"categories/{category_id}/assets/{asset_uuid}/add")
    response = requests.put(url=url, headers=api.getAuthenticationHeaders())
    asset = json.loads(response.text)
    print("\nAsset Requirements (Categories ids):")
    print("------------------------------------")
    print(json.dumps(asset, indent=4))
