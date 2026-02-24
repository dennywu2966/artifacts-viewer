#!/bin/bash
# Start/restart HTTP server for artifacts-viewer

PORT=8080

# Kill existing server on port
pkill -f "python3 -m http.server $PORT" 2>/dev/null
sleep 1

# Start new server
cd /home/denny/projects/artifacts-viewer
python3 -m http.server $PORT &
SERVER_PID=$!

echo "Server started on port $PORT (PID: $SERVER_PID)"
sleep 2

# Verify server is running
if curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT/artifacts-viewer.html | grep -q "200"; then
    echo "Server verified: http://localhost:$PORT/artifacts-viewer.html"
else
    echo "ERROR: Server failed to start"
    exit 1
fi
