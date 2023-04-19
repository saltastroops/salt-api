#!/bin/bash

# Prepare the docker compose file and output the content of the generated file.

# Replace the ${DOCKER_REGISTRY} and ${TAG} environment variables in the docker
# compose file with the correct values, and save the result to the temporary file.
# Note that the pound sign is used as the delimiter for the first sed pattern, as the
# replacement value (a URL) contains slashes.
registry_pattern='s#${DOCKER_REGISTRY}#'
registry_pattern+="${DOCKER_REGISTRY}#"
sed "$registry_pattern" docker-compose.yml | sed 's/${TAG}/dev/'
