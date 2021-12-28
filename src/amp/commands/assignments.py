import amp.api as api
import json
import requests


def list(asset_uuid, **kwargs):
    # Asset assignments list
    # The assignments for the asset. Expect this to be empty unless you have
    # already created assignments.
    url = api.getUrl(f"assets/{asset_uuid}/assignments")

    if "all" in kwargs and kwargs["all"]:
        pass
    elif "distributed" in kwargs and kwargs["distributed"]:
        url = f"{url}?distributed=true"
    else:
        url = f"{url}?distributed=false"

    response = requests.get(url, headers=api.getAuthenticationHeaders())
    print(json.loads(response.text))
    assert response.status_code == 200
    assignments = json.loads(response.text)
    print("\nAsset assignments:")
    print("------------------")
    for assignment in assignments:
        print(json.dumps(assignment, indent=4))


ls = list


def create(asset_uuid, user_id, amount, **kwargs):
    url = api.getUrl(f"assets/{asset_uuid}/assignments/create")
    payload = {
        "assignments": [
            {
                "registered_user": int(user_id),
                "amount": int(amount),
                "ready_for_distribution": True,
            }
        ]
    }
    response = requests.post(
        url=url, data=json.dumps(payload), headers=api.getAuthenticationHeaders()
    )
    print(json.loads(response.text))
    assert response.status_code == 200
    assignment = json.loads(response.text)
    assignment_id = assignment[0]["id"]
    print("\nAsset Assignment:")
    print("-----------------")
    print(json.dumps(assignment, indent=4))


def details(asset_uuid, assignment_id, **kwargs):
    # Assignment details
    url = api.getUrl(f"assets/{asset_uuid}/assignments/{assignment_id}")
    response = requests.get(url, headers=api.getAuthenticationHeaders())
    print(json.loads(response.text))
    assert response.status_code == 200
    assignment = json.loads(response.text)
    print("\nAssignment details:")
    print("-------------------")
    print(json.dumps(assignment, indent=4))


def remove(asset_uuid, assignment_id, **kwargs):
    # Assignment delete
    url = api.getUrl(f"assets/{asset_uuid}/assignments/{assignment_id}/delete")
    response = requests.delete(url, headers=api.getAuthenticationHeaders())
    assert response.status_code == 204
    assignment = json.loads(response.text)
    print("\Deletion details:")
    print("-------------------")
    print(json.dumps(assignment, indent=4))


rm = remove
