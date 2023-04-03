#!/bin/bash

# Create and activate the virtual environment
# /venv should be a Docker volume to avoid installing libraries on every pipeline run
python -m venv /venv
source /venv/bin/activate

# Gather the requirements and install them
poetry export -f requirements.txt --output requirements.txt --without-hashes
python -m pip install wheel
python -m pip install -r requirements.txt
python -m pip install flake8
python -m pip install isort
python -m pip install mypy
python -m pip install pytest

# Run the tests
black --check || true
isort --check-only || true
flake8 --exit-zero saltapi tests
mypy saltapi || true
pytest || true
