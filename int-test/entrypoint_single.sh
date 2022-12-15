#!/usr/bin/env bash
# This is entry point file used by start_single_docker.sh and Jenkins for sdk

#DONT_START_SERVERS=true         # Dont start logging/pingpong server
#KILL_SERVERS_ON_TEST_END=true   # Kill log-server/ping-pong-server on test end. Set to true for debug
#WITH_RERUN=true                 # Set to true if want to run pytest with rerun
# NO_INSTALL=true


if [[ ! -z "${DEBUG}" ]]; then  # If DEBUG flag is set
  echo "DEBUG Mode"
  unset DONT_START_SERVERS
  KILL_SERVERS_ON_TEST_END=true
fi


set -xe

source .env
./nvidia_patch.sh
if [[ -z "${NO_INSTALL}" ]]; then  # If NO_INSTALL is not set
  echo "Installing sdk"
else
  echo "Skip installing sdk (prebuilt)"
fi
apt-get update
apt-get install iproute2 iputils-ping iptables openssl -y
pip3 install -r requirements.txt

echo "Building c++ tests"
./build.sh

if [[ -z "${TEST_HASH}" ]]; then
  echo "Generating TEST_HASH..."
  export TEST_HASH=`openssl rand -hex 4`
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

PYTEST_FLAGS="-vsx --junitxml=reports/jtest_report.xml"
PYTEST_TESTS="client/"
if [[ -z "${WITH_RERUN}" ]]; then
  echo "Starting pytest without RERUN"
  python3 -m pytest $PYTEST_FLAGS $PYTEST_TESTS
  RESULT=$?
else
  echo "Starting pytest with RERUN"
  python3 -m pytest --reruns 3 --reruns-delay 1 $PYTEST_FLAGS $PYTEST_TESTS
  RESULT=$?
fi

echo "Test Complete."
echo "Test result: $RESULT"

if [[ ! -z "${KILL_SERVERS_ON_TEST_END}" ]]; then
	kill -9 `pidof python3 log-server/main.py`
	kill -9 `pidof python3 server_ping_pong.py`
fi

exit $RESULT
