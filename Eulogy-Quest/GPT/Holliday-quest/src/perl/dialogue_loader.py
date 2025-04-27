# ai-gen start (ChatGPT-4o, ?)
# ?= much prompt-engineering

import json
import sys
import re
import string

npc_dialogues = []

def sanitize_filename(name):
    first_name = re.sub(r"[^a-zA-Z0-9]", "", name.split()[0])
    return first_name.capitalize() + ".pl"

def strip_brackets_from_keys(dialogue_dict):
    return {
        key[1:-1] if key.startswith('[') and key.endswith(']') else key: value
        for key, value in dialogue_dict.items()
    }

def load_quest_file(json_path):
    global npc_dialogues
    with open(json_path, 'r') as f:
        data = json.load(f)
    npc_scripting = data.get('npc_scripting', [])
    npc_dialogues.clear()
    for npc in npc_scripting:
        clean_dialogue = strip_brackets_from_keys(npc.get('dialogue', {}))
        npc_dialogues.append(clean_dialogue)
    return npc_scripting

def convert_click_text(text):
    if text.startswith("[") and text.endswith("]"):
        inner_text = text[1:-1]
        normalized = re.sub(r"[\u2012\u2013\u2014\u2015\u2212]", "-", inner_text)
        allowed = string.ascii_letters + string.digits + " '-"
        cleaned_text = ''.join(c for c in normalized if c in allowed)
        return f'[" . quest::saylink("{cleaned_text}") . "]'
    return text

def apply_click_conversion_to_dialogue(value):
    return re.sub(r"\[.*?\]", lambda m: convert_click_text(m.group(0)), value)

def create_hailblock(hail_text):
    sayline = apply_click_conversion_to_dialogue(hail_text)
    escaped_sayline = sayline.replace('"', '\"')
    return f'    if ($text=~/hail/i) {{ quest::say("Greetings $name! {escaped_sayline}"); }}'

def create_event_say_blocks(dialogue_dict, is_first_npc):
    keys = list(dialogue_dict.keys())
    blocks = []

    if is_first_npc:
        parting_text = dialogue_dict.get("parting-text", "")
        processed_parting = apply_click_conversion_to_dialogue(parting_text).replace('"', '\"')
        filtered_keys = [k for k in keys if k not in ("parting-text", "offer")]

        for i, key in enumerate(filtered_keys):
            response = apply_click_conversion_to_dialogue(dialogue_dict[key])
            escaped_response = response.replace('"', '\"')
            pattern = key.replace('"', '\"')

            block = f'    if ($text=~/{pattern}/i) {{ quest::say("{escaped_response}");'
            if i == len(filtered_keys) - 1:
                block += f' quest::say("{processed_parting}");'
            block += " }"
            blocks.append(block)

    else:
        event_say_keys = keys[:-3]
        for i, key in enumerate(event_say_keys):
            if key.lower() == "hail":
                # Only keep the 'Greetings $name!' format
                hailblock = create_hailblock(dialogue_dict[key])
                blocks.append(hailblock)
            else:
                response = apply_click_conversion_to_dialogue(dialogue_dict[key])
                escaped_response = response.replace('"', '\"')
                pattern = key.replace('"', '\"')
                blocks.append(f'    if ($text=~/{pattern}/i) {{ quest::say("{escaped_response}"); }}')

    return blocks

def create_event_item_block(dialogue_dict, is_first_npc):
    lines = []
    if is_first_npc:
        offer_text = dialogue_dict.get("offer", "")
        escaped_offer = offer_text.replace('"', '\"')
        lines.append(f'    quest::say("{escaped_offer}");')
    else:
        keys = list(dialogue_dict.keys())
        last_three = keys[-3:]
        for key in last_three:
            val = dialogue_dict[key].replace('"', '\"')
            lines.append(f'    quest::say("{val}");')
    return lines

def create_perl_file(npc_name, say_lines, item_lines):
    filename = sanitize_filename(npc_name)
    with open(filename, "w") as f:
        f.write("sub EVENT_SAY {\n")
        for line in say_lines:
            f.write(f"{line}\n")
        f.write("}\n\n")
        f.write("sub EVENT_ITEM {\n")
        for line in item_lines:
            f.write(f"{line}\n")
        f.write("}\n")
    print(f"Perl file created: {filename}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python dialogue_loader.py <json_path>")
        return

    json_path = sys.argv[1]
    npcs = load_quest_file(json_path)

    for idx, npc in enumerate(npcs):
        name = npc.get("name", f"Npc{idx}")
        dialogue = npc_dialogues[idx]
        is_first = (idx == 0)

        say_lines = create_event_say_blocks(dialogue, is_first)
        item_lines = create_event_item_block(dialogue, is_first)

        create_perl_file(name, say_lines, item_lines)

if __name__ == "__main__":
    main()

# ai-gen end
