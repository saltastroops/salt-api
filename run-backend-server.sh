#!/bin/bash

# Load the environment variables
set -o allexport
source $BACKEND_ENV_FILE
set +o allexport

cd salt-api

mkdir proposals mapping-tool mapping-tool-log mapping-tool-pipt mapping-tool-proposals finding-charts

# Install Poetry
curl -sSL https://install.python-poetry.org | python3

# Install dependencies
poetry install --no-interaction --no-root

echo "Running the backend server..."

# Run the backend server in the background
poetry run make start &

sleep 1

# Until the backend server is successfully running,
# attempt connecting to it 5 (max_attempts) times
attempt_counter=0
max_attempts=5
until curl -o /dev/null --max-time 30 -s -f --head http://127.0.0.1:8001/docs
do
  if [ ${attempt_counter} -eq ${max_attempts} ];then
      echo "Server not running"
      exit 1
  fi

  attempt_counter=$(($attempt_counter+1))
  echo "Connecting to backend server (attempt ${attempt_counter} of 5)"
  sleep 5
done
