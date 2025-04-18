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
│   ├── quest                         <-------(you are here)
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

Directions to create "doc_holliday_quest.json"

Into ChatGPT:
First upload 
  - `GPT_quest_gen_prompt.json`, 
  - `dialogue_structure.json`, and 
  - `quest_generation_wrapper.json`.
(Don't hit enter yet.)

Second, enter (copy/paste) this line as the prompt to GPT 
(find this prompt in `quest_generation_master_prompt.json`):
(Don't hit enter yet.)

"  ## Copy the text below ##

I’ve uploaded `GPT_quest_gen_prompt.json`, `dialogue_structure.json`, and `quest_generation_wrapper.json`.

Please read and follow all structural and stylistic rules described in those files.

Now generate a full JSON-formatted EverQuest quest for the honored_target = 'Doc Holliday'.  Begin by creating the complete quest scaffold, and ask me to confirm before implementing each NPC.

"  ## Copy the text above ##

Third, hit enter.

Note: ChatGPT likes to sometimes give a slightly different name to the resulting .json file.
This can be "doc_holiday_quest.json", "doc_holiday_quest_final.json", etc.
This can even happen (but less likely) if you are strict with the prompt.
Any automation of this process will need 
to verify that the resulting file is named "doc_holliday_quest.json"
Place the resulting file in Holliday-quest/build/quest/

Next step:
Enter the src/sql/ directory to create the sql implementation files.


============================================================
