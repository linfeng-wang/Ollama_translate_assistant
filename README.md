# AI-Powered Translation Assistant with Ollama

This script functions as a background translator, listening for hotkeys and using a Large Language Model (LLM) to translate selected text. Inspired by the AI_typing_assistant project by patrickloeber (https://github.com/patrickloeber/ai-typing-assistant)


## Quick Start

### 1. Install Ollama

First, install Ollama: https://github.com/ollama/ollama

Run `ollama run wizardlm2`

can try to install other models as well 
Run `ollama run mistral:7b-instruct-v0.2-q4_K_S`

The Mistal 7B Instruct model is well-suited for this task, but feel free to experiment with others!

### 2. Install Required Libraries 
python version 3.8.19

```bash
pip install pynput pyperclip httpx
```

Or install the environment using ymal file
```bash
conda env create -f environment.yml --name myenv
conda activate myenv
```

Running the script
```bash
python translate_tool.py --target_language <full name of a language> 

```

Language can be specified under the option: `--target_language` (Default: French)

Model can be specified under the option: `--model_name` (Default: wizardlm2:latest)

Whether to keep under the original under the option: `--keep_original` (Default: False)



Keep the terminal running in the background and use F9 on lines and use F10 on selected texts


The tool is currently optimised for Mac.
