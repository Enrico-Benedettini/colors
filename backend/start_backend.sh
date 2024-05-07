#!/bin/bash
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

export PORT=3000

nohup python3 backend.py > app.log 2>&1 & echo $! > app.pid
