import configparser
import json
import requests
from pathlib import Path

config = configparser.ConfigParser()
config.read(f"{Path.home()}/.amp/profiles")

if len(config.sections()) == 0:
    raise Exception(
        "Please set BLOCKSTREAM_AMP_USERNAME and BLOCKSTREAM_AMP_PASSWORD in your file ~/.amp/profiles"
    )

profile = config["default"]
API_URL = profile.get("API_URL", "https://amp.blockstream.com/api")


def setProfile(profile_name):
    if profile_name not in config:
        raise Exception(f"Profile {profile_name} not found in ~/.amp/profiles")
    global profile
    profile = config[profile_name]


def getUrl(endpoint):
    return f"{API_URL}/{endpoint}"


def getAuthenticationHeaders(
    username=None, password=None, extra_headers={"content-type": "application/json"}
):
    if username is None:
        username = profile.get("BLOCKSTREAM_AMP_USERNAME")
    if password is None:
        password = profile.get("BLOCKSTREAM_AMP_PASSWORD")

    assert (
        username is not None and password is not None
    ), "Please set BLOCKSTREAM_AMP_USERNAME and BLOCKSTREAM_AMP_PASSWORD in your file ~/.amp/settings.ini"

    url = getUrl(f"user/obtain_token")
    headers = {"content-type": "application/json"}
    payload = {"username": username, "password": password}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    assert response.status_code == 200
    json_data = json.loads(response.text)
    token = json_data["token"]
    headers = {
        "Authorization": f"token {token}",
        **extra_headers,
    }
    return headers


def extractTokenFromHeaders(headers):
    return headers["Authorization"].split(" ")[1]
