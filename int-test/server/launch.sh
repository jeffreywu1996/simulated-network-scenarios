#!/usr/bin/env bash

set -xe

python3 log-server/main.py &
python3 server_ping_pong.py
