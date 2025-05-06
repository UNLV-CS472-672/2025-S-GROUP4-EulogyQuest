import os
import sys
import logging
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv("../../.env")
load_dotenv("../.env")

# === CONFIGURATION ===
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

# === LOGGING ===
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    )
    return logging.getLogger(os.path.basename(__file__))

# === HELPERS ===
def extract_names_by_file_suffix(path, suffix):
    return [
        open(os.path.join(path, f)).read().strip()
        for f in os.listdir(path)
        if f.endswith(suffix + ".txt")
    ]

def stream_sql(sql):
    cmd = [
        "docker-compose", "exec", "-T", "mariadb", "mysql",
        f"-u{DB_USER}", f"-p{DB_PASS}", DB_NAME
    ]
    return subprocess.run(cmd, input=sql.encode("utf-8"), capture_output=True)

def insert_npc(npc_name, npc_id, location):
    clean_name = npc_name.replace(" ", "_")
    x, y, z = location

    return f"""
    REPLACE INTO npc_types (id, name, level, race, class, hp, mana, gender, texture, helmtexture)
    VALUES ({npc_id}, '{clean_name}', 10, 1, 1, 100, 0, 0, 1, 1);

    REPLACE INTO spawngroup (id, name) VALUES ({npc_id}, '{clean_name}_spawngroup');
    REPLACE INTO spawn2 (id, spawngroupID, zone, x, y, z, heading)
    VALUES ({npc_id}, {npc_id}, '{QUEST_ZONE}', {x}, {y}, {z}, 0);
    REPLACE INTO spawnentry (spawngroupID, npcID, chance)
    VALUES ({npc_id}, {npc_id}, 100);
    """

def insert_item(item_name, item_id):
    return f"""
    REPLACE INTO items (id, name, aagi, ac, accuracy, classes, races, icon, loregroup, magic, weight, size, itemtype, favor)
    VALUES ({item_id}, '{item_name}', 0, 5, 0, 65535, 65535, 128, 0, 1, 1, 1, 10, 0);
    """

def disable_unused_npc_spawn(npc_id):
    return f"UPDATE spawnentry SET chance=0 WHERE npcID={npc_id} AND spawngroupID={npc_id};"

# === MAIN ===
def main():
    logger = setup_logging()

    if len(sys.argv) < 2:
        logger.error("Usage: python3 updateNPCs.py <quest_name>")
        sys.exit(1)

    quest_name = sys.argv[1]
    quest_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "Eulogies", quest_name, "build", "quest"))

    npc_names = extract_names_by_file_suffix(quest_path, "_target")
    item_names = extract_names_by_file_suffix(quest_path, "_item")

    # Insert NPCs
    for i, npc in enumerate(npc_names):
        if i >= len(RESERVED_IDS): break
        sql = insert_npc(npc, RESERVED_IDS[i], HARDCODED_LOCATIONS[i % len(HARDCODED_LOCATIONS)])
        result = stream_sql(sql)
        if result.returncode != 0:
            logger.error(f"NPC insert failed: {result.stderr.decode()}")
            sys.exit(1)
        logger.info(f"Inserted NPC '{npc}' with ID {RESERVED_IDS[i]}")

    # Insert Items
    for i, item in enumerate(item_names):
        if i >= len(RESERVED_ITEM_IDS): break
        sql = insert_item(item, RESERVED_ITEM_IDS[i])
        result = stream_sql(sql)
        if result.returncode != 0:
            logger.error(f"Item insert failed: {result.stderr.decode()}")
            sys.exit(1)
        logger.info(f"Inserted Item '{item}' with ID {RESERVED_ITEM_IDS[i]}")

    # Disable unused NPC spawn entries
    for npc_id in RESERVED_IDS[len(npc_names):]:
        sql = disable_unused_npc_spawn(npc_id)
        result = stream_sql(sql)
        if result.returncode != 0:
            logger.error(f"Disable spawnentry failed: {result.stderr.decode()}")
            sys.exit(1)
        logger.info(f"Disabled spawnentry for NPC ID {npc_id}")

if __name__ == "__main__":
    main()
