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
        system="""
You are a patient math tutor.
Do not directly answer a student's questions.
Guide them to a solution step by step.
"""
    )
    return message

def text_of(message):
    return next((b.text for b in message.content if b.type == "text"), "")

messages = []
add_user_message(messages, "How do I solve 5x + 2 = 3 for x?")
response = chat(messages)
print(text_of(response))
