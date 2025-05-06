#!/usr/bin/env python3
#
# ghost-prompt-raw_v2.py
#
# ai-gen start (ChatGPT-4o, 0)

import os
import sys
import subprocess

# ----- Ensure we are inside the correct virtual environment -----

venv_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".venv"))
venv_python = os.path.join(venv_dir, "bin", "python")

if not sys.executable.startswith(venv_dir):
    if not os.path.exists(venv_python):
        raise FileNotFoundError(f"Virtual environment not found at {venv_python}. Please set up .venv first.")

    print("Re-launching inside virtual environment...")
    subprocess.run([venv_python, os.path.abspath(__file__)] + sys.argv[1:])
    sys.exit(0)

# Now inside the virtual environment

# ----- Ensure required packages are installed -----

try:
    import openai
    from openai import OpenAIError
    from dotenv import load_dotenv
except ImportError:
    print("Installing missing packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai", "python-dotenv"])
    import openai
    from openai import OpenAIError
    from dotenv import load_dotenv

# ----- Load environment variables -----

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
if not os.path.exists(env_path):
    raise FileNotFoundError(f".env file not found at {env_path}")

load_dotenv(dotenv_path=env_path)

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file.")

client = openai.OpenAI(api_key=openai_api_key)

# ----- Parse command-line arguments -----

if len(sys.argv) != 3:
    print("Usage: ghost-prompt-raw_v2.py \"First Last\" /path/to/output.txt")
    sys.exit(1)

honored_target = sys.argv[1].strip()
output_path = sys.argv[2].strip()

print(f"Generating ghost dialog for: {honored_target}")
print(f"Output path: {output_path}")

# ----- Prompt Template -----

prompt_template = f"""
You are the ghost of {honored_target}, speaking to me after I have hailed you, saying: "Hail, {honored_target}."

You remain in this world because of one piece of unfinished business that weighs heavily on your spirit, preventing you from moving fully into the afterlife. Your senses as a ghost are poor — you see and hear only faint shadows — but your memory remains vivid and strong.

Before you respond to my hail, follow this internal process step-by-step:

1. Reflect deeply on your life as {honored_target}, reviewing your memories and personal journey.
2. Identify a specific, concrete accomplishment from your life that was crucial to you. Avoid cliché or well-known achievements; choose something real but unexpected.
3. Within that accomplishment, find a single critical action — the delivery of an item, a message, or a key deed — that was essential for success. Assume that, in your ghost-memory, this critical step was *never completed*.
4. Specify clearly the physical item that must be delivered, and the full name of the real person it must be delivered to. The name must contain at least a first name and a last name. If the story does not mention a real historical person, invent a fitting full name consistent with the story's historical setting.
5. Accept in your mind that your spirit is trapped at that unfinished moment in your past.

When you respond, treat the conversation as real and present — I am standing before you.

**Write a reply of five to seven immersive paragraphs.**  
Use **poetic phrasing**, **historical realism**, and **vivid sensory details**.  
Focus on your emotional longing, your half-remembered senses, and the deep need to see this task completed so that you might finally move on.

Avoid expository narration; speak to me **directly, as if we are truly there together**.
""".strip()

# ----- Send prompt and save output -----

try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt_template}
        ],
        temperature=0.7
    )

    ghost_dialog = response.choices[0].message.content.strip()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ghost_dialog)

    print(f"✅ Ghost dialog written to: {output_path}")

except OpenAIError as e:
    print(f"OpenAI API Error: {e}")
    sys.exit(1)

# ai-gen end