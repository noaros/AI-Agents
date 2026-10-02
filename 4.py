from dotenv import load_dotenv
load_dotenv()
from anthropic import Anthropic
import json
import ast
import re

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
        "max_tokens": 10000,
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
                    "properties": {"task": {"type": "string"}, "format": {"type": "string"}},
                    "required": ["task", "format"],
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

def run_prompt(test_case):
    """Merges the prompt and test case input, then returns the result"""
    prompt = f"""
Please solve the following task:

{test_case["task"]}

* Respond only with Python, JSON, or a plain Regex
* Do not add any comments or commentary or explanation
"""
    messages = []
    add_user_message(messages, prompt)
    output = chat(messages)
    return output

def validate_json(text):
    try:
        json.loads(text.strip())
        return 10
    except json.JSONDecodeError:
        return 0

def validate_python(text):
    try:
        ast.parse(text.strip())
        return 10
    except SyntaxError:
        return 0

def validate_regex(text):
    try:
        re.compile(text.strip())
        return 10
    except re.error:
        return 0

def grade_syntax(output, test_case):
    format_type = test_case.get("format", "").lower()
    if format_type == "json":
        return validate_json(output)
    elif format_type == "python":
        return validate_python(output)
    elif format_type == "regex":
        return validate_regex(output)
    else:
        return 0
    
def run_test_case(test_case):
    """Calls run_prompt, then grades the result"""
    output = run_prompt(test_case)
    
    model_grade = grade_by_model(test_case, output)
    model_score = model_grade["score"]
    syntax_score = grade_syntax(output, test_case)
    score = (model_score + syntax_score) / 2

    return {
        "output": output,
        "test_case": test_case,
        "score": score
    }

def run_eval(dataset):
    """Loads the dataset and calls run_test_case with each case"""
    results = []
    
    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)
    
    return results

def grade_by_model(test_case, output):
    eval_prompt = f"""
    You are an expert code reviewer. Evaluate this AI-generated solution.
    
    Task: {test_case}
    Solution: {output}
    
    Provide your evaluation as a structured JSON object with:
    - "strengths": An array of 1-3 key strengths
    - "weaknesses": An array of 1-3 key areas for improvement  
    - "reasoning": A concise explanation of your assessment
    - "score": A number between 1-10
    """

    schema = {
        "type": "object",
        "properties": {
            "strengths": {
                "type": "array",
            },
            "weaknesses": {
                "type": "array",
            },
            "reasoning": {
                "type": "string",
            },
            "score": {
                "type": "number"
            }
        },
        "required": ["tasks"],
        "additionalProperties": False,
    }

    messages = []
    add_user_message(messages, eval_prompt)

    eval_text = chat(messages, output_schema=schema)
    print("DBG",eval_text)
    return json.loads(eval_text)



# dataset = generate_dataset()
# print(dataset)
# with open('dataset.json', 'w') as f:
#     json.dump(dataset, f, indent=2)

with open("dataset.json", "r") as f:
    dataset = json.load(f)
results = run_eval(dataset)
print(json.dumps(results, indent=2))