from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime
import os
import json

app = Flask(__name__)
CORS(app)

# TODO : Change output from excel to json
# TODO : present prompt to gpt and get a response in json format

EXCEL_FILE = "prompts.xlsx"

# TODO : multiple endpoints for different models (one for famous person, one for honored one)


# this endpoint only recieves ONE json file, and will overwrite the previous one, the task is next
# we have to get gpt to generate a quest based on the json file we received which should only be 1 file
# endpoint to get a name from famous person route
@app.route('/famous-person', methods=['POST'])  # changed from GET to POST
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


# ____________this endpoint is no longer needed will keep here for reference ____________#
# @app.route('/prompt', methods=['POST'])
# def receive_prompt():
#     data = request.get_json()
#     # check if message is present in the request
#     message = data.get('message') if data else None
#     # check if message is not empty
#     if not message or not message.strip():
#         return jsonify({'error': 'Invalid request: "message" field is required and cannot be empty'}), 400

#     # Get current timestamp
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     # Load existing file or create new DataFrame
#     if os.path.exists(EXCEL_FILE):
#         df = pd.read_excel(EXCEL_FILE)
#     else:
#         df = pd.DataFrame(columns=["Timestamp", "Prompt"])

#     # Append new row
#     df = pd.concat([df, pd.DataFrame([{"Timestamp": timestamp, "Prompt": message}])], ignore_index=True)

#     # Save back to Excel
#     df.to_excel(EXCEL_FILE, index=False)

#     return jsonify({'received': message, 'status': 'Message saved to Excel'}), 200


if __name__ == '__main__':
    # Defualt port is 5000
    app.run(debug=True)
