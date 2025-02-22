import os

import requests

URL = "https://graph.facebook.com/v21.0/566964093168050/messages"

abspath = os.path.abspath(__file__)
script_dir = os.path.dirname(abspath)

with open(os.path.join(script_dir, ".token")) as f:
    token = f.read().strip()

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}


def send(number="420736452265", message="Hello, user!", debug=False):
    payload = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "text",
        "text": {
            "body": message
        }
    }
    response = requests.post(URL, headers=headers, json=payload)
    if debug:
        print("Status code:", response.status_code)
        print("Response body:", response.text)


if __name__ == "__main__":
    send(debug=True)
