from dotenv import load_dotenv
load_dotenv()
from anthropic import Anthropic
import os

client = Anthropic()
model = "claude-sonnet-5-5"

# A minimally viable agent is just three things:
#   1. a model
#   2. some tools it can call
#   3. a loop that runs the tools and feeds results back until the model is done

# --- 1. Tools: plain Python functions ---

def list_files(path="."):
    return "\n".join(sorted(os.listdir(path)))

def read_file(path):
    with open(path) as f:
        return f.read()

TOOL_FUNCTIONS = {
    "list_files": list_files,
    "read_file": read_file,
}

# --- 2. Tool descriptions: what the model sees ---

TOOLS = [
    {
        "name": "list_files",
        "description": "List the files in a directory.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "Directory path, defaults to '.'"}},
        },
    },
    {
        "name": "read_file",
        "description": "Read the full text contents of a file.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "Path to the file"}},
            "required": ["path"],
        },
    },
]

def run_tool(name, tool_input):
    try:
        return TOOL_FUNCTIONS[name](**tool_input), False
    except Exception as e:
        return f"Error: {e}", True

# --- 3. The agent loop ---

def run_agent(task, max_turns=10):
    messages = [{"role": "user", "content": task}]

    for turn in range(max_turns):
        response = client.messages.create(
            model=model,
            max_tokens=16000,
            system="You are a helpful agent. Use your tools to investigate before answering.",
            tools=TOOLS,
            messages=messages,
        )
        # Keep the whole content (thinking + text + tool_use blocks), not just the text
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            # end_turn (done), max_tokens, refusal, ... -> stop looping
            if response.stop_reason != "end_turn":
                print(f"[stopped: {response.stop_reason}]")
            return next((b.text for b in response.content if b.type == "text"), "")

        # Run every tool the model asked for; return all results in ONE user message
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"[turn {turn}] {block.name}({block.input})")
                output, is_error = run_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                    "is_error": is_error,
                })
        messages.append({"role": "user", "content": tool_results})

    return "[gave up: hit max_turns]"

print(run_agent("Which .py file in the current directory is the longest, and what does it do? Answer in two sentences."))
