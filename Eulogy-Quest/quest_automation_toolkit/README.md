# Quest Automation Toolkit

This project automates the creation of PERL scripts for EverQuest NPC quest integration. The toolkit includes two main Python scripts:

## `convert_json_to_executable_perl.py`

This script converts a given JSON quest implementation file into a MariaDB-compatible Perl script that inserts NPCs, spawns, and other quest data into the database.

### Usage:
```bash
python convert_json_to_executable_perl.py quest.json db_host db_name db_user db_pass
```
quest.json: The input JSON file containing NPC and spawn data - will need to give folder directory route for this as well.
db_host, db_name, db_user, db_pass: Our MariaDB database connection parameters.
---This script will output a .pl Perl script that can be executed to insert quest data into MariaDB database.

## generate_quest_perl_script.py
This script generates a PERL quest script with NPC dialogue and item-handling logic. It will read a JSON input file and create a .pl script with logic for NPC dialogues (using EVENT_SAY) and item handins (using EVENT_ITEM).

### Usage:
```bash
python generate_quest_perl_script.py quest.json
```
quest.json: The input JSON file containing quest data.
---This script outputs a Perl file ready to be used for quest interaction in the game.

### Error Logging
A .txt will be created called quest_error_log.txt and will log any automation/user input issues that are not accepted by the quest reads. This may be most prevalent in the SQL writes.