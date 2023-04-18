#!/bin/bash

# Prepare the docker compose file, save it as a temporary file and output the path of
# the generated file.

# Generate a pseudo-unique file path with the current Unix timestamp
tmp_file="/tmp/docker-compose.$(date +%s).yml"

# Replace the ${DOCKER_REGISTRY} and ${TAG} environment variables in the docker
# compose file with the correct values, and save the result to the temporary file
registry_pattern='s/${DOCKER_REGISTRY}/'
registry_pattern+="${DOCKER_REGISTRY}/"
sed "$registry_pattern" docker-compose.yml | sed 's/${TAG}/dev/' > "$tmp_file"

# Output the file path of the temporary file so that it can be used by the Jenkinsfile
echo "$tmp_file"
