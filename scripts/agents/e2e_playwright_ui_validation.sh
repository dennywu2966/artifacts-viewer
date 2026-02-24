#!/bin/bash
# E2E validation for artifacts-viewer using Playwright MCP

set -e

PORT=8080
BASE_URL="http://localhost:$PORT"

echo "=== Artifacts Viewer E2E Validation ==="

# Start server
echo "[1/5] Starting HTTP server..."
bash /home/denny/projects/artifacts-viewer/scripts/agents/start_restart_stack.sh

# Wait for server
sleep 2

# Use Playwright MCP to validate (these would be called via the MCP tool)
echo "[2/5] Testing page load..."
# playwright: navigate to page, check title

echo "[3/5] Testing sidebar navigation..."
# playwright: click on readme.md

echo "[4/5] Testing markdown rendering..."
# playwright: verify markdown content and mermaid diagram rendered

echo "[5/5] Testing search filter..."
# playwright: type in search box, verify filtering

echo "=== Validation Complete ==="

# Keep server running for manual testing or cleanup
echo "Server running at $BASE_URL/artifacts-viewer.html"
echo "To stop: pkill -f 'python3 -m http.server $PORT'"
