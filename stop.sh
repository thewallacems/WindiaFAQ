#!/bin/bash

if ! grep -q "windiafaq.py" <<< "$(ps -ef | awk '{print $9}')"; then
  echo "WindiaFAQ not running."
  exit 100
fi

screen -X -S WindiaFAQ quit
echo "WindiaFAQ stopped"
exit 2
