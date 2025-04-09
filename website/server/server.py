from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os
import json
from openai import OpenAI

load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = os.getenv("OPEN_API_KEY"))

app = Flask(__name__)
CORS(app)

# TODO : Change output from excel to json
# TODO : present prompt to gpt and get a response in json format

# TODO : multiple endpoints for different models (one for famous person, one for honored one)


# this endpoint only recieves ONE json file, and will overwrite the previous one, the task is next
# we have to get gpt to generate a quest based on the json file we received which should only be 1 file
# endpoint to get a name from famous person route

output_file_name = "before_ai.json"

# /* ai-gen start (ChatGPT-4, 2) */
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


    # build GPT prompt
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
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative quest designer for the fantasy MMORPG game EverQuest."},
                {"role": "user", "content": prompt}
            ],
            temperature = 0.7,
            max_tokens = 600
        )

        quest_text = response.choices[0].message.content.strip()

        # save input and generated quest
        json_data = {
            "famous_person": famous_person,
            "quest": quest_text
        }

        with open("famous_person_with_ai.json", "w") as file:
            json.dump(json_data, file, indent=2)

        return jsonify(json_data), 200

    except Exception as e:
        print(f"OpenAI API error: {e}")
        return jsonify({'error': str(e)}), 500


    return jsonify(response), 200   

# /* end of ai-get */

@app.route('/honored_one', methods=['POST'])  
def post_honored_one():
    data = request.get_json()
    honored_one = data.get('message_name') if data else None
    honored_one_logs = data.get('message_logs') if data else None

    if not honored_one or not honored_one.strip():
        return jsonify({'error': 'Invalid request: "name" field is required and cannot be empty'}), 400

    # Example response for the honored one
    response = {
        'honored_one': honored_one,
        'quest': f"Create a quest inspired by {honored_one}."
    }

    # json file name
    with open(output_file_name, "w") as file:
        json.dump({"honored_one": honored_one, "text logs":honored_one_logs}, file)
        

    return jsonify(response), 200


if __name__ == '__main__':
    # Defualt port is 5000
    app.run(debug=True)
