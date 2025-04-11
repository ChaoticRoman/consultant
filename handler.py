import os
import shutil
import subprocess
import json

from send import send
from ai import chat, system_prompt
from utils import full_path, now2str
from cost import sum_recent_costs

ROMAN = "420736452265"
users = ["420739233949"]

DAYS = 30
LIMIT = 2.0

# TODO make async (make send, handle_* and chat async first)
def handle(contact, message):
    if contact == ROMAN:
        handle_admin(contact, message)
    elif contact in users:
        handle_user(contact, message)
    else:
        send(contact, "You are not registered.")


def handle_admin(contact, message):
    if message in ("/status", "/s"):
        send(contact, status())
    elif message.startswith("/user"):
        handle_user(contact, message.removeprefix('/user').strip())
    else:
        send(contact, chat(message.strip())[0])


def handle_user(contact, message):
    cost = sum_recent_costs(contact_file(contact, cost=True), DAYS)

    if cost > LIMIT:
        send(contact, "Promiň, ale překročil jsi limit.")
        return

    history = build_history(contact)
    response, messages, cost = chat(message, history=history)
    send(contact, response)
    save_user_data(contact, messages, cost)


def save_user_data(contact, messages, price):  # TODO summarization
    with open(contact_file(contact), "w") as f:
        json.dump(messages, f, indent=2)
    with open(contact_file(contact, cost=True), "a") as f:
        f.write(f"{now2str()} {price}\n")


def build_history(contact):
    path = contact_file(contact)
    if os.path.isfile(path):
        with open(path) as f:
            history = json.load(f)
    else:
        with open(full_path("../consultant-users/nvc.txt")) as f:
            history = [system_prompt(f.read())]
    return history


def contact_file(contact, cost=False):
    return full_path(f"../consultant-users/{contact}{'-cost.txt' if cost else '.json'}")


def status():
    total, used, free = shutil.disk_usage("/")
    data_size = folder_size(full_path("data"))
    user_size = folder_size(full_path("../consultant-users"))

    return f"UP\n{free // (2**30)} GiB free\ndata {data_size}\nconsultant-users {user_size}"


def folder_size(folder):
    return subprocess.check_output(
        ['du','-sh', folder]).split()[0].decode('utf-8')
