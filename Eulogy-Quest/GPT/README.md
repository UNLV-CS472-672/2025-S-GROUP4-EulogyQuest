#Overview:
Quests are automatically generated.
If you want to see a quest generated in-game on our AWS server
for "Robin Williams":
```
curl --ftp-pasv -T Eulogyquest_Robin_Williams.trigger \
     ftp://quests:BU5H9LaaGXe8cUj6SIZI0eXpGeDmVJW@184.169.160.73/\
tutorialb/Eulogyquest_Robin_Williams.trigger
```

#Explanation:

##watch_triggers.py
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

##create-quest.py
The is the master script which runs
- base-story.py
- updateNPCs.py
- perl-script-NPCs.py

This puts the quest in-game on our AWS server.
