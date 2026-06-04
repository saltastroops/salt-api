#!/bin/bash

# Usage: ssh user@remote bash -s -- remote_project_dir < _deploy.sh

handle_error() {
  echo "$1" >&2
  exit 1
}

cd "$1" || handle_error "Directory not found: $1"

if ! [[ -d ".git" ]]; then
  handle_error "No .git directory found in project directory: $1"
fi

if [[ "$(git branch --show-current)" != "main" ]]; then
  handle_error "The main branch is not checked out."
fi

sha="$(git show --oneline | cut -f 1,1 -d ' ')"
echo "$sha [$(date)]" >> previous_commits.txt

if [[ "$(docker compose ps | wc -l)" -gt 1 ]]; then  # ps always outputs column names
  if ! docker compose down; then
    handle_error "The Docker container(s) could not be stopped."
  fi
fi

if ! git pull; then
  handle_error "The latest changes could not be pulled from the git repository."
fi

if ! docker compose up --build -d; then
  handle_error "The Docker container(s) could not be started."
fi
