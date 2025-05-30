#!/usr/bin/env python3
import os
import json
import hmac
import hashlib
from typing import Annotated

from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse, HTMLResponse
import uvicorn

from models import WebhookBody
from handler import handle, status
from utils import full_path, now2str
from send import confirm_read

app = FastAPI(docs_url=None, redoc_url=None)

with open(full_path(".app_secret")) as f:
    app_secret = f.read().strip()


def dump(data):
    if type(data) == str:
        data = json.loads(data)
    if type(data) is dict:
        return json.dumps(data, indent=4)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware to log details of every incoming request.
    Prints path, method, query parameters, headers, and body.
    """
    body = await request.body()

    print("--------------------------------------------------")
    print(f"UTC: {now2str()}")
    print(f"Path: {request.url.path}")
    print(f"Method: {request.method}")
    print(f"Query Params: {request.query_params}")
    # Printing headers as a dict-like object
    print(f"Headers: {dump(dict(request.headers))}")
    # Attempt to decode body from bytes to string
    if body:
        print(f"Body: {dump(body.decode('utf-8'))}")
    else:
        print("Body: (empty)")
    print("--------------------------------------------------")

    # Continue processing the request
    response = await call_next(request)
    return response


def verify_webhook(data, hmac_header):
    hmac_recieved = str(hmac_header).removeprefix('sha256=')
    digest = hmac.new(app_secret.encode('utf-8'), data, hashlib.sha256).hexdigest()
    return hmac.compare_digest(hmac_recieved, digest)


@app.middleware("http")
async def auth_requests(request: Request, call_next):
    body = await request.body()

    if request.url.path != "/":
        if not verify_webhook(body, dict(request.headers).get('x-hub-signature-256')):
            return JSONResponse(None, 401, {"WWW-Authenticate": "Basic"})

    response = await call_next(request)
    return response


@app.get("/webhook")
def webhook_get(hub_challenge: Annotated[int |None, Query(alias="hub.challenge")]):
    if hub_challenge:
        return hub_challenge


@app.post("/webhook")
def webhook_post(data: WebhookBody):
    if data.is_message():  # Handle incoming message
        confirm_read(data.message_id())
        handle(data.sender(), data.text())
    else:  # We are not handling sent, delivered, and read now
        return None


@app.get("/")
def status_get():
    return HTMLResponse(f'<html><body>{status().replace("\n", "<br />\n")}</body></hmtl>')


if __name__ == "__main__":
    uvicorn.run(app, uds=full_path("uvicorn.sock"))
