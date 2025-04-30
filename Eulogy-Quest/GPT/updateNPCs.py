# ai-gen start (Chat-GPT 4o-mini-high, ?)
# ?= much re-prompting; final result copy/pasted
#
# Script to insert NPCs and items into the database based on quest build files.

import os
import sys
import logging
import subprocess
from dotenv import load_dotenv
from collections import Counter

# Load environment variables
load_dotenv("../../.env")
load_dotenv("../.env")

DB_USER = "root"
DB_PASS = os.getenv("MARIADB_ROOT_PASSWORD")
DB_NAME = os.getenv("MARIADB_DATABASE")

RESERVED_IDS = list(range(1999900, 1999905))
RESERVED_ITEM_IDS = list(range(200000, 200020))

HARDCODED_LOCATIONS = [
    (-72.26, -192.6, 15.09),
    (-62.77, -193.64, 16.17),
    (-51.89, -183.39, 14.4),
    (-41.97, -178.06, 13.36),
    (-72.72, -195.64, 34.2),
]

QUEST_ZONE = "tutorialb"

DEFAULT_ITEM_ID = 52690 # Jeweled Box

STATIC_ITEM_PARAMS = {
    # Identity and Accessibility
    "classes": 65535,   # All classes
    "races": 65535,     # All standard races
    "loregroup": 0,     # 0 = not restricted to one-per-character
    "questitemflag": 1, # Marks this as a quest item (restricted from vendors/trading)

    # Usage Level Restrictions — allow all levels to use
    "reqlevel": 0,
    "reclevel": 0,
    "recskill": 0,
    "clicklevel": 0,
    "clicklevel2": 0,
    "proclevel": 0,
    "proclevel2": 0,

    # Trade & Persistence Flags
    "nodrop": 0,        # Item is tradable
    "norent": 0,        # Item persists after logout
    "artifactflag": 0,  # Not an artifact
    "tradeskills": 0,   # Not a tradeskill component

    # Stackability & Charges
    "stackable": 0,     # Non-stackable (gear)
    "maxcharges": 0,    # Unlimited use if it has a click effect

    # Click Behavior
    "casttime": 0,
    "recastdelay": 0,
    "recasttype": 0,

    # Augment Restrictions — default to no augments
    "augtype": 0,
    "augrestrict": 0,
    "augslot1type": 0,
    "augslot2type": 0,
    "augslot3type": 0
}

COPIED_ITEM_PARAMS = [
    # Core type and equip behavior
    "itemtype",
    "slots",

    # Basic stats and combat effectiveness
    "ac",
    "hp", "mana", "endur",
    "aagi", "adex", "acha", "aint", "astr", "asta",
    "damage", "delay", "elemdmgamt", "elemdmgtype",
    "accuracy", "avoidance", "strikethrough", "stunresist",
    "dotshielding", "manaregen", "enduranceregen", "regen",

    # Click / proc / worn effects
    "clickeffect", "clicktype",
    "proceffect", "proctype",
    "worneffect", "worntype",
    "focuseffect",
    "scrolleffect", "scrolltype",
    "bardeffecttype", "bardeffect",

    # Appearance
    "icon", "idfile",

    # Description fields
    "lore", "comment", "lorefile",

    # Augment types only if they're meant to be copied (optional)
    "augslot1visible", "augslot2visible", "augslot3visible",
    "augslot4visible", "augslot5visible"
]

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    )

def extract_npc_names(path):
    results = []
    for filename in os.listdir(path):
        if filename.endswith("_target.txt"):
            with open(os.path.join(path, filename), "r") as f:
                results.append(f.read().strip())
    return results

def extract_item_info(path):
    items = []
    for filename in os.listdir(path):
        if filename.endswith("_item.txt"):
            filepath = os.path.join(path, filename)
            with open(filepath, "r") as f:
                lines = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

            if len(lines) < 1:
                continue

            with open(filepath, "w") as f:
                for line in lines:
                    f.write(line + "\n")

            item_name = lines[0]
            descriptors = lines[1:]
            items.append((item_name, descriptors, filepath))
    return items

def query_matching_items(descriptors):
    matches = []
    for desc in descriptors:
        sql = f"SELECT id, name FROM items WHERE name LIKE '%{desc.strip()}%';"
        result = stream_sql_to_mariadb(sql)
        if result.returncode == 0:
            rows = [line.split('\t') for line in result.stdout.decode().strip().split('\n') if line]
            matches.extend(row[0] for row in rows if len(row) == 2)
    return matches

def fetch_item_params(item_id):
    sql = f"SELECT {', '.join(COPIED_ITEM_PARAMS)} FROM items WHERE id = {item_id};"
    result = stream_sql_to_mariadb(sql)
    if result.returncode != 0:
        return {}
    parts = result.stdout.decode().strip().split('\t')
    if len(parts) != len(COPIED_ITEM_PARAMS):
        return {}
    return dict(zip(COPIED_ITEM_PARAMS, parts))

def stream_sql_to_mariadb(sql):
    cmd = [
        "docker-compose", "exec", "-T", "mariadb", "mysql", "-BN",
        f"-u{DB_USER}", f"-p{DB_PASS}", DB_NAME
    ]
    return subprocess.run(cmd, input=sql.encode("utf-8"), capture_output=True)

def main():
    setup_logging()
    logger = logging.getLogger(os.path.basename(__file__))

    if len(sys.argv) < 2:
        print("Usage: python3 updateNPCs.py <quest_name>")
        return

    quest_name = sys.argv[1]
    BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "Eulogies", quest_name, "build", "quest"))

    npc_names = extract_npc_names(BASE_PATH)
    item_info = extract_item_info(BASE_PATH)

    for i, npc in enumerate(npc_names):
        if i >= len(RESERVED_IDS):
            break
        npc_id = RESERVED_IDS[i]
        x, y, z = HARDCODED_LOCATIONS[i % len(HARDCODED_LOCATIONS)]
        npc_clean_name = npc.replace(" ", "_")

        sql = f"""
        REPLACE INTO npc_types (id, name, level, race, class, hp, mana, gender, texture, helmtexture)
        VALUES ({npc_id}, '{npc_clean_name}', 10, 1, 1, 100, 0, 0, 1, 1);

        REPLACE INTO spawngroup (id, name) VALUES ({npc_id}, '{npc_clean_name}_spawngroup');
        REPLACE INTO spawn2 (id, spawngroupID, zone, x, y, z, heading)
        VALUES ({npc_id}, {npc_id}, '{QUEST_ZONE}', {x}, {y}, {z}, 0);
        REPLACE INTO spawnentry (spawngroupID, npcID, chance)
        VALUES ({npc_id}, {npc_id}, 100);
        """
        result = stream_sql_to_mariadb(sql)
        if result.returncode != 0:
            logger.error(f"Failed to stream NPC SQL: {result.stderr.decode()}")
            sys.exit(1)
        else:
            logger.info(f"Streamed NPC SQL to MariaDB successfully: '{npc}', npc_id: '{npc_id}'")

    for i, (item_name, descriptors, filepath) in enumerate(item_info):
        if i >= len(RESERVED_ITEM_IDS):
            break
        item_id = RESERVED_ITEM_IDS[i]

        # Match descriptors to items
        match_ids = query_matching_items(descriptors)
        most_common_id = Counter(match_ids).most_common(1)[0][0] if match_ids else None

        if not most_common_id:
            logger.info(f"No matching item descriptions found for '{item_name}', using fallback item ID {DEFAULT_ITEM_ID}.")
            most_common_id = DEFAULT_ITEM_ID

        props = fetch_item_params(most_common_id)
        if not props:
            logger.error(f"Failed to fetch fields for item ID {most_common_id}")
            sys.exit(1)

        all_params = {**props, **STATIC_ITEM_PARAMS}

        field_list = COPIED_ITEM_PARAMS + list(STATIC_ITEM_PARAMS.keys())
        value_list = [str(f"'{v}'") if isinstance(v, str) and not v.isdigit() else str(v) for v in all_params.values()]

        escaped_name = item_name.replace("'", "''")
        sql = f"""
        REPLACE INTO items (id, name, {', '.join(field_list)})
        VALUES ({item_id}, '{escaped_name}', {', '.join(value_list)});
        """

        result = stream_sql_to_mariadb(sql)

        if result.returncode != 0:
            logger.error(f"Failed to stream item SQL: {result.stderr.decode()}")
            sys.exit(1)
        else:
            logger.info(f"Streamed item SQL to MariaDB successfully: '{item_name}', item_id: '{item_id}'")
            with open(filepath, "a") as f:
                f.write(f"# {item_id}\n")

    for i in range(len(npc_names), len(RESERVED_IDS)):
        npc_id = RESERVED_IDS[i]
        sql = f"UPDATE spawnentry SET chance=0 WHERE npcID={npc_id} AND spawngroupID={npc_id};"
        result = stream_sql_to_mariadb(sql)
        if result.returncode != 0:
            logger.error(f"Failed to stream spawnentry SQL: {result.stderr.decode()}")
            sys.exit(1)
        else:
            logger.info(f"Streamed spawnentry SQL to MariaDB successfully for npc id: '{npc_id}'")


if __name__ == "__main__":
    main()

# ai-gen end