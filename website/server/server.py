from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os
import json
from openai import OpenAI
from pathlib import Path

# Load .env and initialize OpenAI client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

app = Flask(__name__)
CORS(app)

# Path where the SPA will read the latest quest JSON
QUEST_FILE = Path(__file__).parents[2] / 'server' / 'quests' / 'last-quest.json'


@app.route('/famous-person', methods=['POST'])
def post_famous_person():
    data = request.get_json()
    famous_person = data.get('message') if data else None

    if not famous_person or not famous_person.strip():
        return jsonify({'error': 'Invalid request: "message" field is required'}), 400

    # Build GPT prompt
    prompt = f"""
    Create a fun, emotionally meaningful EverQuest-style quest inspired by {famous_person}.
    The quest should have:
      - A title
      - A brief description of why it's meaningful
      - 3-5 objectives the player must complete
      - A quest reward

    Format the output in structured JSON like this:
    {{
      "title": "...",
      "description": "...",
      "objectives": ["...", "..."],
      "reward": "..."
    }}
    """

    try:
        ai_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a creative quest designer for the fantasy MMORPG game EverQuest."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )

        quest_json = json.loads(ai_response.choices[0].message.content)

        # Persist for the SPA
        QUEST_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(QUEST_FILE, 'w') as f:
            json.dump(quest_json, f, indent=2)

        return jsonify(quest_json), 200

    except Exception as e:
        print(f"OpenAI API error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/honored_one', methods=['POST'])
def post_honored_one():
    data = request.get_json()
    honored_one = data.get('message_name') if data else None
    message_logs = data.get('message_logs') if data else None

    if not honored_one or not honored_one.strip():
        return jsonify({'error': 'Invalid request: "message_name" field is required'}), 400

    # Simple example quest; replace with your GPT logic as needed
    quest_json = {
        "title": f"Honoring {honored_one}",
        "description": f"A special quest to honor {honored_one} through remembrance.",
        "objectives": ["Collect personal stories", "Compose the tribute", "Share it with the community"],
        "reward": "Memories and respect"
    }

    # Persist for the SPA
    QUEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(QUEST_FILE, 'w') as f:
        json.dump(quest_json, f, indent=2)

    return jsonify(quest_json), 200


if __name__ == '__main__':
    # Default Flask port is 5000
    app.run(host="0.0.0.0", port=int(os.getenv("FLASK_RUN_PORT", 5000)), debug=True)
