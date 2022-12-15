#!/usr/bin/env bash
# USAGE ./start_single_docker.sh
# BASH=true ./start_single_docker.sh
export TEST_HASH=`openssl rand -hex 4`
echo "TEST_HASH: $TEST_HASH"

# NETWORK=int-test-network
# docker network inspect $NETWORK >/dev/null 2>&1 || docker network create $NETWORK

echo "Starting up client server"
if [ -z "$GITHUB_ACTION"]  # Don't run with -t if github action
then
  echo "Running with ttyl"
  DOCKER_FLAG="-it"
else
  DOCKER_FLAG="-i"
fi

if [[ -z "${DEBUG}" ]]; then
  docker run $DOCKER_FLAG --cap-add NET_ADMIN -w /work --rm --name single_docker -e TEST_HASH=$TEST_HASH -e WITH_RERUN -v $PWD:/work DOCKER_IMAGE ./entrypoint_single.sh
else
  echo "BASH MODE, with DEBUG=true"
  docker run -it --cap-add NET_ADMIN -w /work --rm --name single_docker -e DEBUG=true -e TEST_HASH=$TEST_HASH -v $PWD:/work DOCKER_IMAGE /bin/bash
fi
