#!/bin/bash

if grep -q "main.py" <<< "$(ps -ef | awk '{print $9}')"; then
  echo "WindiaFAQ already running. Please terminate the running WindiaFAQ process before running a new one."
  exit 101
else
  echo "Starting main.py"
fi

cd ~

if ! [[ -d /home/ubuntu/WindiaFAQ ]]; then
  echo "Cloning WindiaFAQ files..."
  git clone https://github.com/thewallacems/WindiaFAQ.git
  echo "WindiaFAQ files cloned."
fi

cd WindiaFAQ

if ! [[ -f /home/ubuntu/WindiaFAQ/main.py ]]; then
  echo "main.py not found. Fixing install of WindiaFAQ."
  cd ~
  rm -rf WindiaFAQ
  git clone https://github.com/thewallacems/WindiaFAQ.git
  cd WindiaFAQ
fi

UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

if [ $LOCAL == $BASE ]; then
    echo "Updating WindiaFAQ..."
    git pull
    echo "WindiaFAQ updated"
elif [ $REMOTE = $BASE ]; then
    echo "There are local changes in WindiaFAQ that must be pushed before starting"
    echo "Please review these changes before attempting to start"
    exit 102
fi

python3.8 -m pip install -U pip

if [[ -f /home/ubuntu/WindiaFAQ/requirements.txt ]]; then
  python3.8 -m pip install -r ~/WindiaFAQ/requirements.txt
fi

if grep -q "WindiaFAQ" <<< "$(screen -list)"; then
  echo "Closing existing WindiaFAQ screen"
  screen -X -S WindiaFAQ quit
fi

screen -d -m -S WindiaFAQ bash -c "python3.8 /home/ubuntu/WindiaFAQ/main.py"
echo "WindiaFAQ started"
exit 0
