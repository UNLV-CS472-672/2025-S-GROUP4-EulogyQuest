#!/usr/bin/env python3
#
# GPT/prompts/get-delivery-target_v2.py
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
    print("Usage: get-delivery-target_v2.py \"First Last\" <dialog_file_path> [output_dir]")
    sys.exit(1)

honored_target = sys.argv[1].strip()
dialog_file_path = sys.argv[2].strip()
first_last = honored_target.replace(" ", "_")

if len(sys.argv) >= 4:
    output_dir = sys.argv[3].strip()
else:
    output_dir = os.path.join("..", "Eulogies", first_last, "build", "quest")

os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, f"{first_last}-delivery-target.txt")

with open(dialog_file_path, "r", encoding="utf-8") as f:
    ghost_dialog = f.read()

prompt = f"""
You are creating the delivery target for a quest that begins with the following ghost dialogue:

---
{ghost_dialog}
---

Please output exactly five lines:
1. The full name of the recipient (must be a real or realistic person)
2. The EverQuest zone name (lowercase, e.g., 'tutorialb')
3. A one-sentence immersive description of the zone location
4. (Leave this line blank)
5. A paragraph explaining why the person is at that location — this will help build that NPC's dialogue later.

No commentary, no explanation — only the five lines.
"""

try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    target_text = response.choices[0].message.content.strip()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(target_text + "\n")

    print(f"✅ Delivery target written to {output_file}")

except OpenAIError as e:
    print(f"OpenAI API Error: {e}")
    sys.exit(1)

# ai-gen end