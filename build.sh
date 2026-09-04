#!/bin/bash
set -e

# Install Node.js via NodeSource
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies
npm install --production

echo "Build complete"
