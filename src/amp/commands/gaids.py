import amp.api as api
import json
import requests


def validate(gaid, **kwargs):
    url = api.getUrl(f"gaids/{gaid}/validate")
    response = requests.get(url, headers=api.getAuthenticationHeaders())
    assert response.status_code == 200
    gaid_validation = json.loads(response.text)
    gaid_is_valid = gaid_validation["is_valid"]
    print(f"\nValidating GAID '{gaid}'")
    print(f"GAID is Valid: {gaid_is_valid}")
