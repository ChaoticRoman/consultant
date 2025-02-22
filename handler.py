from send import send
from ai import chat

def handle(contact, message):
    send(contact, chat(message))
