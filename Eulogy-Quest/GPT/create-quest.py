# ai-gen start (Chat-GPT 4o-mini-high, ?)
# ?= much re-prompting; final result copy/pasted
#
#!/usr/bin/env python3
# create-quest.py
# ----------------
# Master script to orchestrate the creation of a quest:
# 1. Runs base-story.py
# 2. Runs updateNPCs.py
# 3. Runs perl-script-NPCs.py
#
# Located at: GPT/create-quest.py
# Usage: python3 create-quest.py <honored_target> [zone]
#   honored_target: two-word name (e.g. "Pope Francis")
#   zone: 'tutorialb' (default) or 'world-wide' (not yet implemented)

import sys
import subprocess
from pathlib import Path


def main():
    # Parse arguments
    if len(sys.argv) < 2:
        print("Usage: python3 create-quest.py <honored_target> [zone]")
        sys.exit(1)

    honored_target = sys.argv[1].strip()
    parts = honored_target.split()
    if len(parts) != 2:
        print("Error: honored_target must be two words (first and last name)")
        sys.exit(1)

    zone = sys.argv[2].strip() if len(sys.argv) > 2 else 'tutorialb'
    if zone not in ('tutorialb', 'world-wide'):
        print("Error: zone must be 'tutorialb' or 'world-wide'")
        sys.exit(1)

    first_name, last_name = parts
    quest_name = f"{last_name}-quest"

    # Locate script directory
    script_dir = Path(__file__).parent.resolve()  # .../GPT

    # Paths to sub-scripts
    base_story = script_dir / 'base-story.py'
    update_npcs = script_dir / 'updateNPCs.py'
    perl_script = script_dir / 'perl-script-NPCs.py'

    # Command prefix to ensure venv is active
    activate = "source ../.venv/bin/activate"

    # 1. Run base-story.py with honored_target
    cmd1 = f"{activate} && python3 {base_story} '{honored_target}'"
    print(f"Running: {cmd1}")
    subprocess.run(['bash', '-c', cmd1], check=True)

    # 2. Run updateNPCs.py with quest_name
    cmd2 = f"{activate} && python3 {update_npcs} '{quest_name}'"
    print(f"Running: {cmd2}")
    subprocess.run(['bash', '-c', cmd2], check=True)

    # 3. Run perl-script-NPCs.py with honored_target and zone
    cmd3 = f"{activate} && python3 {perl_script} '{honored_target}' '{zone}'"
    print(f"Running: {cmd3}")
    subprocess.run(['bash', '-c', cmd3], check=True)

    print("Quest creation pipeline complete.")


if __name__ == '__main__':
    main()

# ai-gen end