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


def generate_insert_sql(npc_id, name):
    return f"""
    INSERT IGNORE INTO npc_types
        SET id={npc_id},
            name='{name}';

    INSERT IGNORE INTO spawngroup
        SET id={npc_id},
            name='SpawnGroup_{npc_id}';

    INSERT IGNORE INTO spawn2
        SET id={npc_id},
            spawngroupID={npc_id};

    INSERT IGNORE INTO spawnentry
        SET spawngroupID={npc_id},
            npcID={npc_id},
            chance=0;
    """


def generate_update_sql(npc, npc_id):
    name = npc["npc"]
    race = npc.get("appearance", {}).get("race", "")
    gender = npc.get("appearance", {}).get("gender", "")
    loc = npc.get("location", {})
    coords = loc.get("coordinates", {})
    x = coords.get("x", 0)
    y = coords.get("y", 0)
    z = coords.get("z", 0)
    heading = loc.get("heading", 0)
    zone = loc.get("zone", "")

    print(f"Need support for race: {race}")
    print(f"Need support for gender: {gender}")

    return f"""
    UPDATE npc_types
        SET name='{name}'
        WHERE id={npc_id};

    UPDATE spawn2
        SET x={x},
            y={y},
            z={z},
            heading={heading},
            zone='{zone}'
        WHERE id={npc_id} AND spawngroupID={npc_id};

    UPDATE spawnentry
        SET chance=100
        WHERE npcID={npc_id} AND spawngroupID={npc_id};
    """


def do_stuff_with_dialog(dialog_text):
    if dialog_text:
        print(f"Need support for captured dialog: {dialog_text}")


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

    npc_entries = load_npcs_from_json(npc_json_path)
    limited_npcs = npc_entries[:len(RESERVED_IDS)]

    # ai-gen start (Chat-GPT 4o, 2)
    for npc, npc_id in zip(limited_npcs, RESERVED_IDS):
        print(f"\nProcessing NPC: {npc['npc']} → ID: {npc_id}")
        # ai-gen end (Chat-GPT 4o, 2)
        sql = generate_insert_sql(npc_id, npc['npc'])
        stream_sql_to_mariadb(sql)

        sql = generate_update_sql(npc, npc_id)
        stream_sql_to_mariadb(sql)

        dialog = npc.get("dialogue", {}).get("hail-text", "")
        do_stuff_with_dialog(dialog)

    used_ids = set(RESERVED_IDS[:len(limited_npcs)])
    unused_ids = set(RESERVED_IDS) - used_ids

    for npc_id in sorted(unused_ids):
        print(f"\nDisabling unused NPC slot at ID {npc_id}")
        sql = generate_disable_spawn_sql(npc_id)
        stream_sql_to_mariadb(sql)

    print("\nAll done.")


if __name__ == "__main__":
    main()
