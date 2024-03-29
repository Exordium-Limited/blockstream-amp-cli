import amp.api as api
import json
import requests


def list(**kwargs):
    # Registered users list
    url = api.getUrl("registered_users")
    response = requests.get(url, headers=api.getAuthenticationHeaders())
    assert response.status_code == 200
    registered_users = json.loads(response.text)
    print("\nRegistered users list:")
    print("----------------------")
    for registered_user in registered_users:
        print(json.dumps(registered_user, indent=4))


ls = list


def create(user_gaid, user_fullname, is_company, **kwargs):
    url = api.getUrl("registered_users/add")
    payload = {
        "is_company": bool(is_company),
        "name": user_fullname,
        "GAID": user_gaid,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=api.getAuthenticationHeaders()
    )
    assert response.status_code == 201
    registered_user = json.loads(response.text)
    print("\nNew Registered User (individual):")
    print("---------------------------------")
    print(json.dumps(registered_user, indent=4))


def edit(user_id, user_fullname, **kwargs):
    url = api.getUrl(f"registered_users/{user_id}/edit")
    payload = {
        "name": user_fullname,
    }
    response = requests.put(
        url, data=json.dumps(payload), headers=api.getAuthenticationHeaders()
    )
    assert response.status_code == 200
    registered_user = json.loads(response.text)
    print("\Edited Registered User (individual):")
    print("---------------------------------")
    print(json.dumps(registered_user, indent=4))


def remove(user_id, **kwargs):
    url = api.getUrl(f"registered_users/{user_id}/delete")
    response = requests.delete(url, headers=api.getAuthenticationHeaders())
    assert response.status_code == 204
    print("\Deleted Registered User (individual):")
    print("---------------------------------")
    print(response.text)


rm = remove


def gaids_list(user_id, **kwargs):
    url = api.getUrl(f"registered_users/{user_id}/gaids")
    response = requests.get(url, headers=api.getAuthenticationHeaders())
    assert response.status_code == 200
    print("\List of GAIDS of the User:")
    print("---------------------------------")
    print(response.text)


gaids_ls = gaids_list


def gaids_add(user_id, gaid, **kwargs):
    url = api.getUrl(f"registered_users/{user_id}/gaids/add")
    response = requests.post(
        url, data=json.dumps(gaid), headers=api.getAuthenticationHeaders()
    )
    assert response.status_code == 200
    print("\GAID added successfully")


def gaids_setdefault(user_id, gaid, **kwargs):
    url = api.getUrl(f"registered_users/{user_id}/gaids/set-default")
    response = requests.post(
        url, data=json.dumps(gaid), headers=api.getAuthenticationHeaders()
    )
    assert response.status_code == 200
    print("\GAID set as default successfully")
