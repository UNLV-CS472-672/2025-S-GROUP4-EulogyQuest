from flask import Flask, request, jsonify, send_from_directory 
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
from pathlib import Path

load_dotenv()

app = Flask(__name__, static_folder='../client/build', static_url_path='/')

CORS(app)

ftp_server = ""
ftp_user = ""
ftp_pass = ""


# this endpoint only recieves ONE json file, and will overwrite the previous one, the task is next
# we have to get gpt to generate a quest based on the json file we received which should only be 1 file
# endpoint to get a name from famous person route

output_file_name = "before_ai.json"

app.route('/')
def serve_react():
	return send_from_directory(app.static_folder, 'index.html')

def not_found(e):
	return send_from_directory(app.static_folder, 'index.html')

# /* ai-gen start (ChatGPT-4, 2) */
@app.route('/famous-person', methods=['POST'])  
def post_famous_person():
    data = request.get_json()
    famous_person = data.get('message') if data else None

    if not famous_person or not famous_person.strip():
        return jsonify({'error': 'Invalid request: "message" field is required and cannot be empty'}), 400

    # Build filename
    underscored = "_".join(famous_person.split())
    filename = f"Eulogyquest_{underscored}.trigger"
    local_file = Path(filename)

    try:
        # Create the empty trigger file if it doesn't exist
        if not local_file.exists():
            local_file.touch()

        # Build FTP upload URL
        remote_dir = "tutorialb"  # the directory on FTP server
        remote_path = f"{remote_dir}/{filename}"
        url = f"ftp://{ftp_user}:{ftp_pass}@{ftp_server}/{remote_path}"

        # Run curl command to upload
        cmd = [
            "curl",
            "--ftp-pasv",
            "-T", str(local_file),
            url
        ]
        subprocess.run(cmd, check=True)

        response = {
            'famous_person': famous_person,
            'quest': f"Created trigger for {famous_person}."
        }

        return jsonify(response), 200

    except Exception as e:
        print(f"FTP upload error: {e}")
        return jsonify({'error': str(e)}), 500


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
