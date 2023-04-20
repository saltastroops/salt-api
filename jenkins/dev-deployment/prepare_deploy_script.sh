#!/bin/bash

# Prepare the script for deploying, replacing the environment variables for the Docker
# registry user and URL. The updated script content is output to stdout, so that it can
# be used in the Jenkinsfile.

# Note that the pound sign is used as the delimiter for the first sed pattern, as the
# replacement value (a URL) contains slashes.
registry_pattern='s#${DOCKER_REGISTRY}#'
registry_pattern+="${DOCKER_REGISTRY}#"
username_pattern='s/${DOCKER_REGISTRY_USERNAME}/'
username_pattern+="${REGISTRY_CREDENTIALS_USR}/"
cat jenkins/dev-deployment/deploy.sh | sed "$registry_pattern" | sed "$username_pattern"
