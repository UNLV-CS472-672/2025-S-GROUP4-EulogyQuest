from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

# TODO : Change output from excel to json
# TODO : present prompt to gpt and get a response in json format

# TODO : multiple endpoints for different models (one for famous person, one for honored one)


# this endpoint only recieves ONE json file, and will overwrite the previous one, the task is next
# we have to get gpt to generate a quest based on the json file we received which should only be 1 file
# endpoint to get a name from famous person route

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
    json_file = "famous_person_before_ai.json"
    with open(json_file, "w") as file:
        json.dump({"famous_person": famous_person}, file)

    return jsonify(response), 200
# /* end of ai-get */




if __name__ == '__main__':
    # Defualt port is 5000
    app.run(debug=True)