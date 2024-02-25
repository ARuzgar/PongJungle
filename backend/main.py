#!/usr/bin/env python3

import time
import requests
import json

UID = "u-s4t2ud-272a7d972a922c63919b4411aff1da6abf64ec93eb38804b51427a0c0fbf86ea"
SECRET = "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"
REDIRECT_URI = "http://10.11.29.3:8000"


def get_access_token(code):
    url = "https://api.intra.42.fr/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": UID,
        "client_secret": SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve access token: {e}")
        return None


def get_user_info(access_token):
    url = "https://api.intra.42.fr/v2/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve user information: {e}")
        return None



if __name__ == "__main__":
    authorization_code = "31605671aa8de3ad62ba443e8284407e28687d6682b86c7fbc7ce62b3641a55e"
    access_token = get_access_token(authorization_code)

    if access_token:
        print(f"Access Token: {access_token}")
        user_info = get_user_info(access_token)

        if user_info:
            print("User Information:")
            print(json.dumps(user_info, indent=2))
        else:
            print("Failed to retrieve user information.")
    else:
        print("Failed to obtain access token.")