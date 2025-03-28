# EulogyQuest | Custom AI quests honoring the fallen. Based on AkkStack

<img src="Eulogy-Quest/eulogy-docs/EQ-halfling-tombstone.png" alt="Logo" width="300"/>

<p align="center">

[CS-472, Group 4 Github Repo](github.com/UNLV-CS472-672/2025-S-GROUP4-EulogyQuest)

Ken Harvey, Richard Varagson, John Zaleschuk, Jayson Kirchand-Patel, Hardy Fenam, Adam Hamou, Parham Pahlavan, Kevin Ramos, Michael Soffer, & Tanner Donovan

</p>

<p align="center">

# EulogyQuest Description

## Project Overview

This project addresses the lack of a proper in-game recognition that a player has died. Not "Game over, insert coin" died. For real died.
Everquest is one of the founding games of the MMORPG genre, and there is an open-source community which maintains the ability to make your own Everquest worlds, run on your own server, with your own rules. This community is EQEmu. It is here that we'll implement a proper "eulogy" in the form of an 'on-the-fly' (some call it 'dynamic') generation of a static quest.

EulogyQuest will allow a user (who perhaps has just lost a friend) to automatically create an in-game quest which pays tribute to the fallen. The user will input enough information (text files and such) for ChatGPT to make a fitting quest which illustrates relevant details about the fallen. The quest will result in an in-game item which will summon a translucent version of the fallen. Those wishing to "pay their respects" will be able to perform this quest as well, and with the same reward.

Perhaps the hesitant user would first like to test this? They simply supply the name of a famous deceased person (perhaps a dead president). Hopefully the hesitant user appreciates the journey, and is thereby encouraged to provide real data (text) to get a personalized quest of their own fallen.

## Setup & Installation

- [Local Game Server Install Guide](Eulogy-Quest/eulogy-docs/Eulogy-quest%20development%20guide_v3.pdf)
- [Issue Triage and Initial NPC changes](Eulogy-Quest/eulogy-docs/Issue%20Triage%20-%20EulogyQuest.pdf)
- [Persistent NPC Guide](Eulogy-Quest/eulogy-docs/Permanent%20NPC%20How%20to.pdf)


## Technology Stack

This project is based on [EQEmu](https://eqemulator.org), specifically with the [Akk-stack project](https://docs.eqemu.io/akk-stack/introduction/).
The quests are created by the addition or change to a perl or lua file for the associated NPC.
NPCs (Non Player Characters) are created as database entries.
Cloning Akk-stack, you inherit his server management system, which is a docker-compose environment with a game server, database server, lua/perl server runtimes, php server, ftp server, custom shells, and the Web-admin server.

## Deployment Instructions for the End User

While you *could* use the Setup & Installation instruction PDFs above to test our work, we will need to simplify this in another short tutorial. Soon we'll have the public Eulogyquest server (on AWS) set up to generate our on-demand quests. Until then, you'd follow the instructions in the Setup & Installation section above, but only to setup the client. Make sure your eqhost.txt file points to the public eqemulator login server (`Host=login.projecteq.net:5999`). This will allow you to play on our public server. I *do* however keep this server offline most of the time, but will probably soon keep it on as a CI/CD test environment.

</p>

# And now a word from our sponsor.. err.. **open-source upstream**
## AkkStack | Containerized EverQuest Emulator Server Environment

<p align="center">
 
<img src="https://github.com/Akkadius/akk-stack/assets/3319450/d276736b-622a-4bd6-a9eb-c9fdc48b3259" alt="AkkStack">

AkkStack is a simple Docker Compose environment that is augmented with developer and operator focused tooling for running EverQuest Emulator servers

You can have an entire server running within minutes, configured and ready to go for development or production use

**The README for this project has gotten far too large, we have moved to a** [dedicated documentation space within the EverQuest Emulator Docs](https://docs.eqemu.io/akk-stack/introduction/)

</p>

## Feature Requests

Want a feature that isn't already available? Open an issue with the title "[Feature Request]" and we will see about getting it added

## Contributing

If you want to contribute to the repo, please submit **Pull Requests**

## Pay it Forward

If you decide to utilize this repository, know that it's built on a lot of effort I've put in to ensure it's super easy for you to enjoy for free. I kindly ask that you consider giving back to the community by contributing in any way you can. Let's keep the spirit of collaboration alive!
