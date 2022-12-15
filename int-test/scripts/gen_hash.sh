#!/usr/bin/env bash

set -o allexport
export TEST_HASH=`openssl rand -hex 4`                                                                                                                                                                         
set +o allexport
echo "TEST_HASH: $TEST_HASH"
