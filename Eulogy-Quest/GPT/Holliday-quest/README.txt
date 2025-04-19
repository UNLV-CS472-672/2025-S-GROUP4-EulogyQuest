############################################################ 
# Directory Structure of
# akk-stack/Eulogy-Quest/GPT/Holliday-quest/
.                               <-------------(you are here)
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

File creation is done by using items in:  Holliday-quest/src/
Created files are stored in:              Holliday-quest/build/

To create the quest itself 
(the idea in a structured json document)
  - create the document using the files in:     src/quest/
  - store the created document in:              build/quest/

To create the sql files
(needed to place the NPCs in-game)
  - create the sql files using the files in:    src/sql/
  - store the created sql files in:             build/sql/

To create the perl files
(needed to script the NPCs)
  - create the perl files using the files in:   src/perl/
  - store the created perl files in:            build/perl/

Each directory has detailed instruction in its README.txt
The file creation and placement is by-hand for now,
but the organization here should well facilitate
automation with a master script.              <-----(TODO)
Note that this master script will need a ChatGPT API key.

README.txt files located in Holliday-quest/src
deal with implementation details.

Readme.txt files located in Holliday-quest/build
deal with explanations of use and purpose.

Another quest can be created (by hand) using this directory.
Simply copy the directory, rename it, delete the files in
the build/ directory, and follow the instructions.
Change the references to "Doc Holliday" to your new
"honored_target".

Soon we'll have an automated master script that will do this
re-creation, requiring only the entry of the "honored_target"
(and possibly optionally debug-mode or not).

Suggested reading-order for all the README.txt files in the project:
(Find the README.txt in the given directories below)

  A. If you're just digesting what's going on:
    0. uml/Quest-Generation-Flowchart.pdf
    1. This README.txt (well done!)
    2. build/
    3. src/
    4. build/quest/
    5. src/quest/
    6. build/sql/
    7. src/sql/
    8. build/perl
    9. src/perl

  B. If you're following the directions to produce a new quest:
    0. uml/Quest-Generation-Flowchart.pdf
    1. This README.txt (well done!)
    2. build/
    3. build/quest
    4. build/sql
    5. build/perl
    6. src/
    7. src/quest
    8. src/sql
    9. src/perl


Ready?:
Either way, head over to:
    build/README.txt, and
    uml/Quest-Generation-Flowchart.pdf


============================================================
