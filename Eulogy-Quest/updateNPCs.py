import os
import sys
import json
import subprocess
from dotenv import load_dotenv

# ai-gen start (Chat-GPT 4o, 2)
load_dotenv("../.env")

DB_USER = "root"
DB_PASS = os.getenv("MARIADB_ROOT_PASSWORD")
DB_NAME = os.getenv("MARIADB_DATABASE")
RESERVED_IDS = list(range(1999900, 1999905))
RESERVED_ITEM_IDS = list(range(200000, 200020))

def stream_sql_to_mariadb(sql_text: str):
    try:
        proc = subprocess.Popen(
            [
                "docker-compose", "exec", "-T", "mariadb",
                "mysql", f"-u{DB_USER}", f"-p{DB_PASS}", DB_NAME
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = proc.communicate(input=sql_text)

        if proc.returncode != 0:
            print("SQL execution failed:")
            print(stderr)
        else:
            print("SQL executed successfully")

    except Exception as e:
        print(f"Error executing SQL: {e}")

# ai-gen end (Chat-GPT 4o, 2)

def load_npcs_from_json(json_path):
    with open(json_path) as f:
        data = json.load(f)

    return data.get("npc_scripting", [])

def load_items_from_json(json_path):
    with open(json_path) as f:
        data = json.load(f)
    
    items = []
    items.extend(data.get("quest_reward_items", []))
    items.extend(data.get("required_offer_items", {}).values())
    items.extend(data.get("force_obtained_items", {}).values())

    # ai-gen start (Chat-GPT 4o, 0)
    # Remove duplicates before returning the item list
    unique = {(item["name"]): item for item in items if "name" in item}
    # ai-gen end (Chat-GPT 4o, 0)
    return list(unique.values())

def load_loot_drops(npc_entries):
    loot_drops={}

    for npc in npc_entries:
        method = npc.get("npc_method_of_receipt")
        if method and method.strip() == "taken-by-force":
            npc_name = npc.get("name")
            item_name = npc.get("gives_item", {}).get("name")
            if npc_name and item_name:
                loot_drops[npc_name]=item_name

    return loot_drops

def generate_npc_sql(npc, npc_id):
    # name = npc["npc"] ## Changed due to ChatGPT inconsistency
    name = npc["name"].replace("'", "''")
    # race = npc.get("appearance", {}).get("race", "")
    # gender = npc.get("appearance", {}).get("gender", "")
    loc = npc.get("location", {})
    # coords = loc.get("coordinates", {}) ## Changed due to ChatGPT inconsistency
    x = loc.get("x", 0)
    y = loc.get("y", 0)
    z = loc.get("z", 0)
    # x = coords.get("x", 0) ## Changed due to ChatGPT inconsistency
    # y = coords.get("y", 0) ## Changed due to ChatGPT inconsistency
    # z = coords.get("z", 0) ## Changed due to ChatGPT inconsistency
    heading = loc.get("heading", 0)
    zone = loc.get("zone", "")

    # print(f"Need support for race: {race}")
    # print(f"Need support for gender: {gender}")

    return f"""
    INSERT INTO npc_types (id, name)
    VALUES ({npc_id}, '{name}')
    ON DUPLICATE KEY UPDATE
        name = '{name}';

    INSERT INTO spawngroup (id, name)
    VALUES ({npc_id}, 'SpawnGroup_{npc_id}')
    ON DUPLICATE KEY UPDATE
        name = 'SpawnGroup_{npc_id}';

    INSERT INTO spawn2 (id, spawngroupID, x, y, z, heading, zone)
    VALUES ({npc_id}, {npc_id}, {x}, {y}, {z}, {heading}, '{zone}')
    ON DUPLICATE KEY UPDATE
        x = {x},
        y = {y},
        z = {z},
        heading = {heading},
        zone = '{zone}';

    INSERT INTO spawnentry (npcID, spawngroupID, chance)
    VALUES ({npc_id}, {npc_id}, 100)
    ON DUPLICATE KEY UPDATE
        chance = 100;
    """

def generate_item_sql(item, item_id):
    name = item["name"].replace("'", "''")
    # other item params go here later
    # race/class = 65535 flag for all races/classes
    # icon = 682 : a simple rolled scroll icon
    # loregroup = <reserved_id> used for quest items that should be unique
    # color = I took that ugly number from an existing entry. Unsure if its used. More testing needed

    return f"""
    INSERT INTO items (id, name, classes, races, idfile, icon, color, loregroup)
    VALUES ({item_id}, '{name}', 65535, 65535, 'IT63', 682, 4278190080, {item_id})
    ON DUPLICATE KEY UPDATE
        name = '{name}',
        classes = 65535,
        races = 65535,
        idfile = 'IT63',
        icon = 682,
        loregroup = {item_id},
        color = 4278190080;
    """

def generate_loot_drop_sql(npc_id, item_id):
    # For reference if we make drops more complex
    # loottable         : All drops assigned to a mob
    # loottable_entries : Assign many/one drops to a single table using composite keys (loottable_id, lootdrop_id))
    # lootdrop          : Type of loot dropped by a mob
    # lootdrop_entries  : Assign many/one item to a single lootdrop using composite key (lootdrop_id, item_id)

    # Simple Example: Spider Mob Drops: 100% silk, 50% chance of an eye
    # loottable         : (table_id_1, spider_drops)
    # loottable_entries : (table_id_1, lootid1) AND (tableid1, lootid2)
    # lootdrop_entries  : (loot_id_1, silk_id) AND (loot_id_2, eye_id)
    # lootdrop          : (loot_id_1, 100%) AND (loot_id_2, 50%)

    return f"""
    UPDATE npc_types
        SET loottable_id={item_id},
            isquest=0
        WHERE id={npc_id};

    INSERT INTO lootdrop (id, name)
    VALUES ({item_id}, 'EQ_NPC_{npc_id}')
    ON DUPLICATE KEY UPDATE
        name = 'EQ_NPC_{npc_id}';

    INSERT INTO lootdrop_entries (lootdrop_id, item_id, chance)
    VALUES ({item_id}, {item_id}, 100)
    ON DUPLICATE KEY UPDATE
        chance = 100;

    INSERT INTO loottable (id, name, done)
    VALUES ({item_id}, 'EQ_NPC_{npc_id}', 1)
    ON DUPLICATE KEY UPDATE
        name = 'EQ_NPC_{npc_id}',
        done = 1;

    INSERT INTO loottable_entries (loottable_id, lootdrop_id, probability)
    VALUES ({item_id}, {item_id}, 100)
    ON DUPLICATE KEY UPDATE
        probability = 100;

    """

def generate_disable_spawn_sql(npc_id):
    return f"""
    UPDATE spawnentry
        SET chance=0
        WHERE npcID={npc_id} AND spawngroupID={npc_id};
    """


def main():
    # ai-gen start (Chat-GPT 4o, 2)
    if len(sys.argv) < 2:
        print("Usage: python3 updateNPCs.py <json_file_path>")
        return

    npc_json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "gen_out", sys.argv[1]))
    # ai-gen end (Chat-GPT 4o, 2)

    # collecting info from json files
    npc_entries = load_npcs_from_json(npc_json_path)
    item_list   = load_items_from_json(npc_json_path)
    loot_drops  = load_loot_drops(npc_entries)

    # making sure we stay in the bounds of our reserved ids
    limited_items = item_list[:len(RESERVED_ITEM_IDS)]
    assert len(item_list) <= len(RESERVED_ITEM_IDS), "Not enough reserved IDs for all items"
    limited_npcs = npc_entries[:len(RESERVED_IDS)]
    assert len(npc_entries) <= len(RESERVED_IDS), "Not enough reserved IDs for all NPCs"

    # A small workaround, if you have a better way let me know
    # I swap key-value pairs in the dict so that I can search for item_name without a nested for loop (pretty sure its hashed)
    loot_items = {item_name: npc_name for npc_name, item_name in loot_drops.items()}

    # iterate all quest items 
    # generate their sql insert/update and feed to the DB.
    # loot is treated differently, so it's tracked in loot_drops and the items are matched by name
    # if the item is a loot_drop, replace the item_name by the reserved id we used. 
    for item, item_id in zip(limited_items, RESERVED_ITEM_IDS):
        item_name = item['name']
        print(f"\nProcessing Item: {item_name} → ID: {item_id}")
        
        npc_name = loot_items.get(item_name)
        if npc_name:
            loot_drops[npc_name] = item_id
        
        sql = generate_item_sql(item, item_id)
        stream_sql_to_mariadb(sql)

    # iterate all NPCs 
    # generate their sql insert/update and feed to the DB.
    # if the npc has quest loot drops, generate the sql insert/update for that and pipe to DB
    for npc, npc_id in zip(limited_npcs, RESERVED_IDS):
        npc_name = npc['name']
        print(f"\nProcessing NPC: {npc_name} → ID: {npc_id}")

        sql = generate_npc_sql(npc, npc_id)
        stream_sql_to_mariadb(sql)

        if npc_name in loot_drops:
            item_id = loot_drops[npc_name]
            sql = generate_loot_drop_sql(npc_id, item_id)
            stream_sql_to_mariadb(sql)

    # check for unused NPC ids
    # needed incase we generate a quest with 5 npcs, then one with 3 npcs
    # we don't want the 2 lingering that didn't get overwritten
    used_ids = set(RESERVED_IDS[:len(limited_npcs)])
    unused_ids = set(RESERVED_IDS) - used_ids

    # disable the spawns of the unused id spots
    for npc_id in sorted(unused_ids):
        print(f"\nDisabling unused NPC slot at ID {npc_id}")
        sql = generate_disable_spawn_sql(npc_id)
        stream_sql_to_mariadb(sql)

    print("\nAll done.")


if __name__ == "__main__":
    main()
