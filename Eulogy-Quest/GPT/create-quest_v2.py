#!/usr/bin/env python3

import os
import sys
import subprocess

# ----------------------
# Input Arguments
# ----------------------
if len(sys.argv) < 2:
    print("Usage: create-quest_v2.py \"First Last\" [zone]")
    sys.exit(1)

honored_target = sys.argv[1].strip()
zone = sys.argv[2] if len(sys.argv) > 2 else "tutorialb"

# Convert name to underscored format
first_last = honored_target.replace(" ", "_")
build_dir = os.path.join("Eulogies", first_last, "build", "quest")
os.makedirs(build_dir, exist_ok=True)


# ----------------------
# Helper: Run script with args
# ----------------------
def run_script(script_name, args):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    prompts_dir = os.path.join(script_dir, "prompts")
    full_path = os.path.join(prompts_dir, script_name)
    subprocess.run(["python3", full_path] + args, check=True)

# ----------------------
# Step 1: Generate Ghost dialog
# ----------------------
print("[1] Generating ghost dialog via ghost-prompt-raw_v2.py...")
raw_dialog_filename = f"Ghost-dialog-{first_last}-raw.txt"
raw_dialog_path = os.path.join(build_dir, raw_dialog_filename)

run_script("ghost-prompt-raw_v2.py", [honored_target, raw_dialog_path])

# ----------------------
# Step 1.5: Write honored_target.txt
# ----------------------
honored_file_path = os.path.join(build_dir, "honored_target.txt")
with open(honored_file_path, "w", encoding="utf-8") as f:
    f.write(honored_target + "\n")

# ----------------------
# Step 2: Get delivery target info
# ----------------------
print("[2] Generating delivery target via get-delivery-target_v2.py...")
#target_output_path = os.path.join(build_dir, f"{first_last}-delivery-target.txt")
run_script("get-delivery-target_v2.py", [honored_target, raw_dialog_path, build_dir])

# ----------------------
# Step 3: Get delivery item info
# ----------------------
print("[3] Generating delivery item via get-delivery-item_v2.py...")
#item_output_path = os.path.join(build_dir, f"{first_last}-delivery-item.txt")
run_script("get-delivery-item_v2.py", [honored_target, raw_dialog_path, build_dir])

# ----------------------
# Step 4: Update SQL NPC entries (Ghost only)
# ----------------------
print("[4] Updating NPC database via updateNPCs_v2.py...")
run_script("updateNPCs_v2.py", [honored_target, zone])

# ----------------------
# Step 5: Generate Perl scripts for Ghost NPC
# ----------------------
print("[5] Generating Perl script via perl-script-NPCs_v2.py...")
run_script("perl-script-NPCs_v2.py", [honored_target, raw_dialog_path])

print("\nQuest generation complete.")
