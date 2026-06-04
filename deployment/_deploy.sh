#!/bin/bash

# Usage: ssh user@remote bash -s -- remote_project_dir < _deploy.sh

cd "$1" || { echo "Directory not found: $1" >&2; exit 1; }

if [[ "$(git branch --show-current)" != "main" ]]; then
  echo "The main branch is not checked out." >&2
  exit 1
fi

sha="$(git show --oneline | cut -f 1,1 -d ' ')"
echo "$sha [$(date)]" >> previous_commits.txt

if [[ "$(docker compose ps | wc -l)" -gt 1 ]]; then  # ps always outputs column names
  if ! docker compose down; then
    echo "The Docker container(s) could not be stopped." >&2
    exit 1
  fi
fi

if ! git pull; then
  echo "The latest changes could not be pulled from the git repository." >&2
  exit 1
fi

if ! docker compose up --build -d; then
  echo "The Docker container(s) could not be started." >&2
  exit 1
fi
