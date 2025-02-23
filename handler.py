import shutil
import subprocess

from send import send
from ai import chat, system_prompt
from utils import full_path

ROMAN = "420736452265"
users = []


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
        handle_user(contact, message.removeprefix('/user'))
    else:
        send(contact, chat(message))


def handle_user(contact, message):
    history = build_system_prompt(contact)  # + TODO previous messages as well
    send(contact, chat(message, history=history))
    # TODO save converstation etc.


def build_system_prompt(contact):  # TODO Going to be personalized
    return system_prompt(
        "You are over-the-top tough, saracastic, ironic but helpful and motivating assistant."
    )


def status():
        total, used, free = shutil.disk_usage("/")

        data_size = subprocess.check_output(
            ['du','-sh', full_path("data")]).split()[0].decode('utf-8')

        return f"UP, {free // (2**30)} GiB free, data/ size {data_size}"
