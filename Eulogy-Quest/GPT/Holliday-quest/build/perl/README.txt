############################################################
# Directory Structure of Holliday-quest/
.
├── build
│   ├── perl           <--------(you are here)
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

Definitions
NPCs 
  - in-game interactive non-player characters, 
  - aka: Non Player Characters

EQEmu
  - Everquest Emulator
  - aka: Unofficial, enthusiast-ran game server

############################################################

Explanation for
  1. why these perl files are needed and what they do
  2. what the quest actually does and how these files apply

(1)
NPCs are all over Everquest; they are primary to in-game content.
They are the "quest" in Everquest.
Without getting philosophical, the game experience is tied
directly to interactions with NPCs, specifically to their quests.

Once placed in-game, either at the game's initial launch,
on one of the expansion releases, by an official GM, or by
someone running their own custom EQEmu, these NPCs perform
the task of motivating the human player-base to accomplish
tasks for rewards.

This is done by scripting the NPCs to act.
Types of NPC actions include:
  - speaking
  - pathing (walking about)
  - receiving items
  - giving items
  - giving faction (in-game reputation) as a reward

These perl files are where these actions are scripted for
each individual NPC. Each NPC must have a perl script file
if that NPC is to do anything (be interactive).
Their perl script must reside in a directory named with
their location. So, the NPC named "Vahlara", located in the
zone "tutorialb" must have a perl file located at:
`akk-stack/server/quests/tutorialb/`.
So, this file's long name would be:
`akk-stack/server/quests/tutorialb/Vahlara.pl`.

(2)
Practically, pedantically, what the quest does -- specifically:
Eulogy-quests operate with a certain structure.

(Let's ignore the part where the player asks for a specific
 quest to be generated. Instead, here let's just focus on
 the quest -- as though they just walked up to an existing
 quest.)

- First, the player left-clicks on the NPC to target it. 
  The NPC is named "Hollidays ghost".

- The player then types "/say hail", or "/h" into their
  game text-window.

- The NPC has a rule for this interaction in their perl file.
  The NPC returns the text associated with 
  the event of being told "hail".

- This first (originating, and as we'll see also terminating)
  NPC sends the player to the second NPC.

- The second NPC needs something which some lowly spider or
  some other nearby monster ran off with.

     - How do we know this? Well, we hailed this NPC.
       This NPC then told us his story, his need.

     - We might be promted to hear more of the [story].

     - We see [story] in our text window as part of
       the words this NPC is telling us. We click on [story].

     - The story continues. 
       The scripted text associated with [story] is shown
       to the player. Eventually the [links] end, and
       the player goes and whacks the spider on the head,
       retrieves the [lost watch] and returns it to the
       second NPC. The handling of the turn-in for the
       [lost watch] is handled by the perl script. In our case,
       we hand it back to the player and send them to the
       next NPC in the quest-chain.

     - The second NPC thanks the player and sends the player
       off to the third NPC.

     - Multiple NPC which duplicate the basic structure of the
       second NPC are found along this quest's path.

- When the last NPC is visited it is time for the quest's reward.
  Some quests end at an unpredictable place; these are linear.
  Some start and end at the same NPC; these are circular.
  Eulogy-quest is hardcoded circular with a total of 5 NPCs.

- The last NPC takes the collected item or items
  (4 items in our case)
  and then gives the player a reward.
  This is all scripted in the final (here, the first) 
  NPC's perl file.


============================================================

