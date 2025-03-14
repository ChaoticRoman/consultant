import os

import requests

from utils import full_path
from smartsplit import split_text_into_chunks

URL = "https://graph.facebook.com/v21.0/566964093168050/messages"

with open(full_path(".token")) as f:
    token = f.read().strip()

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}


def send(number="420736452265", message="Hello, user!", debug=False):
    chunks = split_text_into_chunks(message, max_length=4096)
    for chunk in chunks:
        send_single(number, chunk, debug)


def send_single(number="420736452265", message="Hello, user!", debug=False):
    if len(message) > 4096:
        raise ValueError("Too long message to send by WhatsApp.")
    payload = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "text",
        "text": {
            "body": message
        }
    }
    response = requests.post(URL, headers=headers, json=payload)

    if debug or not response.ok:
        print("Status code:", response.status_code)
        print("Response body:", response.text)


if __name__ == "__main__":
    send(debug=True)
