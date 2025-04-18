############################################################
# Directory Structure of Holliday-quest/
.
├── build
│   ├── perl
│   │   ├── Ada.pl
│   │   ├── Hollidays.pl
│   │   ├── Mister.pl
│   │   ├── Pastor.pl
│   │   ├── README.txt
│   │   └── Sylas.pl
│   ├── quest
│   │   ├── doc_holliday_quest.json
│   │   └── README.txt
│   ├── README.txt
│   └── sql
│       ├── doc_holliday_implementation.json
│       ├── doc_holliday_implementation.sql
│       └── README.txt
├── Holliday-working.png
├── Note-from-the-author-about-GPT.txt
├── README.md
├── README.txt
├── src
│   ├── perl
│   │   ├── dialogue_loader.py
│   │   ├── doc_holliday_quest.json
│   │   ├── README.txt
│   │   └── Unterminated-string-literal-fix.png
│   ├── quest
│   │   ├── dialogue_structure.json
│   │   ├── GPT_quest_gen_prompt.json
│   │   ├── quest_generation_master_prompt.json
│   │   ├── quest_generation_wrapper.json
│   │   └── README.txt
│   ├── README.txt
│   └── sql                          <-------(you are here)
│       ├── basic_honored_target_implementation.json
│       ├── honored_target_implementation.json
│       ├── implementation_master_prompt.json
│       ├── json_prompt.json
│       ├── npc-db-lookup.png
│       ├── README.txt
│       └── sql_prompt.json
├── tree.txt
└── uml
    ├── Lucidchart-link.txt
    ├── parts
    │   ├── 1-Overview.png
    │   ├── 2-Quest-blueprint-phase.png
    │   ├── 3-SQL-generation-part1.png
    │   ├── 4-SQL-generation-part2.png
    │   ├── 5-Perl-generation.png
    │   └── 6-Input-the-sql-and-perl.png
    └── Quest-Generation-Flowchart.pdf

11 directories, 42 files
############################################################

Below find 2 separate directions to produce:
  1. doc_holliday_implementation.json
  2. doc_holliday_implementation.sql

############################################################

(1, json)
Directions to create "basic_doc_holliday_implementation.json" 
OR "doc_holliday_implementation.json" (if not debugging).

Into ChatGPT:
First, upload:
  `doc_holliday_quest.json` 

Second, upload:
  either:
    `basic_honored_target_implementation.json`
    (for all NPCs to be spawned in tutorialb)
  or:
    `honored_target_implementation.json`
    (to spawn the NPCs at locations around the world).
(don't hit enter yet).

Third, from `json_prompt.json`, use the correct prompt:
(by "use", I mean either copy/paste by hand into GPT, or
 pull the correct value when automating this process)
  - `(json_prompt.json).basic` (if doing a basic/debug build), OR
  - `(json_prompt.json).production` (if doing a production build).

Third, press Enter.


(2, sql)
Directions to create "doc_holliday_implementation.sql"

First:
Upload `doc_holliday_implementation.json` and  `sql_prompt.json`
(don't hit enter yet)

Second:
Use/Paste the value for "prompt" in implementation_master_prompt.json.

Then press Enter.


============================================================

(TODO)--> Combine basic_honored_target_implementation.json
                + honored_target_implementation.json
          ..and key the choice as done in `json_prompt.json`


