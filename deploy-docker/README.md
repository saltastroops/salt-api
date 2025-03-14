# Docker Deployment Guide

This guide provides instructions for deploying the Docker environment for Web Manager using the `deploy-docker` directory.

## Prerequisites

- **Docker**: Ensure Docker is installed. Check by running:
  ```bash
  docker --version
  ```

## Deployment Instructions

### 1. Copy the Contents of the deploy-docker Directory

After updating both the `salt-api` and `web-manager` from `git`. There will be directory in the salt-api directory 
called `deploy-docker`.

Your project structure should look like this: 

```
wm-2022/
├── salt-api/
│   ├── deploy-docker/
│   │   ├── docker-compose.yml
│   │   ├── Dockerfile
│   │   └── other-configuration-files
│   └── salt-api-files
├── web-manager/
    └── web-manager-files

```

You need to copy the content that is inside the `deploy-docker` directory to the `wm-2022`. Also add the `.env` file
with correct environment variables. 

In the end your project structure should look like this:

```
wm-2022/
├── salt-api/
│   ├── deploy-docker/
│   │   ├── docker-compose.yml
│   │   ├── Dockerfile
│   │   └── other-configuration-files
│   └── salt-api-files
├── web-manager/
│   └── web-manager-files
├── .env
├── docker-compose.yml
├── Dockerfile
└── other-configuration-files
```


### 2. Build and Run the Containers

Navigate to the directory where you copied the `deploy-docker`'s content.
From the projects structure you will need to go to the `wm-2022/` directory and run:

```bash
docker compose down
docker compose up --build -d
```
*Make sure that .env file contains correct environment variables*

Then the web manager will be running on port 4201 

