#!/bin/bash

echo "Starting ZEO server"

runzeo -a localhost:2709 -f /tmp/storage.fs &

disown


