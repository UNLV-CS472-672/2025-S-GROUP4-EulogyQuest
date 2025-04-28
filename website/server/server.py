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
# api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

app = Flask(__name__)
CORS(app)

# Path where the SPA will read the latest quest JSON
QUEST_FILE = Path(__file__).parents[2] / 'server' / 'quests' / 'last-quest.json'

output_file_name = "before_ai.json"

# /* ai-gen start */
@app.route('/famous-person', methods=['POST'])
def post_famous_person():
    data = request.get_json()
    famous_person = data.get('message') if data else None

    if not famous_person or not famous_person.strip():
        return jsonify({'error': 'Invalid request: "message" field is required and cannot be empty'}), 400

    # Example response for the famous person
    response = {
        'famous_person': famous_person,
        'quest': f"Create a quest inspired by {famous_person}."
    }

    # json file name
    with open(output_file_name, "w") as file:
        json.dump({"famous_person": famous_person}, file)

    # Persist for the SPA
    QUEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(QUEST_FILE, 'w') as f:
        json.dump(response, f, indent=2)

    return jsonify(response), 200
# /* end of ai-get */

@app.route('/honored_one', methods=['POST'])
def post_honored_one():
    data = request.get_json()
    honored_one = data.get('message_name') if data else None
    honored_one_logs = data.get('message_logs') if data else None

    if not honored_one or not honored_one.strip():
        return jsonify({'error': 'Invalid request: "message_name" field is required and cannot be empty'}), 400

    # Example response for the honored one
    response = {
        'honored_one': honored_one,
        'quest': f"Create a quest inspired by {honored_one}."
    }

    # json file name
    with open(output_file_name, "w") as file:
        json.dump({"honored_one": honored_one, "text logs": honored_one_logs}, file)

    # Persist for the SPA
    QUEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(QUEST_FILE, 'w') as f:
        json.dump(response, f, indent=2)

    return jsonify(response), 200

if __name__ == '__main__':
    # Default Flask port is 5000
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("FLASK_RUN_PORT", 5000)),
        debug=True
    )

