# File: website/client/Dockerfile
# -----------------------------
# 1) Use a lightweight Node.js image for development
FROM node:16-alpine

# 2) Set working directory
WORKDIR /app

# 3) Copy package manifests and install deps
COPY package.json package-lock.json ./
RUN npm install

# 4) Copy application source
COPY . .

# 5) Expose React dev-server port
EXPOSE 3000

# 6) Start the React development server
CMD ["npm", "start"]
