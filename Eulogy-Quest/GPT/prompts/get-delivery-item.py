#!/usr/bin/env python3
#
# still pass honored_target's name in a "string"
# now pass the Ghost-dialog-<Firstname_Lastname>-raw.txt
# to this script, asking for the name and descriptors for the item
#
#!/usr/bin/env python3

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

# ----- Handle honored_target name and story filename -----

if len(sys.argv) < 3:
    print("Usage: python get-delivery-item.py <honored_target_name> <story_file_name>")
    sys.exit(1)

honored_target_name = sys.argv[1]
story_file_name = sys.argv[2]

print(f"Using honored_target: {honored_target_name}")
print(f"Using story file: {story_file_name}")

# Read the story text from the specified file
story_file_path = os.path.abspath(story_file_name)

if not os.path.exists(story_file_path):
    print(f"Error: Story file '{story_file_name}' not found.")
    sys.exit(1)

with open(story_file_path, 'r', encoding='utf-8') as file:
    story_text = file.read()

# ----- Prompt Template -----

prompt_template = f"""
Here is a story:

--- STORY START ---
{story_text}
--- STORY END ---

Identify:
1. The name of the item in dire need of delivery as told in the story.
Give this item a fitting name which matches the item in the story.
This item should have a two or three word name, sufficient to differentiate it from other similar items.
The item can reference its use, intent, or intended recipient.
Good names include 'Valley Forge missive', 'Note to Nathanael', and 'Promise of supplies'.
Be specific. Avoid general or mystical names.

2. Five one-word adjectives which might believeably apply to this item.
These adjectives should help in locating similar items.
Good adjectives describe physical attributes such as size, color, age, condition, and so forth.

Output:
Only output 6 lines.
For the first line:
only the name of the item.
For the last 5 lines, only output its adjectives, one adjective per line.
"""

final_prompt = prompt_template.strip()

# ----- Create dynamic output filename -----

safe_name = honored_target_name.replace(" ", "_").replace("\"", "").replace("'", "")
base_filename = f"{safe_name}-delivery-item.txt"
output_dir = os.getcwd()
output_filename = os.path.join(output_dir, base_filename)

counter = 1
while os.path.exists(output_filename):
    output_filename = os.path.join(output_dir, f"{safe_name}-delivery-item_{counter}.txt")
    counter += 1

# ----- Send prompt to GPT and save -----

try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a master Everquest quest designer."},
            {"role": "user", "content": final_prompt}
        ],
        temperature=0.7
    )

    ghost_delivery_item = response.choices[0].message.content.strip()

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(ghost_delivery_item)

    print(f"Response written to {output_filename}")

except OpenAIError as e:
    print(f"OpenAI API Error: {e}")
    sys.exit(1)
