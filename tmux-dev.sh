#!/usr/bin/env bash
SESSION="dairy"
DIR="$(cd "$(dirname "$0")" && pwd)"

tmux kill-session -t "$SESSION" 2>/dev/null
tmux new-session -d -s "$SESSION" -x 220 -y 50
tmux send-keys -t "$SESSION:0" "cd '$DIR' && .venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload 2>&1 | tee /tmp/dairy-server.log" Enter
tmux attach -t "$SESSION"
