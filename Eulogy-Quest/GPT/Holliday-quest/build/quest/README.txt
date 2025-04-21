############################################################
# Directory Structure of Holiday-quest/
.
├── build
│   ├── perl
│   │   ├── Ada.pl
│   │   ├── Hollidays.pl
│   │   ├── Mister.pl
│   │   ├── Pastor.pl
│   │   ├── README.txt
│   │   └── Sylas.pl
│   ├── quest               <--------(you are here)
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

Explanation of doc_holliday_quest.json.

This file is the starting point for everything that is produced.
This is the high-level recipie.

This is where the ChatGPT "deliverables" are stored.
The storage is structured, using json.
The idea of "deliverables" was first spoken of in
Eulogy-quest back in DP-1, on the GPT-table
(of which there were 18 action-items describing what we
 needed of GPT and what we'd call the items returned by GPT).

My hope when creating this was that most of these deliverables
would be real in-game assets, tied together by a creative story.
So, when I ask GPT for a zone to put the NPC into, it almost always
comes up with a real in-game zone. But when I ask it to
name a real nearby monster (mob), it dreams up the name of a mob
who might very-well be in zone. When I ask it to produce items
associated with the quest, it again dreams-up items.

I was planning on the item dreaming. So I made sure to also ask
for a list of descriptors for the items. Early version of the
prompt did this for me. I want to revisit this and make sure
to get this functionality back. --- (TODO) 
However, I'll do it as another
stand-alone prompt. I don't want to have any more problems with
this primary quest-prompt.

Sadly, even though it got the zone choice and naming correct 99%
of the time, it does not get placement **within** the zone correct.
The suggestions for ambient settings within the zones is
usually terrific (like the broken walls in eastwastes). 
However, it very often totally dreams up the x,y,z locations in-zone.


If we were baking a cake,
this file is less mis-en-place, and more shopping-list.


============================================================

