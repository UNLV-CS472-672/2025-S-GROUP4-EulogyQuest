# File: website/server/Dockerfile
# -----------------------------
# 1) Use a minimal Python base image
FROM python:3.9-slim

# 2) Set working directory
WORKDIR /app

# 3) Copy and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copy application code
COPY . .

# 5) Expose Flask default port
EXPOSE 5000

# 6) Launch the Flask server
CMD ["flask", "run", "--host=0.0.0.0"]