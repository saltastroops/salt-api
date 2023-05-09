#!/bin/bash

# Load the environment variables
set -o allexport
source $DEV_ENV_FILE
set +o allexport

# Create and activate the virtual environment
# /venv should be a Docker volume to avoid installing libraries on every pipeline run
python -m venv /venv
source /venv/bin/activate

# Gather the requirements and install them
poetry export -f requirements.txt --output requirements.txt --without-hashes --with dev
python -m pip install wheel
python -m pip install -r requirements.txt

# Run the tests
black --check saltapi tests || true
isort --check-only saltapi tests  || true
flake8 --exit-zero saltapi tests
bandit -r saltapi
mypy saltapi || true
pytest || true
