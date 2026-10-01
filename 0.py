from dotenv import load_dotenv
load_dotenv()
from anthropic import Anthropic

client = Anthropic()
model = "claude-sonnet-5-5"

print("hi")

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, content):
    assistant_message = {"role": "assistant", "content": content}
    messages.append(assistant_message)

def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=16000,
        messages=messages,
    )
    print("IN<<\n"+str(message)+"\n>>\n")
    return message

def text_of(message):
    return next((b.text for b in message.content if b.type == "text"), "")

messages = []
add_user_message(messages, "Define quantum computing in one sentence")
response = chat(messages)
print(text_of(response))
add_assistant_message(messages, response.content)  # keep thinking blocks
add_user_message(messages, "Write another sentence")
final = chat(messages)

print(text_of(final))
