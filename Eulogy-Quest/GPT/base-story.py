# ai-gen start (Chat-GPT 4o-mini-high, ?)
# ?= much re-prompting; final result copy/pasted
#
# base-story.py
# ----------------
# Script: base-story
# Path: GPT/base-story.py
# Description:
#   Generates base story components (task, delivery item, delivery recipient, target location, and NPC name)
#   by querying the GPT API as the ghost of the honored_target. It scaffolds a new quest directory
#   under GPT/Eulogies/<LastName>-quest/build/quest and writes each component as text files there.
#   Finally, it cleans up generated text files by removing backticks and empty lines.

import os
import argparse
import logging
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate base story components and scaffold the quest directory for a given honored_target",
    )
    parser.add_argument(
        'honored_target',
        help='Full name of the honored target (two words, e.g. "Pope Francis")'
    )
    return parser.parse_args()


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def main():
    # Load environment
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logging.error("OPENAI_API_KEY not set. Please configure your .env or environment.")
        return

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Parse arguments
    args = parse_args()
    honored_target = args.honored_target.strip()
    parts = honored_target.split()
    if len(parts) != 2:
        logging.error("honored_target must be two words (first and last name)")
        return
    last_name = parts[1]

    # Locate and create Eulogies/<LastName>-quest/build/quest directory
    script_dir = Path(__file__).parent.resolve()  # .../GPT
    eulogies_dir = script_dir / 'Eulogies'
    quest_dir = eulogies_dir / f"{last_name}-quest"
    build_dir = quest_dir / 'build' / 'quest'
    build_dir.mkdir(parents=True, exist_ok=True)
    logging.info(f"Using quest build directory: {build_dir}")

    # Write honored_target.txt
    honored_target_path = build_dir / 'honored_target.txt'
    honored_target_path.write_text(honored_target, encoding='utf-8')
    logging.info(f"Wrote honored_target.txt: {honored_target}")

    # Construct AI prompt
    prompt = (
        f"You are the ghost of {honored_target} in the world of EverQuest. "
        "A player has initiated conversation with you. Identify six pieces of information:\n\n"
        "1. Provide 'ghost_task.txt' describing only the delivery task, its importance, "
        "the item to deliver, the recipient, and the exact EverQuest zone (valid through Planes of Power). "
        "This is internal-use only.\n\n"
        "2. Provide 'ghost_delivery_item.txt' containing only the item name.\n\n"
        "3. Provide 'ghost_delivery_target.txt' containing only the recipient's two-word name.\n\n"
        "4. Provide 'ghost_delivery_target_location.txt' containing only the zone name where the recipient is located.\n"
        "5. Provide 'ghost_dialog.txt' containing a short in-character paragraph where the ghost explains the quest to the player\n\n"
        "6. Provide 'ghost_reward.txt' containing only a reward item name (no description, only the name). The ghost doesnt know about this item.\n"
    )

    # Query GPT
    logging.info("Querying GPT for base story components...")
    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
    except Exception as e:
        logging.error(f"ChatCompletion API error: {e}")
        return
    content = response.choices[0].message.content

    # Parse response into sections
    sections = {
        'ghost_task': [],
        'ghost_delivery_item': [],
        'ghost_delivery_target': [],
        'ghost_delivery_target_location': [],
        'ghost_dialog': [],
        'ghost_reward': []
    }
    current = None
    for line in content.splitlines():
        if 'ghost_task.txt' in line:
            current = 'ghost_task'; continue
        if 'ghost_delivery_item.txt' in line:
            current = 'ghost_delivery_item'; continue
        if 'ghost_delivery_target.txt' in line and 'location' not in line:
            current = 'ghost_delivery_target'; continue
        if 'ghost_delivery_target_location.txt' in line:
            current = 'ghost_delivery_target_location'; continue
        if 'ghost_dialog.txt' in line:
            current = 'ghost_dialog'; continue
        if 'ghost_reward.txt' in line:
            current = 'ghost_reward'; continue
        if current:
            sections[current].append(line)

    # Write each file in build_dir
    filenames = {
        'ghost_task': 'ghost_task.txt',
        'ghost_delivery_item': 'ghost_delivery_item.txt',
        'ghost_delivery_target': 'ghost_delivery_target.txt',
        'ghost_delivery_target_location': 'ghost_delivery_target_location.txt',
        'ghost_dialog': 'ghost_dialog.txt',
        'ghost_reward': 'ghost_reward.txt'
    }
    for key, fname in filenames.items():
        file_path = build_dir / fname
        text = '\n'.join(sections[key]).strip()
        file_path.write_text(text, encoding='utf-8')
        logging.info(f"Wrote {fname}: {text!r}")

    # Copy ghost_delivery_target.txt to npc1_target.txt
    target_file = build_dir / 'ghost_delivery_target.txt'
    if target_file.exists():
        npc_name = target_file.read_text(encoding='utf-8').strip()
        npc1_file = build_dir / 'npc1_target.txt'
        npc1_file.write_text(npc_name, encoding='utf-8')
        logging.info(f"Wrote npc1_target.txt: {npc_name!r}")

    # Cleanup generated text files: remove backticks and empty lines
    for txt_file in build_dir.glob('*.txt'):
        content = txt_file.read_text(encoding='utf-8')
        # Remove all backtick characters
        content = content.replace('`', '')
        # Remove empty lines
        lines = [line for line in content.splitlines() if line.strip()]
        txt_file.write_text("\n".join(lines) + "\n", encoding='utf-8')
        logging.info(f"Cleaned formatting in {txt_file}")

    logging.info("base-story generation complete.")

if __name__ == '__main__':
    setup_logging()
    main()

# ai-gen end