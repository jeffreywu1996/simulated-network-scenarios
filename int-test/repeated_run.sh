#!/bin/bash

export count=0
while pytest -vsx client
do
    count=$((count+1))
    echo $count
done
