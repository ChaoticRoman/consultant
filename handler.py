from send import send

def handle(contact, message):
    send(contact, f"You think that {message}?!")
