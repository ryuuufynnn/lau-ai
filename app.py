import config
import json
import urllib.request
import urllib.error


def get_question():
    print("type 'q' to exit loop")
    question = input("ask me > ")

    return question


def ask_ai(question):
    url = "http://127.0.0.1:8080/v1/completions"

    prompt = f"""You are LAU AI, a simple and concise programming study assistant.

Focus mainly on Python and Data Structures and Algorithms (DSA).

Rules:
- Give direct answers.
- Keep basic answers short and easy to understand.
- Do not show your thinking or reasoning.
- Do not repeat sentences.
- If the user asks for code, provide working code.
- Follow the user's requested programming language.
- If the user asks for no comments, do not add comments.

User question:
{question}

LAU AI answer:"""

    data = {
        "prompt": prompt,
        "temperature": 0.2,
        "max_tokens": 150
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request) as response:
            result = json.loads(response.read().decode("utf-8"))

        return result["choices"][0]["text"].strip()

    except urllib.error.URLError as error:
        return f"Could not connect to AI server: {error}"
    
def save_history(question):
    history = load_history()
    history.append(
        {"question": question}
    )

    with open(config.HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def load_history():
    try:
        with open(config.HISTORY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def show_history():
    history = load_history()

    if not history:
        print("lau-ai > no history yet.")
        return

    print("\nHistory: ")

    number = 1

    for item in history:
        print(f"{number}. {item['question']}")
        number += 1


def main():
    while True:
        question = get_question()

        if question.lower() == "q":
            break

        if question.strip() == "/h":
            show_history()
            continue

        save_history(question)

        answer = ask_ai(question)

        print(f"\nlau-ai > {answer}\n")


if __name__ == "__main__":
    main()