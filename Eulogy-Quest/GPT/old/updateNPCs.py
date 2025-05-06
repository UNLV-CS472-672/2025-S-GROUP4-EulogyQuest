# ai-gen start (Chat-GPT 4o-mini-high, ?)
# ?= much re-prompting; final result copy/pasted
#
# Script to insert NPCs and items into the database based on quest build files.

import os
import sys
import logging
import subprocess
from dotenv import load_dotenv

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

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    )

def extract_names_by_file_suffix(path, suffix):
    results = []
    for filename in os.listdir(path):
        if filename.endswith(suffix + ".txt"):
            with open(os.path.join(path, filename), "r") as f:
                results.append(f.read().strip())
    return results


def stream_sql_to_mariadb(sql):
    cmd = [
        "docker-compose", "exec", "-T", "mariadb", "mysql",
        f"-u{DB_USER}", f"-p{DB_PASS}", DB_NAME
    ]
    result = subprocess.run(cmd, input=sql.encode("utf-8"), capture_output=True)
    return result

def main():
    logger = logging.getLogger(os.path.basename(__file__))

    if len(sys.argv) < 2:
        print("Usage: python3 updateNPCs.py <quest_name>")
        return

    quest_name = sys.argv[1]
    BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "Eulogies", quest_name, "build", "quest"))

    npc_names = extract_names_by_file_suffix(BASE_PATH, "_target")
    item_names = extract_names_by_file_suffix(BASE_PATH, "_item")

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

    for i, item in enumerate(item_names):
        if i >= len(RESERVED_ITEM_IDS):
            break
        item_id = RESERVED_ITEM_IDS[i]

        sql = f"""
        REPLACE INTO items (id, name, aagi, ac, accuracy, classes, races, icon, loregroup, magic, weight, size, itemtype, favor)
        VALUES ({item_id}, '{item}', 0, 5, 0, 65535, 65535, 128, 0, 1, 1, 1, 10, 0);
        """
        result = stream_sql_to_mariadb(sql)
        if result.returncode != 0:
            logger.error(f"Failed to stream item SQL: {result.stderr.decode()}")
            sys.exit(1)
        else:
            logger.info(f"Streamed item SQL to MariaDB successfully: '{item}', item_id: '{item_id}'")

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
    setup_logging()
    main()

# ai-gen end