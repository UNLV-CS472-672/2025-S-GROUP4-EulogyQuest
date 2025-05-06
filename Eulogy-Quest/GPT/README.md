# Dialog improvement change
## Old behavior: 
`watch_triggers.py` calls `create-quest.py` calls `base-story.py`, `updateNPCs.py`, `perl-script-NPCs.py`.
## New behavior:
4/28 - present (5/1)
`watch_triggers.py` (watchdog service script) listens for, and executes
`create-quest_v2.py` when hearing a change to Eulogyquest<First_Last>.trigger in `akk-stack/server/quests/tutorialb`.

Instead of calling `base-story.py` (which was our emergency strategy of just getting NPCs in game and given garbage dialog immediately), we'll instead call `ghost-prompt-raw.py`, `get-delivery-item.py`, and `get-delivery-target.py`.

Previously, `base-story.py` created `ghost_task.txt`, 
`ghost_delivery_target.txt`, `ghost_delivery_target_location.txt`, and `ghost_delivery_item.txt`.

`<First_Last>-delivery-item.txt`, and `<First_Last>-delivery-target.txt`.

Now, `perl-script-NPCs.py` is coded to take the dialog in `ghost_task.txt` and use this to create/update the Ghost NPC's perl file, inserting dialog into the EVENT_SAY routine.

This needs to change. Before, the idea was to define **up-front** the names of the ghost and the 4 additional NPCs. Because we need to take a **small-to-large** approach (non-monolithic), the names of the associated NPCs are not known "at compile time" so-to-speak. The **one** "next" NPC is identified sequentially. This means we need to keep track of the number each NPC corresponds to, so that when the 5th NPC (zero index == ghost, last NPC == npc4) is created, that 5th NPC needs to know that their **delivery-target** is the quest-originating **Ghost** npc.

## ghost-prompt-raw_v2.py
Call-Dir:  akk-stack/Eulogy-Quest/GPT/prompts
IN:        1. [string of two words for the name of the honored_target]
              aka: <honored_target_name>
           2. output (build) directory:
              GPT/Eulogies/<honored_target>/build/quest
OUTPUT:    `Ghost-dialog-<First_Last>-raw_<counter>.txt`

Instead of `create-quest.py` calling `base-story.py`, it will first call `ghost-prompt-raw.py`, outputting the file `Ghost-dialog-<First_Last>-raw_<counter#>.txt`. The counter is to keep track of additional files generated, so that any new files don't overwrite the previous ones. This facilitates iteration, being able to compare results of new runs. The perl generation phase `perl-script-NPCs.py` needs to instead grab its text from `Ghost-dialog-<First_Last>-raw_<counter#>.txt`, taking the highest counter value. Currently, `perl-script-NPCs.py` pulls the dialog from `ghost_task.txt`.

## get-delivery-target_v2.py
Call-Dir: akk-stack/Eulogy-Quest/GPT/prompts
IN:       1. <honored_target_name>
          2. <story_file_name>
          3. [output (build) directory]:
             GPT/Eulogies/<honored_target>/build/quest (default)
OUTPUT:   `<First_Last>-delivery-target.txt`

This script reads in the output of `ghost-prompt-raw_v2.py` (the <story_file_name>).
Similarly, instead of `base-story.py` creating `ghost_delivery_target.txt`, `ghost_delivery_item.txt`, and `ghost_delivery_target_location.txt` all at-once, we'll create these using `get-delivery-target_v2.py` and `get-delivery-item_v2.py`. The first script `get-delivery-target_v2.py` returns both the **recipient** and their **location** in a text file with 5 "lines".
1. The name of the intended recipient.
2. The location. 
3. An immersive description of the location. 
4. a blank line. 
5. A one-paragraph explanation of why they are at this location in the first place. This last paragraph's reasoning will serve as (hopefully reliable) input in generating this NPC's dialog when creating the next "step" in the quest, linking this NPC to the ghost's story.

## get-delivery-item_v2.py
Call-Dir: akk-stack/Eulogy-Quest/GPT/prompts
IN:       1. <honored_target_name>
          2. <story_file_name>
          3. [output (build) directory]:
             GPT/Eulogies/<honored_target>/build/quest (default)
OUTPUT:   `<First_Last>-delivery-item.txt`

This script reads in the output of `ghost-prompt-raw.py_v2` (the <story_file_name>) and returns 6 lines in a txt file:
Lines:
1:   The item's name
2-6: One word adjectives describing the physical characteristic of the item

# Overview:
Quests are automatically generated.
If you want to see a quest generated in-game on our AWS server
for "Robin Williams":
```
curl --ftp-pasv -T Eulogyquest_Robin_Williams.trigger \
     ftp://quests:BU5H9LaaGXe8cUj6SIZI0eXpGeDmVJW@184.169.160.73/\
tutorialb/Eulogyquest_Robin_Williams.trigger
```

# Explanation:

## watch_triggers.py
FPT is enabled on the AWS game server.

If you like, you can also enable FPT on your own local server as well, 
but this isn't required.
To do so, edit akk-stack/.env and set ENABLE_FPT_QUESTS to true.
On AWS, I had to open ports 21 and 30000 - 30049.
The ftp username is 'quests', and the PW is found via `make info`.

The AWS game server has a watchdog monitor set which watches for file additions
or changes in the quests/tutorialb directory. Once such a change is detected,
base-story.py is called -- creating the quest in-game.

You can (again not requried) also set up the watchdog service.
In your .venv python virtual environment (akk-stack/Eulogy-Quest/.venv/)
`pip3 install watchdog`. 
This lets you run `akk-stack/Eulogy-Quest/GPT/watch_triggers.py`.

`watch_triggers.py` then calls `base-story.py`.
`base-story.py` makes GPT API calls. To do this locally, you need
a GPT api key stored in a .env file.
Since akk-stack has its own .env, Eulogy-Quest has our own .env at
`akk-stack/Eulogy-Quest/.env`
In our .env, write: OPENAI_API_KEY=
and paste in your key directly after the equals sign.

You can test quest generation without setting up a GPT key or FTP, 
as these are set up on the AWS game server.

You can test the AWS game server quest generation by using curl to ftp
a specially named file for the 'honored_target' of your choice.
You just need the ftp username and password. 
The name (username) is:  quests 
and the pw is:           BU5H9LaaGXe8cUj6SIZI0eXpGeDmVJW

(Although if you want to do this locally, 
 your FTP PW is found using `make info` in the akk-stack/ directory.)

So, if you wanted to see a quest generated in-game on our AWS server
for "Robin Williams":

1. Have the file: Eulogyquest_Robin_Williams.trigger
   created. You can store this wherever, but I'd recommend storing it
   outside the akk-stack directory altogether, like on your Desktop.

2. On your local WSL terminal, and at the directory where your local
   version of the _.target file resides,
   (we're uploading that _.target file now)
   enter the following command (without the surrounding tick-marks):
```
curl --ftp-pasv -T Eulogyquest_Robin_Williams.trigger \
     ftp://quests:BU5H9LaaGXe8cUj6SIZI0eXpGeDmVJW@184.169.160.73/\
tutorialb/Eulogyquest_Robin_Williams.trigger
```

This curl command is what our website will call when we use that interface.

## create-quest.py
The is the master script which runs
- base-story.py
- updateNPCs.py
- perl-script-NPCs.py

This puts the quest in-game on our AWS server.
