#!/usr/bin/env bash
# This setup script installs all dependencies and start log servers

set -xe

source .env
./nvidia_patch.sh
apt-get update
apt-get install iproute2 iputils-ping iptables openssl -y
pip3 install -r requirements.txt

echo "Building c++ tests"
./build.sh

if [[ -z "${TEST_HASH}" ]]; then
  echo "ERROR: HASH not found"
  exit
else
  echo "TEST_HASH found."
fi
echo "TEST_HASH: $TEST_HASH"

if [[ -z "${DONT_START_SERVERS}" ]]; then
  echo "Starting log-server and ping-pong server"
  (cd server && python3 log-server/main.py &)
  (cd server && python3 server_ping_pong.py &)
fi

echo "Starting zoro agent"
zoro agent start


sleep 2
echo "Testing that log server is ready..."
curl http://0.0.0.0:8001/logs

# if [[ -z "${WITH_RERUN}" ]]; then
#   echo "Starting pytest without RERUN"
#   #python3 -m pytest -vsx --junitxml=reports/jtest_report.xml client
#   python3 -m pytest -vsx --junitxml=reports/jtest_report.xml client/python_sdk/test_py_sync_2a_basic_produce_messages.py
# else
#   echo "Starting pytest with RERUN"
#   python3 -m pytest --reruns 3 --reruns-delay 1 -vsx client
# fi
# RESULT=$?
#
# echo "Test Complete."
# echo "Test result: $RESULT"
#
# if [[ ! -z "${KILL_SERVERS_ON_TEST_END}" ]]; then
# 	kill -9 `pidof python3 log-server/main.py`
# 	kill -9 `pidof python3 server_ping_pong.py`
# fi
#
# exit $RESULT
