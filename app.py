import config
import json
import urllib.request
import urllib.error
import textwrap
import re
import subprocess
import time
import os

from context import AI_CONTEXT, load_memory, format_memory

curious_penguin = "rene-mamaaa"

def get_question():
    RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, RESET = colors()

    return input(f"{YELLOW}> {RESET}")

def clean_answer(answer):
    # Remove thinking tags
    answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL)

    # Remove extra blank lines
    answer = re.sub(r"\n\s*\n+", "\n\n", answer)

    # Remove spaces at the beginning/end
    answer = answer.strip()

    return answer

def format_answer(answer):
    answer = clean_answer(answer)

    lines = answer.splitlines()
    formatted = []

    in_code = False

    for line in lines:
        stripped = line.strip()

        # Keep code blocks untouched
        if stripped.startswith("```"):
            in_code = not in_code
            formatted.append(line)
            continue

        if in_code:
            formatted.append(line)
            continue

        if not stripped:
            formatted.append("")
            continue

        # Wrap normal text so it doesn't stretch too far
        wrapped = textwrap.wrap(
            stripped,
            width=76,
            subsequent_indent="         "
        )

        formatted.extend(wrapped)

    return "\n".join(formatted).strip()

def ask_ai(question):
    url = "http://127.0.0.1:8080/v1/chat/completions"

    memory = format_memory()

    data = {
        "messages": [
            {
                "role": "system",
                "content": f"{AI_CONTEXT}\n\nUser memory: \n{memory}"
            },
            {
                "role": "user",
                "content": question
            }
        ],
        "temperature": 0.2,
        "max_tokens": 200,
        "chat_template_kwargs": {
            "enable_thinking": False
        }
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

        answer = result["choices"][0]["message"]["content"]

        return format_answer(answer)

    except urllib.error.URLError:
        return "Could not connect to LAU AI server."

    except (KeyError, json.JSONDecodeError):
        return "Invalid response from LAU AI server."

def save_history(question):
    history = load_history()

    history.append({
        "question": question
    })

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

    for item in history:
        print(f"> {item['question']}")

def colors():
    # ANSI escape codes for colors
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

    return RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, RESET

def start_ai_server():
    RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, RESET = colors()

    url = "http://127.0.0.1:8080/health"

    # Check if server is already running
    try:
        urllib.request.urlopen(url, timeout=1)
        return None
    except:
        pass

    print(f"server-status: {MAGENTA}starting{RESET}")

    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "/usr/lib"
    env.pop("LD_PRELOAD", None)

    # Remove possible library overrides
    env.pop("LD_LIBRARY_PATH", None)
    env.pop("LD_PRELOAD", None)

    server = subprocess.Popen(
        [
            "/home/laurence-linux/llama.cpp/build/bin/llama-server",
            "--model",
            "/home/laurence-linux/llama.cpp/models/Qwen3.5-0.8B-Q4_0.gguf",
            "--reasoning",
            "off"
        ],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Wait until server is ready
    for _ in range(60):
        try:
            urllib.request.urlopen(url, timeout=1)
            print(f"server-status: {GREEN}ready{RESET}")
            return server
        except:
            if server.poll() is not None:
                print(f"server-status: {RED}failed{RESET}")
                return None

            time.sleep(0.5)

    print("Could not connect to LAU AI server.")
    server.terminate()
    return None

def main():
    RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, RESET = colors()

    print("_____________________________________\n")
    print(f"{MAGENTA}lau-ai{RESET}")
    print("_____________________________________\n")

    while True:
        question = get_question()

        if question.lower() == "q":
            break

        if question.strip() == "/h":
            show_history()
            continue

        if not question.strip():
            continue

        save_history(question)

        answer = ask_ai(question)

        print(f"{BLUE}lau-ai > {CYAN}{answer}{RESET}")
        print()

if __name__ == "__main__":
    server = start_ai_server()
    main()