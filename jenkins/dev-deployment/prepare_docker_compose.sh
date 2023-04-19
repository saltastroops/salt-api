#!/bin/bash

# Prepare the docker compose file and output the content of the generated file.

# The docker registry variable should have an "https://" or "http://" prefix, but this
# must not be included in the pushed image name.
registry=$(echo "http://aaa" | sed s#https://## | sed s#http://##)

# Replace the ${DOCKER_REGISTRY} and ${TAG} environment variables in the docker
# compose file with the correct values, and save the result to the temporary file.
# Note that the pound sign is used as the delimiter for the first sed pattern, as the
# replacement value (a URL) contains slashes.
registry_pattern='s#${DOCKER_REGISTRY}#'
registry_pattern+="${registry}#"
sed "$registry_pattern" docker-compose.yml | sed 's/${TAG}/dev/'
