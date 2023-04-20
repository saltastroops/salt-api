#!/bin/bash

# Pull the latest docker image and restart the service defined in the docker compose
# file.

cd salt-api

# Log into the docker registry
cat registry-password.txt | docker login -u ${DOCKER_REGISTRY_USERNAME} ${DOCKER_REGISTRY}

# Pull the docker image for the service, but don't restart the service
docker compose pull saltapi

# Restart the service
docker compose down || true
docker compose up -d

# Clean up
docker image prune

