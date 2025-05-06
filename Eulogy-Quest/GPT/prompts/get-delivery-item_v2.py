#!/usr/bin/env python3
#
# GPT/prompts/get-delivery-item_v2.py
#
# ai-gen start (ChatGPT-4o, 0)

import os
import sys
import subprocess

# ----- Ensure we're inside the correct venv -----
venv_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".venv"))
venv_python = os.path.join(venv_dir, "bin", "python")

if not sys.executable.startswith(venv_dir):
    print("Re-launching inside virtual environment...")
    subprocess.run([venv_python, os.path.abspath(__file__)] + sys.argv[1:])
    sys.exit(0)

try:
    import openai
    from openai import OpenAIError
    from dotenv import load_dotenv
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai", "python-dotenv"])
    import openai
    from openai import OpenAIError
    from dotenv import load_dotenv

load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env")))
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

if len(sys.argv) < 3:
    print("Usage: get-delivery-item_v2.py \"First Last\" <dialog_file_path> [output_dir]")
    sys.exit(1)

honored_target = sys.argv[1].strip()
dialog_file_path = sys.argv[2].strip()
first_last = honored_target.replace(" ", "_")

if len(sys.argv) >= 4:
    output_dir = sys.argv[3].strip()
else:
    output_dir = os.path.join("..", "Eulogies", first_last, "build", "quest")

os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, f"{first_last}-delivery-item.txt")

with open(dialog_file_path, "r", encoding="utf-8") as f:
    ghost_dialog = f.read()

prompt = f"""
You are creating a delivery item for a quest that begins with the following ghost dialogue:

---
{ghost_dialog}
---

Your task is to generate the item that must be delivered to complete this ghost's final wish. The output must include:

1. The full name of the item on line 1
2. Five one-word adjectives (lines 2–6) describing its physical characteristics (not abstract virtues)

Only output six lines total, each on its own line. No preamble, explanation, or markdown.
"""

try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    item_text = response.choices[0].message.content.strip()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(item_text + "\n")

    print(f"✅ Delivery item written to {output_file}")

except OpenAIError as e:
    print(f"OpenAI API Error: {e}")
    sys.exit(1)

# ai-gen end