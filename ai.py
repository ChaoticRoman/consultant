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

USD_PER_INPUT_TOKEN = {"o1": 15e-6, "o3-mini": 1.1e-6}
USD_PER_OUTPUT_TOKEN = {"o1": 60e-6, "o3-mini": 4.4e-6}


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

    usage = response.usage
    prompt_tokens, completion_tokens = (
        usage.prompt_tokens,
        usage.completion_tokens
    )

    price = USD_PER_INPUT_TOKEN[model] * prompt_tokens
    price += USD_PER_OUTPUT_TOKEN[model] * completion_tokens

    return content, messages, price


def system_prompt(content):
    return {"role": "system", "content": content}


def log(*args):
    with open(full_path("data/ai.log"), "a") as f:
        f.write(
            str(datetime.datetime.now()) + " "
            + " ".join(str(a) for a in args) + "\n"
        )


if __name__ == "__main__":
#    print(f"{chat('Tell me all you know about Chineese Triad organization.')=}")
    print(f"{chat('Tell a joke.')=}")
#    print(f"{chat('Tell a joke.', [system_prompt('You are grim storyteller.')])=}")
