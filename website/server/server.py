from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
import ftplib
import io  # <-- you forgot this import in your earlier file

# /* ai-gen start (ChatGPT-4, 2) */
# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__, static_folder='../client/build', static_url_path='/')
CORS(app)

# FTP Configuration (replace with your actual FTP details or load from env)
FTP_SERVER = "your-ftp-server-ip"
FTP_USER = "your-ftp-username"
FTP_PASS = "your-ftp-password"

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

    # --- replicate filename format
    underscored = "_".join(famous_person.split())
    filename = f"Eulogyquest_{underscored}.trigger"
    remote_dir = "tutorialb"

    # --- build file content (could be anything you want, matching your system)
    file_content = f"Quest trigger for {famous_person}"

    try:
        ftp = ftplib.FTP(FTP_SERVER)
        ftp.login(user=FTP_USER, passwd=FTP_PASS)

        # --- change to correct remote directory
        ftp.cwd(remote_dir)

        # --- upload in memory
        with io.BytesIO(file_content.encode('utf-8')) as memfile:
            ftp.storbinary(f'STOR {filename}', memfile)

        ftp.quit()

        return jsonify({
            'famous_person': famous_person,
            'filename_uploaded': f"{remote_dir}/{filename}",
            'status': 'Upload successful'
        }), 200

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
        return jsonify({'error': 'Invalid request: "message_name" field is required and cannot be empty'}), 400

    save_data = {
        "honored_one": honored_one,
        "text_logs": honored_one_logs
    }

    try:
        # Save to local file
        with open(OUTPUT_FILE_NAME, "w") as file:
            json.dump(save_data, file, indent=2)

        # Upload via FTP
        remote_dir = "tutorialb"
        remote_filename = f"Eulogyquest_{'_'.join(honored_one.split())}_honored.trigger"
        
        with open(OUTPUT_FILE_NAME, "rb") as file:
            ftp = ftplib.FTP(FTP_SERVER)
            ftp.login(user=FTP_USER, passwd=FTP_PASS)
            ftp.cwd(remote_dir)
            ftp.storbinary(f"STOR {remote_filename}", file)
            ftp.quit()

        return jsonify({'status': 'success', 'data': save_data, 'ftp_uploaded': f"{remote_dir}/{remote_filename}"}), 200

    except ftplib.all_errors as e:
        print(f"[FTP ERROR] {e}")
        return jsonify({'error': f'FTP Upload failed: {str(e)}'}), 500

    except Exception as e:
        print(f"[SERVER ERROR] {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

# Main entry point for local testing

if __name__ == '__main__':
    app.run(debug=True)
# ai-gen end (ChatGPT-4, 2)