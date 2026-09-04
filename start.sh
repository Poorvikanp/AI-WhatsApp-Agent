#!/bin/bash
set -e

echo "Starting FastAPI backend..."
uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "Waiting for backend to be ready..."
sleep 5

echo "Starting WhatsApp client..."
node wa_client.js &
WA_PID=$!

echo "Both processes started. Forwarding signals..."

# Forward signals to both children
trap "kill -TERM $BACKEND_PID $WA_PID" SIGTERM
trap "kill -INT $BACKEND_PID $WA_PID" SIGINT

# Wait for either process to exit
wait -n

# Kill the other process
kill -TERM $BACKEND_PID $WA_PID 2>/dev/null || true
wait
