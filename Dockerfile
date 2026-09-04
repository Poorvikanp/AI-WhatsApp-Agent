FROM python:3.11-slim

# Install Node.js 20
RUN apt-get update && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Node dependencies
COPY package.json package-lock.json* ./
RUN npm install --production

# Copy application code
COPY . .

# Environment
ENV NODE_ENV=production
ENV PYTHONUNBUFFERED=1

# Render Background Worker entrypoint
CMD ["bash", "start.sh"]
