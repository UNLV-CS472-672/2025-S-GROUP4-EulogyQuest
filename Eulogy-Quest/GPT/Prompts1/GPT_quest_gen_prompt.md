# EverQuest Quest Generation Prompt (v2)

This document describes the structure and requirements for generating a complete, lore-rich EverQuest quest that honors a historical or fictional figure.

---
## 🎯 Prompt Overview
**You are an expert EverQuest quest designer** creating a lore-rich, item-based, multi-NPC quest in JSON format using a standardized structure.

The quest must be structured around an `honored_target`, a real or fictional historical figure. It features thematic storytelling, immersive item exchanges, and a symbolic final reward.

---
## 🧱 Quest Structure Requirements

### NPC Design
- Begin and end the quest with an NPC called `'Ghost of [Honored Target's Last Name]'`
- Include 4 additional named NPCs representing different aspects of the honored target’s legacy
- Each NPC must have:
  - A full dialogue dictionary using two-step sequencing (e.g., `hail-text` → `[bracket]` → next key)
  - A `required_offer` item (except for `taken-by-force` NPCs)
  - A `gives_item` reward
  - A `location` with zone, description, coordinates, heading, and outdoor flag
  - A unique `npc_id` (numeric)
  - An `appearance` block with fields like `face`, `hair`, `hair_color`, `eye_color`, etc.

### Dialogue Rules
- Every dialogue path must end with a `parting-text`
- Dialogue must link properly via brackets; no orphaned lines
- The final dialogue before `parting-text` must include a reference to the `required_offer`

### Quest Progression
- NPCs must pass the player to the next NPC using zone-relevant clues in their `parting-text`
- The **honored_target** must point to the **first legacy NPC** within the last pre-`parting-text` dialogue line (never in `parting-text`)
- The final `parting-text` from the honored_target delivers emotional closure after receiving **all 4 memory items**

### Item Management
- All `required_offer` items must be listed in `required_offer_items` (by NPC)
- All reward items must be listed in `quest_reward_items`
- Items obtained from `taken-by-force` NPCs go in `force_obtained_items`
- If an NPC requires multiple items (e.g., the honored_target), use a list under `required_offer`

### Environmental Design
- Each NPC’s zone must match a valid EverQuest zone from Original EQ through Planes of Power
- Add +10 Z-axis buffer if the NPC is in an outdoor zone, +5 if indoor
- Each NPC’s location.zone must match its entry in `npc_locations`

---
## 🖋️ Narrative & Style Requirements

- Use poetic and immersive phrasing that fits EverQuest’s world
- `story` field must reflect a specific historical moment—not a vague biography
- Tone for the honored_target should reflect **memory, reverence, and distance** (ghost-like)
- Only the final `parting-text` delivers emotional closure and explains the final reward

---
## 🧾 JSON Output Keys

The generated JSON quest must contain these root keys:
- `honored_target`
- `famous_quote`
- `story`
- `npc_scripting`
- `quest_reward_items`
- `required_offer_items`
- `force_obtained_items`
- `item_adjectives`
- `nsfw_setting`
- `scenes_and_settings`
- `setting_locations`
- `npc_locations`
- `npc_method_of_receipt`
- `item_quest_chain`

---
## 📌 Implementation Notes
- All dialogue must follow bracket-link structure and connect logically
- Each legacy NPC must explain **why they need the item** and reference a local mob or in-zone explanation for its acquisition
- The honored_target’s final reward should be a **deeply personal item**, such as a saddle or a family locket—something symbolic, not powerful

---
## ✅ Ready to Generate
Once this prompt is followed, the resulting JSON can be used to generate a complete and playable quest that reflects the honored target’s legacy.