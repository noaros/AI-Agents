from dotenv import load_dotenv
load_dotenv()
from anthropic import Anthropic
import json

client = Anthropic()
model = "claude-sonnet-5-5"
print("hi")

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages, system=None, stop_sequences=[], output_schema=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
    }
    if system:
        params["system"] = system
    if stop_sequences:
        params["stop_sequences"] = stop_sequences
    if output_schema:
        params["output_config"] = {
            "format": {"type": "json_schema", "schema": output_schema}
        }
    
    response = client.messages.create(**params)
    return next(block.text for block in response.content if block.type == "text")

def generate_dataset():
    prompt = """
Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts that generate Python, JSON, or Regex specifically for AWS-related tasks. Each task should require Python, JSON, or a Regex to complete.

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single regex
* Focus on tasks that do not require writing much code

Please generate 3 objects.
"""

    schema = {
        "type": "object",
        "properties": {
            "tasks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {"task": {"type": "string"}},
                    "required": ["task"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["tasks"],
        "additionalProperties": False,
    }

    messages = []
    add_user_message(messages, prompt)
    text = chat(messages, output_schema=schema)
    return json.loads(text)["tasks"]

dataset = generate_dataset()
print(dataset)
with open('dataset.json', 'w') as f:
    json.dump(dataset, f, indent=2)