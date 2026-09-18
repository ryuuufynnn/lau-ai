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

def load_knowledge():
    knowledge_dir = Path(__file__).parent / "knowledge"

    knowledge = []

    for file in knowledge_dir.glob("*.json"):
        try:
            with open(file, "r") as f:
                knowledge.append(f.read())
        except OSError:
            continue

    return "\n\n".join(knowledge)

def load_lessons():
    lessons_dir = Path(__file__).parent / "knowledge" / "lessons"

    lessons = []

    for file in lessons_dir.glob("*.md"):
        try:
            with open(file, "r") as f:
                lessons.append(f.read())
        except OSError:
            continue

    return "\n\n".join(lessons)

def find_knowledge(question):
    knowledge = load_knowledge()

    keywords = question.lower().split()

    matches = []

    for line in knowledge.splitlines():
        line_lower = line.lower()

        for keyword in keywords:
            if len(keyword) > 2 and keyword in line_lower:
                matches.append(line)
                break

    return "\n".join(matches[:10])

def detect_topic(question):
    question = question.lower()

    topics = {
        "python": [
            "python",
            "list",
            "tuple",
            "dictionary",
            "dict",
            "function",
            "loop",
            "while",
            "for loop",
            "pathlib"
        ],
        "java": [
            "java",
            "jvm",
            "class",
            "object",
            "inheritance",
            "interface",
            "generics"
        ],
        "c": [
            " c ",
            "c language",
            "c programming",
            "pointer",
            "malloc",
            "printf",
            "scanf"
        ],
        "dsa": [
            "dsa",
            "data structure",
            "algorithm",
            "array",
            "stack",
            "queue",
            "linked list",
            "bubble sort",
            "binary search"
        ],
        "programming": [
            "programming",
            "program",
            "programming language",
            "compiler",
            "code"
        ]
    }

    for topic, keywords in topics.items():
        for keyword in keywords:
            if keyword in question:
                return topic

    return None

def load_topic_knowledge(topic):
    knowledge_dir = Path(__file__).parent / "knowledge"
    knowledge_file = knowledge_dir / f"{topic}.json"

    try:
        with open(knowledge_file, "r") as file:
            return file.read()
    except OSError:
        return ""

def get_relevant_knowledge(question):
    topic = detect_topic(question)

    if not topic:
        return ""

    return load_topic_knowledge(topic)

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