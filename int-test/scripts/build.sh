#!/usr/bin/env bash

echo "Rebuild Base Image"
docker build -f Dockerfile.base -t int-test-base .
