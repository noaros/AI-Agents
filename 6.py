from dotenv import load_dotenv
load_dotenv()
from anthropic import Anthropic, beta_tool
import os

client = Anthropic()
model = "claude-sonnet-5-5"

# Same agent as 5.py, but the SDK's tool runner owns the loop.
# @beta_tool turns each function into a tool: the schema comes from the
# type hints, the descriptions come from the docstring.

@beta_tool
def list_files(path: str = ".") -> str:
    """List the files in a directory.

    Args:
        path: Directory path, defaults to '.'
    """
    return "\n".join(sorted(os.listdir(path)))

@beta_tool
def read_file(path: str) -> str:
    """Read the full text contents of a file.

    Args:
        path: Path to the file.
    """
    with open(path) as f:
        return f.read()

runner = client.beta.messages.tool_runner(
    model=model,
    max_tokens=16000,
    system="You are a helpful agent. Use your tools to investigate before answering.",
    tools=[list_files, read_file],
    messages=[{"role": "user", "content": "Which .py file in the current directory is the longest, and what does it do? Answer in two sentences."}],
    max_iterations=10,
)

# Each pass is one model response; the runner calls the tools between passes
for turn, message in enumerate(runner):
    for block in message.content:
        if block.type == "tool_use":
            print(f"[turn {turn}] {block.name}({block.input})")

# The last message yielded is the final answer
if message.stop_reason != "end_turn":
    print(f"[stopped: {message.stop_reason}]")
print(next((b.text for b in message.content if b.type == "text"), ""))
