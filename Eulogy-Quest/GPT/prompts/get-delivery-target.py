#!/usr/bin/env python3
#
# still pass honored_target's name in a "string"
# now pass the Ghost-dialog-<Firstname_Lastname>-raw.txt
# to this script, asking for the name of the delivery recipient
# and the relevant pertinent data.
#

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
    print("Usage: python get-delivery-target.py <honored_target_name> <story_file_name>")
    sys.exit(1)

honored_target_name = sys.argv[1]
story_file_name = sys.argv[2]

print(f"Using honored_target: {honored_target_name}")
print(f"Using story file: {story_file_name}")

story_file_path = os.path.abspath(story_file_name)

if not os.path.exists(story_file_path):
    print(f"Error: Story file '{story_file_name}' not found.")
    sys.exit(1)

with open(story_file_path, 'r', encoding='utf-8') as file:
    story_text = file.read()

# ----- Load zone whitelist dynamically -----
# place the whitelist in the same directory as this file

zone_whitelist_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "zone_whitelist.txt"))

if not os.path.exists(zone_whitelist_path):
    print(f"Error: zone_whitelist.txt not found at {zone_whitelist_path}")
    sys.exit(1)

with open(zone_whitelist_path, 'r', encoding='utf-8') as f:
    zone_whitelist_content = f.read().strip()

print(f"Loaded {zone_whitelist_content.count(',') + 1} zones from whitelist.")


# ----- New Prompt Template -----

prompt_template = f"""
Here is a story:

--- STORY START ---
{story_text}
--- STORY END ---

Identify the following:

1. The full name of the intended recipient who must receive the item mentioned in the story. Use a real historical figure if mentioned; otherwise, invent a fitting name consistent with the story's historical setting.

2. A plausible in-game EverQuest zone where this recipient could be found. 
Choose ONLY from the following list of valid EverQuest zones:
{zone_whitelist_content}
These zones existed by the "Planes of Power" expansion, including original EverQuest, Ruins of Kunark, Scars of Velious, or Shadows of Luclin expansions. Ensure the zone fits the thematic setting and activities of the recipient.

3. A specific, immersive location description within that zone, such as "by the waterfall," "inside the temple ruins," or "at the merchant stands near the city gates." This should make sense geographically within the chosen EverQuest zone.

4. Leave one blank line for clarity.

5. Write a one-paragraph explanation describing why the recipient is at this location. What circumstances have brought them here? What are they doing? Be historically plausible and immersive.

Output only the five elements above, formatted cleanly in order.
"""

final_prompt = prompt_template.strip()


# ----- Output file naming -----

safe_name = honored_target_name.replace(" ", "_").replace("\"", "").replace("'", "")
base_filename = f"{safe_name}-delivery-target.txt"
output_dir = os.getcwd()
output_filename = os.path.join(output_dir, base_filename)

counter = 1
while os.path.exists(output_filename):
    output_filename = os.path.join(output_dir, f"{safe_name}-delivery-target_{counter}.txt")
    counter += 1

# ----- Send prompt to GPT and save -----

try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a master EverQuest quest designer specializing in lore-friendly and geographically plausible character placement."},
            {"role": "user", "content": final_prompt}
        ],
        temperature=0.7
    )

    ghost_delivery_target = response.choices[0].message.content.strip()

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(ghost_delivery_target)

    print(f"Response written to {output_filename}")

except OpenAIError as e:
    print(f"OpenAI API Error: {e}")
    sys.exit(1)
