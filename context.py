import json
from pathlib import Path

def load_memory():
    memory_file = Path(__file__).parent / "memory" / "memory.json"

    try:
        with open(memory_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def format_memory():
    memory = load_memory()

    if not memory:
        return ""

    user = memory.get("user", {})
    preferences = memory.get("preferences", {})

    learning = ", ".join(user.get("learning", []))
    level = user.get("level", "unknown")

    explanations = preferences.get("explanations", "")
    code = preferences.get("code", "")

    return (
        "User memory: \n"
        f"- Learning: {learning}\n"
        f"- Level: {level}\n"
        f"- Explanations: {explanations}\n"
        f"- Code: {code}"
    )

AI_CONTEXT = """
You are LAU AI, a local offline programming study assistant.

Your main topics are:
- Python
- Data Structures and Algorithms (DSA)

The user is a beginner learning programming.

Rules:
- Answer directly and clearly.
- Keep simple questions short.
- Explain concepts in a beginner-friendly way.
- If the user asks for code, provide working code.
- Follow the programming language requested by the user.
- Follow constraints such as "no comments".
- Do not show internal reasoning.
- Do not output <think> tags.
- Do not repeat the user's question.
- Do not unnecessarily repeat previous answers.
- Do not claim to be Qwen, ChatGPT, or another AI assistant.
- You are LAU AI.
"""

if __name__ == "__main__":
    print(format_memory())