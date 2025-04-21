### Author: Tanner Donovan
### Script Development Start Date: 4/14/2025
### Description: This script converts through automation a JSON input {honored_target}_implementation.json built from previous script and turns it into an executable PERL.
###              This will prove useful for all quest development steps. 

import json
import os
import sys

# Constants
NPC_TYPES_START_ID = 2000100
SPAWNGROUP_START_ID = 2000100
SPAWN2_START_ID = 3266100

def convert_json_to_executable_perl(input_file, db_config):
    with open(input_file, 'r') as f:
        data = json.load(f)

    base = os.path.basename(input_file)
    honored_target = base.replace("_quest", "").replace(".json", "")
    perl_filename = f"{honored_target}_implementation.pl"

    npc_type_insert = []
    spawngroup_insert = []
    spawnentry_insert = []
    spawn2_insert = []

    spawngroup_id = SPAWNGROUP_START_ID
    spawn2_id = SPAWN2_START_ID

    for npc in data.get("npc_scripting", []):
        npc_id = npc["npc_id"]
        name = npc["name"].replace("'", "''")
        texture = npc.get("appearance", {}).get("texture", 0)
        helm_texture = npc.get("appearance", {}).get("helm_texture", 0)

        loc = npc["location"]
        zone = loc["zone"]
        x, y = loc["x"], loc["y"]
        z = loc["z"] + (10 if loc.get("outdoor", False) else 5)
        heading = loc["heading"]

        npc_type_insert.append(
            f'"INSERT INTO npc_types (id, name, texture, helmtexture) VALUES ({npc_id}, \'{name}\', {texture}, {helm_texture});"'
        )
        spawngroup_insert.append(
            f'"INSERT INTO spawngroup (id, name) VALUES ({spawngroup_id}, \'{zone}_{spawngroup_id}\');"'
        )
        spawnentry_insert.append(
            f'"INSERT INTO spawnentry (spawngroupID, npcID, chance) VALUES ({spawngroup_id}, {npc_id}, 100);"'
        )
        spawn2_insert.append(
            f'"INSERT INTO spawn2 (id, spawngroupID, zone, x, y, z, heading) VALUES ({spawn2_id}, {spawngroup_id}, \'{zone}\', {x}, {y}, {z}, {heading});"'
        )

        spawngroup_id += 1
        spawn2_id += 1

    # DB config
    db_host, db_name, db_user, db_pass = db_config

    with open(perl_filename, 'w') as f:
        f.write("#!/usr/bin/perl\n")
        f.write("use strict;\nuse warnings;\nuse DBI;\nuse IO::File;\n\n")

        f.write("# DB connection\n")
        f.write(f"my $dsn = 'DBI:mysql:database={db_name};host={db_host}';\n")
        f.write(f"my $user = '{db_user}';\n")
        f.write(f"my $password = '{db_pass}';\n")
        f.write("my $dbh = DBI->connect($dsn, $user, $password, { RaiseError => 0, AutoCommit => 1 }) or die \"Connection failed: $DBI::errstr\\n\";\n\n")

        f.write("# Open error log\n")
        f.write("my $log = IO::File->new('> found_conversion_issues.txt') or die \"Could not open found_conversion_issues.txt: $!\\n\";\n\n")

        def perl_array(name, array):
            return f"my @{name} = (\n  " + ",\n  ".join(array) + "\n);\n\n"

        f.write(perl_array("npc_type_insert", npc_type_insert))
        f.write(perl_array("spawngroup_insert", spawngroup_insert))
        f.write(perl_array("spawnentry_insert", spawnentry_insert))
        f.write(perl_array("spawn2_insert", spawn2_insert))

        f.write("""foreach my $sql (@npc_type_insert, @spawngroup_insert, @spawnentry_insert, @spawn2_insert) {
    eval {
        $dbh->do($sql);
    };
    if ($@) {
        print $log "SQL Error while executing: $sql\\nError: $@\\n";
        warn "SQL Error logged for: $sql\\n";
        # die "Aborting due to SQL error.\\n";  # Optional fail-fast
    }
}
$log->close;
$dbh->disconnect;
print "Done\\n";
""")

    os.chmod(perl_filename, 0o755)
    print(f" Perl script created: {perl_filename} (ready to execute)")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python convert_to_perl_exec.py quest.json db_host db_name db_user db_pass")
        sys.exit(1)

    convert_json_to_executable_perl(
        input_file=sys.argv[1],
        db_config=sys.argv[2:]
    )
