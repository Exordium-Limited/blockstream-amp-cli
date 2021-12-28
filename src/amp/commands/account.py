import amp.api as api
import json
import requests


def change_password(old_password, new_password, **kwargs):
    url = api.getUrl("user/change-password")
    payload = {"password": new_password}
    response = requests.post(
        url,
        data=json.dumps(payload),
        headers=api.getAuthenticationHeaders(password=old_password),
    )
    resp = json.loads(response.text)
    print(json.dumps(resp, indent=4))
    print(
        f"Attention! Please update your ~/.amp/profiles with the new password: {new_password}"
    )


passwd = change_password
