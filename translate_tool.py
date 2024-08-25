import time
from string import Template
import httpx
from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyperclip
import argparse

controller = Controller()

def get_arguments():
    parser = argparse.ArgumentParser(description="Translate text using a specified model and language.")
    parser.add_argument("--target_language", type=str, default="Chinese", help="The target language for translation.")
    # parser.add_argument("--model_name", type=str, default="llama3.1:latest", help="The name of the model to use.")
    parser.add_argument("--model_name", type=str, default="wizardlm2:latest", help="The name of the model to use.")
    parser.add_argument("--keep_original", action='store_true', help="Option to keep the original text in the output.")

    return parser.parse_args()

def fix_text(text, target_language, model_name, keep_original):
    if keep_original:
        not_ = ""
    else:
        not_ = "not"
        
        
    prompt_template = Template(
        f"""Translate the selected text into {target_language}, do {not_} include a preamble and any other text.
        
    $text

    Return only the corrected text, don't include a preamble.
    """
        )
    OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"

    prompt = prompt_template.substitute(text=text)
    response = httpx.post(
        OLLAMA_ENDPOINT,
        json={"prompt": prompt, "model": model_name, "keep_alive": "10m", "stream": False},
        headers={"Content-Type": "application/json"},
        timeout=100,
    )
    if response.status_code != 200:
        print("Error", response.status_code)
        return None
    return response.json()["response"].strip()


def fix_current_line(target_language, model_name, keep_original):
    # macOS shortcut to select the current line: Cmd+Shift+Left
    controller.press(Key.cmd)
    controller.press(Key.shift)
    controller.press(Key.left)

    controller.release(Key.cmd)
    controller.release(Key.shift)
    controller.release(Key.left)

    fix_selection(target_language, model_name, keep_original)


def fix_selection(target_language, model_name, keep_original):
    # 1. Copy selection to clipboard
    with controller.pressed(Key.cmd):
        controller.tap("c")

    # 2. Get the clipboard string
    time.sleep(0.1)
    text = pyperclip.paste()

    # 3. Fix string
    if not text:
        return
    fixed_text = fix_text(text, target_language, model_name, keep_original)
    if not fixed_text:
        return

    # 4. Paste the fixed string to the clipboard
    pyperclip.copy(fixed_text)
    time.sleep(0.1)

    # 5. Paste the clipboard and replace the selected text
    with controller.pressed(Key.cmd):
        controller.tap("v")


def on_f9(target_language, model_name, keep_original):
    fix_current_line(target_language, model_name, keep_original)
    print('f9 pressed')


def on_f10(target_language, model_name, keep_original):
    fix_selection(target_language, model_name, keep_original)
    print('f10 pressed')


def main():
    args = get_arguments()

    with keyboard.GlobalHotKeys({
        "<f9>": lambda: on_f9(args.target_language, args.model_name, args.keep_original),
        "<f10>": lambda: on_f10(args.target_language, args.model_name, args.keep_original)
    }) as h:
        h.join()


if __name__ == "__main__":
    main()
