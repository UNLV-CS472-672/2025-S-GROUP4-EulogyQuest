Dependencies
react, react-dom, Flask, react-router-dom, axios, pandas

Install:
npm install react react-dom react-router-dom axios
pip install flask pandas flask_cors openpyxl python-dotenv(on a virtual enviroment)

### GPT Backend Setup

1. Create a virtual environment: 
python3 -m venv venv
source venv/bin/activate

2. Install dependencies

3. Create a .env file in website/server/ directory and add the OpenAI API key:
OPENAPI_API_KEY=sk-xxxxxxxxxxxxxxxxxx

NOTE: Do not commit the .env file! (Should already be included in the .gitignore)
