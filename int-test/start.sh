#!/usr/bin/env bash
# DEBUG mode: will go into /bin/bash instead of running tests
# DEBUG=true ./start.sh

export TEST_HASH=`openssl rand -hex 4`
echo "TEST_HASH: $TEST_HASH"

NETWORK=int-test-network
docker network inspect $NETWORK >/dev/null 2>&1 || docker network create $NETWORK

echo "Starting up client server"
docker-compose -f docker-compose.dev.yml up --build --abort-on-container-exit
