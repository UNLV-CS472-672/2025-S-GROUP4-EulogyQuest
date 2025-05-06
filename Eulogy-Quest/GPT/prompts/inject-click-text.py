#!/usr/bin/env python3

import os
import sys

def inject_clicktext(dialog_path, target_path):
    # Read the raw ghost dialogue
    with open(dialog_path, 'r', encoding='utf-8') as f:
        dialogue = f.read()

    # Read the delivery item's name from the <Name>-delivery-item.txt file
    with open(target_path, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        keywords = [first_line.split()[0].lower()] if first_line else []

    # Apply click-text formatting
    for keyword in keywords:
        if keyword in dialogue:
            dialogue = dialogue.replace(keyword, f"[{keyword}]")

    # Output filename
    base, ext = os.path.splitext(dialog_path)
    output_file = f"{base}-clicktext{ext}"

    # Save result
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(dialogue)

    print(f"[✓] Click-text injected. Output saved to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 inject-click-text.py <Ghost-dialog-(Name)-raw.txt> <(Name)-delivery-target.txt>")
        sys.exit(1)

    inject_clicktext(sys.argv[1], sys.argv[2])
