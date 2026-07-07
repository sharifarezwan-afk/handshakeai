#!/bin/bash
set -euo pipefail

pytest /tests/test_outputs.py -rA --ctrf /tmp/ctrf.json
status=$?

if [ "$status" -eq 0 ]; then
  echo 1 > /tmp/reward.txt
else
  echo 0 > /tmp/reward.txt
fi

exit "$status"