#!/usr/bin/env python3

import os
import sys
import subprocess

# ----- Ensure we are inside the correct virtual environment -----

# Define path to .venv
venv_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".venv"))
venv_python = os.path.join(venv_dir, "bin", "python")

# Relaunch inside venv if not already
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

# Load OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file.")

# Create OpenAI client
client = openai.OpenAI(api_key=openai_api_key)

# ----- Handle honored_target name -----

# Default honored_target name
default_name = "Christopher Reeve"

# Check if a name was passed as a command-line argument
if len(sys.argv) > 1:
    default_name = sys.argv[1]  # Update default_name if argument provided
    print(f"Using honored_target: {default_name}")
else:
    print(f"No honored_target passed. Using default: {default_name}")

# Set final name for prompt replacement
name = default_name

# ----- Prompt Template -----

prompt_template = (
    "Act as the ghost of honored_target. You want to move on fully to the afterlife, but you have one last piece of unfinished business which keeps you here as a ghost. Being a ghost, your senses are poor, but your memory is still strong. I have just initiated conversation with you, saying, \"Hail, honored_target\". Despite your poor senses, I seem like I could have been a family member or friend, so you share this task with me, pleading with me to complete it.\n\n"
    "Before answering me, take a step-by-step approach to creating your response to my hail.\n"
    "- First, consider your life. Review your life as honored_target.\n"
    "- Second, identify some concrete, specific accomplishment as honored_target. This is not some abstract ideal or something ethereal. This is a specific accomplishment that was highly important to you. This accomplishment should be unexpected, not what the world would consider cliche regarding you.\n"
    "- Third, pick an item from this specific accomplishment which, had it not been delivered, would have ruined this accomplishment, making it as though it never happened. Most accomplishments are the result of many sequential efforts, and if any single one of these sequential efforts are thwarted in the chronology of a great accomplishment, the end result will never happen. Pick one such effort somewhere in this great accomplishment's chain of causality.\n"
    "- Fourth, as a ghost, to your current memory, you have forgotten that this great accomplishment was actually achieved. Your memory is still at this previous point in the chain of causality! You never delivered this important item! And you know, either directly -- or by some very strong suggestion -- that this task must be done, and is keeping you from moving on to the afterlife.\n"
    "- Fifth, clearly and concretely identify the item needing delivery. Also clearly identify the person you need this item delivered to. These are not abstract items and people, this is a real item and a real person from your life.\n"
    "- Sixth, I would like your response to my hail to be about five to seven paragraphs long.\n\n"
    "Now I'd like to add some context. I want to feel as though I'm getting a chance to get to know you, the real honored_target.\n"
    "Please treat this scenario with historical accuracy. Act as though I just hailed you. Act as though you now have the chance to convey this great need to me. Respond only as though in conversation with me."
)

# Replace honored_target in the prompt
final_prompt = prompt_template.replace("honored_target", name)

# ----- Create dynamic output filename -----

# Sanitize name for safe filenames
safe_name = name.replace(" ", "_").replace("\"", "").replace("'", "")
base_filename = f"Ghost-dialog-{safe_name}.txt"
output_dir = os.getcwd()
output_filename = os.path.join(output_dir, base_filename)

# If file already exists, add _1, _2, etc.
counter = 1
while os.path.exists(output_filename):
    output_filename = os.path.join(output_dir, f"Ghost-dialog-{safe_name}_{counter}.txt")
    counter += 1

# ----- Send prompt to GPT and save -----

try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": final_prompt}
        ],
        temperature=0.7
    )

    ghost_dialog = response.choices[0].message.content.strip()

    # Save response
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(ghost_dialog)

    print(f"Response written to {output_filename}")

except OpenAIError as e:
    print(f"OpenAI API Error: {e}")
    sys.exit(1)
