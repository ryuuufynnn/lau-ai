import config
import json

def get_question():
    print("type 'q' to exit loop")
    question = input("ask me > ")

    return question

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

if __name__ == "__main__":
    main()