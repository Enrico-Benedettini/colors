#!/bin/bash
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

if [[ -f 'app.pid' ]]; then
    kill -9 $(cat app.pid)
    rm app.pid
fi
