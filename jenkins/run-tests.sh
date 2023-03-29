#!/bin/bash

# Create and activate the virtual environment
# /venv should be a Docker volume to avoid installing libraries on every pipeline run
python -m venv /venv
source /venv/bin/activate

# Gather the requirements and install them
poetry export -f requirements.txt --output requirements.txt --without-hashes
python -m pip install -r requirements.txt

# Run the tests
flake8 --exit-zero saltapi tests
mypy saltapi
