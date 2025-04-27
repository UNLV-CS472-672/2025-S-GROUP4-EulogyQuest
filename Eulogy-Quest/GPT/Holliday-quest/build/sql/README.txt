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
│   └── sql                         <------(you are here)
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
│   └── sql
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

Explanation of these sql files.

GPT exports the sql commands necessary to place the NPCs
in-game in a persistent manner (via database insertions).

It is first exported as a .json file, and then it is converted
into a one-shot sql file.

The one-shot sql file has the added behavior of only
inserting if the table entry at that location is free, and
otherwise does an update instead of an attempt at insertion.

Updating allows for iterating.
We have a "debug" process where a simplified version
of the quest is spawned with all the NPCs in the tutorialb zone
at a static, valid location.

Once the quest is ready to move beyond debug-mode, we can
instead generate table entries for the NPC which place
them world-wide.

Note that the Holliday-quest/src/sql/ directory has two files:
  - honored_target_implementation.json
  - basic_honored_target_implementation.json

These two files represent the choice to spawn the NPC in debug-mode
(in static locations in tutorialb), or in production-mode
(with world-wide locations).


============================================================

