#!/usr/bin/env bash

set -xe

./build.sh

if [[ ! -z "${DEBUG}" ]]; then  # If DEBUG flag is set
  set +x
  echo "DEBUG Mode. Will not auto run tests"
  echo "Please open new terminal"
  echo "docker exec -it client /bin/bash"
  echo "Start test with: python3 -m pytest -vsx client"
  sleep 10000000h
else
  if [[ ! -z "${WITH_RERUN}" ]]; then
    echo "Starting tests with RERUN"
    python3 -m pytest -vvsx --reruns 2 --reruns-delay 1 client
  else
    echo "Starting tests"
    python3 -m pytest -vvsx client
  fi
  # python3 -m pytest -vsx client/test_stable.py
fi
