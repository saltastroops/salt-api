#!/bin/bash

# Prepare the docker compose file and output the content of the generated file.

# The docker registry variable should have an "https://" or "http://" prefix, but this
# must not be included in the pushed image name.
registry=$(echo ${DOCKER_REGISTRY} | sed s#https://## | sed s#http://##)

# Replace the ${DOCKER_REGISTRY}, ${DOCKER_REGISTRY_USERNAME} and ${TAG} environment
# variables in the docker compose file with the correct values, and output the result to
# stdout.
# Note that the pound sign is used as the delimiter for the first sed pattern, as the
# replacement value (a URL) contains slashes.
registry_pattern='s#${DOCKER_REGISTRY}#'
registry_pattern+="${registry}#"
username_pattern='s/${DOCKER_REGISTRY_USERNAME}/'
username_pattern+="${REGISTRY_CREDENTIALS_USR}/"
sed "$registry_pattern" docker-compose.yml | sed "$username_pattern" | sed 's/${TAG}/dev/'
