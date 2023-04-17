#!/bin/bash

# Load the environment variables
set -o allexport
source $FRONTEND_ENV_FILE
set +o allexport

# Install dependencies
npm ci

# Lint code
npx eslint -c .eslintrc.json

# Check code formatting
npx prettier --check .

# Start frontend server and run Cypress tests
npm run cy:run
