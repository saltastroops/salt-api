# Deployment to a development server

Running the Jenkinsfile requires ssh credentials, a secret file, and some environment variables.

## SSH credentials

You need to add the SSH credentials for the development server in the Jenkins settings for credentials (Dashboard > Manage Jenkins > Manage Credentials). The credentials id must be `salt-api-dev-server-credentials`. You need to supply a private key (rather than a password) when adding the credentials.

## Secret file

You need to add a secret file with the environment variables needed by the API server in the Jenkins ection for credentials (Dashboard > Manage Jenkins > Manage Credentials). The credentials id must be `salt-api-dev-env`. Note that the environment variables in this file are different from those covered in the following section.

## Environment variables

The following environment variables need to be defined. You can set them under Dashboard > Manage Jenkins > Configure System in the section "Global properties".

| Variable          | Description                                             | Example                      |
|-------------------|---------------------------------------------------------|------------------------------|
| DOCKER_REGISTRY   | URL of the Docker registry for hosting the Docker image | https://registry.example.com |
| SALT_API_DEV_HOST | Hostname of the SALT  API development server            | api.example.com              |


