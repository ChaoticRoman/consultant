#!/usr/bin/env python3
import os
from typing import Annotated

from fastapi import FastAPI, Request, Query
import uvicorn

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware to log details of every incoming request.
    Prints path, method, query parameters, headers, and body.
    """
    body = await request.body()

    print("--------------------------------------------------")
    print(f"Path: {request.url.path}")
    print(f"Method: {request.method}")
    print(f"Query Params: {request.query_params}")
    # Printing headers as a dict-like object
    print(f"Headers: {dict(request.headers)}")
    # Attempt to decode body from bytes to string
    if body:
        print(f"Body: {body.decode('utf-8')}")
    else:
        print("Body: (empty)")
    print("--------------------------------------------------")

    # Continue processing the request
    response = await call_next(request)
    return response


@app.get("/webhook")
def webhook(hub_challenge: Annotated[int |None, Query(alias="hub.challenge")]):
    if hub_challenge:
        return hub_challenge
    return {"message": "Hello from FastAPI!"}


@app.post("/webhook")
def submit_data(data: dict):
    return {"received_data": data}


@app.put("/webhook")
def update_data(data: dict):
    return {"updated_data": data}


if __name__ == "__main__":
    abspath = os.path.abspath(__file__)
    os.chdir(os.path.dirname(abspath))

    uvicorn.run(app, uds="uvicorn.sock")
