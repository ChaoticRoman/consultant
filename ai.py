import os
import datetime

import openai

from utils import full_path

DEBUG_LOG = True

abspath = os.path.abspath(__file__)
script_dir = os.path.dirname(abspath)

with open(full_path(".openai_key")) as f:
    os.environ["OPENAI_API_KEY"] = f.read().strip()

client = openai.OpenAI()


def chat(prompt, history=None, model="o3-mini"):
    messages = history if history else []
    messages.append({"role": "user", "content": prompt.strip()})

    if DEBUG_LOG:
        log("Sending to OpenAI:", messages)

    response = client.chat.completions.create(
        model=model, messages=messages
    )

    message = response.choices[0].message
    content = message.content.strip()

    messages.append({"role": "assistant", "content": content})

    if DEBUG_LOG:
        log("Got from OpenAI:", content)

    return content, messages


def system_prompt(content):
    return {"role": "system", "content": content}


def log(*args):
    with open(full_path("data/ai.log"), "a") as f:
        f.write(
            str(datetime.datetime.now()) + " "
            + " ".join(str(a) for a in args) + "\n"
        )


if __name__ == "__main__":
    print(f"{chat('Tell a joke.')=}")
    print(f"{chat('Tell a joke.', [system_prompt('You are grim storyteller.')])=}")
