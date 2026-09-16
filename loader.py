import threading
import sys
import time

def show_loader(stop_event):
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    i = 0

    while not stop_event.is_set():
        print(f"\r{BLUE}lau-ai > {CYAN}{spinner[i]}{RESET}", end="", flush=True)

        i = (i + 1) % len(spinner)
        time.sleep(0.5)

    print("\r\033[K", end="", flush=True)
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()
    # sys.stdout.write("\r          \r")
    # sys.stdout.flush()

