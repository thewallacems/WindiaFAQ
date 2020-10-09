#!/bin/bash

/home/ubuntu/WindiaFAQ/stop.sh
STATUS=$?
if [ $STATUS == 100 ]; then
  echo "WindiaFAQ not running"
  exit 100
fi

/home/ubuntu/WindiaFAQ/start.sh
exit $?
