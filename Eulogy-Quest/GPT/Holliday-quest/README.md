// ai-gen start (ChatGPT-4.5, 0)

Here’s a clear summary of the extracted directory structure:

```
Holliday-quest/
├── README.txt
├── tree.txt
├── Note-from-the-author.txt
├── Holliday-working.png
├── src/
│   ├── README.txt
│   ├── .quest_generation_master_prompt.json.swp
│   ├── sql/
│   │   ├── honored_target_implementation.json
│   │   ├── README.txt
│   │   ├── .basic_honored_target_implementation.json.swp
│   │   ├── basic_honored_target_implementation.json
│   │   ├── npc-db-lookup.png
│   │   └── sql_prompt.json
│   ├── perl/
│   │   ├── README.txt
│   │   ├── Unterminated-string-literal-fix.png
│   │   ├── doc_holliday_quest.json
│   │   └── dialogue_loader.py
│   └── quest/
│       ├── quest_generation_wrapper.json
│       ├── GPT_quest_gen_prompt.json
│       ├── quest_generation_master_prompt.json
│       ├── README.txt
│       └── dialogue_structure.json
└── build/
    ├── README.txt
    ├── sql/
    │   ├── doc_holliday_implementation.sql
    │   ├── README.txt
    │   └── doc_holliday_implementation.json
    ├── perl/
    │   ├── Sylas.pl
    │   ├── Pastor.pl
    │   ├── Mister.pl
    │   ├── README.txt
    │   ├── Hollidays.pl
    │   └── Ada.pl
    └── quest/
        ├── README.txt
        └── doc_holliday_quest.json
```

Here's a clear summary of the project based on your provided `README.txt` files:

---

# 🎯 Project Overview: "Holliday Quest" (Eulogy-Quest Series)

## 📌 High-Level Summary:
The Holliday Quest is part of the broader "Eulogy-Quest" series. It involves generating structured, interactive NPC-driven quests for EverQuest, specifically tailored for EQEmu servers (EverQuest emulation servers). Each quest involves a chain of interactions between the player and multiple NPCs, involving dialogue exchanges, item retrieval tasks, and ultimately rewarding players upon completion.

---

## 📂 Directory Structure and Roles:

The project structure is organized primarily into two key directories:  
- **`src/`**: Source files and master prompts for quest generation.
- **`build/`**: Output from the quest generation process, ready-to-use implementation files.

---

## 🔧 `src/` Directory Details:
The source (`src/`) directory contains the components necessary to prompt ChatGPT for generating quests and their implementation:

### 📌 Quest (`src/quest`):
- `GPT_quest_gen_prompt.json`: Instructions to ChatGPT on how to generate a structured, JSON-formatted EverQuest quest.
- `dialogue_structure.json`: Guidelines for structuring NPC dialogues.
- `quest_generation_wrapper.json`: Wrapper to ensure consistent generation and naming of quests.
- Master prompt (`quest_generation_master_prompt.json`): Consolidated instructions used for consistent quest prompting.

### 📌 SQL (`src/sql`):
- Contains JSON templates (`honored_target_implementation.json`, `basic_honored_target_implementation.json`) for generating SQL insert commands. 
- `sql_prompt.json`: Converts the JSON-generated commands into ready-to-use SQL scripts.
- Offers both "debug" and "production" modes for NPC placement.

### 📌 Perl (`src/perl`):
- `dialogue_loader.py`: Python script to automatically generate Perl scripts from quest JSON files.
- Perl scripts provide NPC dialogues and in-game interaction logic.

---

## 🚀 `build/` Directory Details:
The build (`build/`) directory contains generated outputs from the quest-generation prompts, ready for deployment in EQEmu environments:

### 📌 Quest (`build/quest`):
- `doc_holliday_quest.json`: The JSON-structured quest detailing NPC interactions, dialogues, and item tasks.

### 📌 SQL (`build/sql`):
- SQL implementation files (`doc_holliday_implementation.json`, `doc_holliday_implementation.sql`) which insert the generated NPCs into the game database.
- Supports iteration through safe SQL insertion and updates.

### 📌 Perl (`build/perl`):
- Perl scripts (`Ada.pl`, `Hollidays.pl`, `Mister.pl`, `Pastor.pl`, `Sylas.pl`) which script NPC behavior, dialogue interactions, and quest logic.
- Scripts handle player interactions, dialogues, item exchanges, and rewards.

---

## 🗃️ Workflow and File Relationships:

**Step 1: Quest Generation**  
- Use ChatGPT with files from `src/quest/` to generate `doc_holliday_quest.json`.

**Step 2: NPC Database Insertions**  
- Generate SQL implementation files (`build/sql/`) using `doc_holliday_quest.json` and templates from `src/sql/`.

**Step 3: NPC Interaction Logic**  
- Run `dialogue_loader.py` (from `src/perl`) to automatically generate NPC Perl scripts (`build/perl/`) based on `doc_holliday_quest.json`.

---

## 📖 Explanation of Quest Flow:
- A player initiates the quest by interacting with the initial NPC ("Hollidays ghost").
- Sequentially interacts with 4 additional NPCs, each requiring item retrieval from mobs.
- Dialogue interactions involve clickable texts driving the story forward.
- The quest concludes by returning to the original NPC, exchanging collected items for rewards.

---

## 🎲 Intended Gameplay Experience:
- Immersive narrative experiences driven by carefully scripted NPC interactions.
- Structured, consistent, and dynamically generated quests that enrich the EverQuest world.
- Player engagement through exploration, combat, item recovery, and storytelling.

---

// ai-gen end