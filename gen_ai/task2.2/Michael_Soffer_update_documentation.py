"""
Script: perl-script-NPCs.py

This script is part of the EulogyQuest EverQuest custom server project.
It generates `.pl` Perl quest files for NPCs based on quest dialogue files,
allowing NPCs to respond to a player's "hail" with a custom line of dialogue.

Usage:
    python3 perl-script-NPCs.py <honored_target>

Example:
    python3 perl-script-NPCs.py "Joe Greene"

Expected directory structure:
    Eulogies/
        Greene-quest/
            build/
                quest/
                    honored_target.txt
                    ghost_task.txt
                    npc1_target.txt
                    npc1_task.txt
                    ...

Generated files:
    - NPC .pl files placed in `perl/`
    - Copies of those files are moved to the `server/quests/tutorialb/` folder for EverQuest engine use
"""

import os
import sys
import re
import shutil
from pathlib import Path

def main():
    # --- Validate command-line argument ---
    if len(sys.argv) < 2:
        print("Usage: python3 perl-script-NPCs.py <honored_target>")
        return

    honored_target = sys.argv[1].strip()
    parts = honored_target.split()
    if len(parts) != 2:
        print("Error: honored_target must consist of two words (first and last name)")
        return

    first_name, last_name = parts

    # --- Set up file paths ---
    quest_dir = Path(__file__).parent / "Eulogies" / f"{last_name}-quest" / "build" / "quest"
    perl_dir = quest_dir.parent / "perl"
    perl_dir.mkdir(parents=True, exist_ok=True)

    # --- Read honored NPC name ---
    honored_path = quest_dir / "honored_target.txt"
    if not honored_path.exists():
        print(f"Error: Could not find honored_target.txt at {honored_path}")
        return

    npc_names = []
    honored_npc_name = honored_path.read_text(encoding="utf-8").strip().replace(" ", "_")
    npc_names.append(honored_npc_name)

    # --- Gather additional NPC names from npc*_target.txt files ---
    for file in quest_dir.glob("npc*_target.txt"):
        name = file.read_text(encoding="utf-8").strip()
        if name:
            npc_names.append(name.replace(" ", "_"))

    # --- Load default quest text from ghost_task.txt (to be replaced with JSON eventually) ---
    task_path = quest_dir / "ghost_task.txt"
    if not task_path.exists():
        print(f"Error: Could not find ghost_task.txt at {task_path}")
        return

    quest_text_dump = task_path.read_text(encoding="utf-8").strip()

    # --- Destination for testing: EverQuest 'tutorialb' quest folder ---
    tutorialb_dir = Path(__file__).parent.parent.parent / "server" / "quests" / "tutorialb"
    tutorialb_dir.mkdir(parents=True, exist_ok=True)

    # --- Generate and copy Perl files for each NPC ---
    for index, npc in enumerate(npc_names):
        # Try to load a specific quest dialogue for this NPC
        file_name = f"npc{index}_task.txt" if index != 0 else "ghost_task.txt"
        npc_task_path = quest_dir / file_name

        if npc_task_path.exists():
            quest_text = npc_task_path.read_text(encoding="utf-8").strip()
            print(f"Using specific quest text for {npc}. file: {file_name}")
        else:
            quest_text = quest_text_dump
            print(f"No custom quest text found for {npc}. Using default quest text.")

        # Generate Perl script content
        output_path = perl_dir / f"{npc}.pl"
        perl_script = f"""
sub EVENT_SAY {{
  if ($text=~/hail/i) {{
      quest::say("{quest_text}");
  }}
}}
"""
        # Write .pl file and copy to tutorialb zone folder
        output_path.write_text(perl_script.strip() + "\n", encoding="utf-8")
        print(f"Generated: {output_path}")

        dest_path = tutorialb_dir / f"{npc}.pl"
        shutil.copy(output_path, dest_path)
        print(f"Copied to: {dest_path}")


if __name__ == "__main__":
    main()
