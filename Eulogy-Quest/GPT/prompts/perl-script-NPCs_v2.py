#!/usr/bin/env python3
#
# GPT/prompts/perl-script-NPCs_v2.py
#
# ai-gen start (Chat-GPT 4o-mini-high, ?)
# ?= much re-prompting; final result copy/pasted
#
import os
import sys
import re
import shutil
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 perl-script-NPCs.py <honored_target>")
        return

    honored_target = sys.argv[1].strip()
    parts = honored_target.split()
    if len(parts) != 2:
        print("Error: honored_target must consist of two words (first and last name)")
        return

    first_name, last_name = parts

    gpt_root = Path(__file__).resolve().parent.parent
    safe_name = honored_target.replace(" ", "_")
    quest_dir = gpt_root / "Eulogies" / safe_name / "build" / "quest"

    perl_dir = quest_dir.parent / "perl"
    perl_dir.mkdir(parents=True, exist_ok=True)

    # Start with honored_target.txt
    honored_path = quest_dir / "honored_target.txt"
    if not honored_path.exists():
        print(f"Error: Could not find honored_target.txt at {honored_path}")
        return

    npc_names = []
    honored_npc_name = honored_path.read_text(encoding="utf-8").strip().replace(" ", "_")
    npc_names.append(honored_npc_name)

    # Gather other npc_target files
    for file in quest_dir.glob("npc*_target.txt"):
        name = file.read_text(encoding="utf-8").strip()
        if name:
            npc_names.append(name.replace(" ", "_"))

    # NOTE: Once quest_dialogue.json is implemented (a structured version of ghost_task),
    # this should be updated to load from that file instead of ghost_task.txt.

    safe_name = honored_target.replace(" ", "_")
    task_path = quest_dir / f"Ghost-dialog-{safe_name}-raw.txt"

    if not task_path.exists():
        print(f"Error: Could not find ghost_task.txt at {task_path}")
        return

    quest_text_dump = task_path.read_text(encoding="utf-8").strip()

    # NOTE: The generated Perl files should eventually be copied to either:
    #   1. the appropriate zone directory in akk-stack/server/quests/ (for world-wide placement), or
    #   2. the tutorialb zone directory (for localized testing).
    # This behavior should be controlled by a second argument to this script,
    # which we'll implement once world-wide NPC placement is supported.

# Go from prompts/ → GPT/ → Eulogy-Quest/ → akk-stack/

    akk_stack_root = Path(__file__).resolve().parents[3]
    tutorialb_dir = akk_stack_root / "server" / "quests" / "tutorialb"
    tutorialb_dir.mkdir(parents=True, exist_ok=True)

    for index, npc in enumerate(npc_names):

        #try to find quest text for this npc (npc1_task.txt, npc2_task.txt, etc)
        file_name = f"npc{index}_task.txt" if index != 0 else f"Ghost-dialog-{safe_name}-raw.txt"

        npc_task_path = quest_dir / file_name

        if npc_task_path.exists():
            quest_text = npc_task_path.read_text(encoding="utf-8").strip()
            print(f"Using specific quest text for {npc}. file: {file_name}")
        else:
            quest_text = quest_text_dump
            print(f"No custom quest text found for {npc}. Using default quest text.")

        output_path = perl_dir / f"{npc}.pl"
        perl_script = f"""
sub EVENT_SAY {{
  if ($text=~/hail/i) {{
      quest::say(\"{quest_text}\");
  }}
}}
"""
        output_path.write_text(perl_script.strip() + "\n", encoding="utf-8")
        print(f"Generated: {output_path}")

        # Copy to tutorialb
        dest_path = tutorialb_dir / f"{npc}.pl"
        shutil.copy(output_path, dest_path)
        print(f"Copied to: {dest_path}")


if __name__ == "__main__":
    main()

# ai-gen end