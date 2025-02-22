import os

import openai

abspath = os.path.abspath(__file__)
script_dir = os.path.dirname(abspath)

with open(os.path.join(script_dir, ".openai_key")) as f:
    os.environ["OPENAI_API_KEY"] = f.read().strip()

client = openai.OpenAI()


def chat(prompt, history=None, model="o3-mini"):
    messages = history if history else []
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model, messages=messages
    )

    message = response.choices[0].message
    content = message.content.strip()

    return content


if __name__ == "__main__":
    print(f"{chat('Tell a joke.')=}")
