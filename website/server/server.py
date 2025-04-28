from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
import ftplib
import io  # <-- you forgot this import in your earlier file

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__, static_folder='../client/build', static_url_path='/')
CORS(app)

# FTP Configuration (replace with your actual FTP details or load from env)
FTP_SERVER = os.getenv('FTP_SERVER') or "your-ftp-server-ip"
FTP_USER = os.getenv('FTP_USER') or "your-ftp-username"
FTP_PASS = os.getenv('FTP_PASS') or "your-ftp-password"

# Output file name (used by honored_one route)
OUTPUT_FILE_NAME = "before_ai.json"

# Serve React Frontend
@app.route('/')
def serve_react():
    return send_from_directory(app.static_folder, 'index.html')

# Handle 404 Errors (React SPA fallback)
@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

# Famous Person Endpoint
@app.route('/famous-person', methods=['POST'])
def post_famous_person():
    data = request.get_json()
    famous_person = data.get('message') if data else None

    if not famous_person or not famous_person.strip():
        return jsonify({'error': 'Invalid request: "message" field is required and cannot be empty'}), 400

    response_data = {
        'famous_person': famous_person,
        'quest': f"Create a quest inspired by {famous_person}."
    }

    # Attempt FTP Upload
    try:
        file_content = json.dumps(response_data, indent=2)
        
        ftp = ftplib.FTP(FTP_SERVER)
        ftp.login(user=FTP_USER, passwd=FTP_PASS)

        with io.BytesIO(file_content.encode('utf-8')) as memfile:
            ftp.storbinary('STOR famous_person_quest.json', memfile)

        ftp.quit()

        return jsonify(response_data), 200

    except ftplib.all_errors as e:
        print(f"[FTP ERROR] {e}")
        return jsonify({'error': f'FTP Upload failed: {str(e)}'}), 500

    except Exception as e:
        print(f"[SERVER ERROR] {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

# Honored One Endpoint
@app.route('/honored_one', methods=['POST'])
def post_honored_one():
    data = request.get_json()
    honored_one = data.get('message_name') if data else None
    honored_one_logs = data.get('message_logs') if data else None

    if not honored_one or not honored_one.strip():
        return jsonify({'error': 'Invalid request: "name" field is required and cannot be empty'}), 400

    save_data = {
        "honored_one": honored_one,
        "text_logs": honored_one_logs
    }

    try:
        with open(OUTPUT_FILE_NAME, "w") as file:
            json.dump(save_data, file, indent=2)

        return jsonify({'status': 'success', 'data': save_data}), 200

    except Exception as e:
        print(f"[SERVER ERROR] {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

# Main entry point for local testing
if __name__ == '__main__':
    app.run(debug=True)
