#!/bin/bash

echo "Checking redis..."
if [ "$(redis-cli ping)" != "PONG" ]; then
    echo "Redis not running. Starting"
    screen -d -m -S redis bash -c 'redis-server'
    sleep .2
fi

if [ "$(redis-cli ping)" != "PONG" ]; then
    echo "Redis failed to start. Aborting..."
    exit 1;
else
    echo "OK"
fi