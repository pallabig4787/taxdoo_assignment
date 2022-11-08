import requests
import json


def test_api_taxdoo_post():
    access_token = 'd6fbf0f04c6f4deeeaaa39e3001d37fdc6590451ace65a0e2e094830f0ae6ab0'
    headers = {
        "authorization": f"Bearer {access_token}"
    }
    data = {"id": 3790, "name": "Api automate", "email": "palg@kmailcom", "gender": "female", "status": "active"}
    resp = requests.post(url="https://gorest.co.in/public/v2/users", data=data, headers=headers)
    data = resp.json()
    assert (resp.status_code == 201), "Status code is not 201. Rather found : ” + str(resp.status_code)"


def test_api_taxdoo_get():
    resp = requests.get("https://gorest.co.in/public/v2/posts")
    assert (resp.status_code == 200), "Status code is not 200. Rather found : " + str(resp.status_code)
