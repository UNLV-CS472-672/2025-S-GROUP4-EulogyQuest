from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

EXCEL_FILE = "prompts.xlsx"

@app.route('/prompt', methods=['POST'])
def receive_prompt():
    data = request.get_json()
    # check if message is present in the request
    message = data.get('message') if data else None
    # check if message is not empty
    if not message or not message.strip():
        return jsonify({'error': 'Invalid request: "message" field is required and cannot be empty'}), 400

    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Load existing file or create new DataFrame
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
    else:
        df = pd.DataFrame(columns=["Timestamp", "Prompt"])

    # Append new row
    df = pd.concat([df, pd.DataFrame([{"Timestamp": timestamp, "Prompt": message}])], ignore_index=True)

    # Save back to Excel
    df.to_excel(EXCEL_FILE, index=False)

    return jsonify({'received': message, 'status': 'Message saved to Excel'}), 200


if __name__ == '__main__':
    # Defualt port is 5000
    app.run(debug=True)
