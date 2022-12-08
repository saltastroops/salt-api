# Deploying the Web Manager

The Web Manager is deployed via a GitHub Action workflow, which does the following.

1. It builds the Docker image and pushes it to a container registry.

2. It copies the relevant docker compose file to the deployment server.

3. It powers down the application with docker-compose.

4. It pulls the required version of the required Docker images from the container registry and restarts the application, again using docker-compose.

The deployment server is accessed via a bastion server, which is assumed to be the same for both staging and production deployment.

## Requirements

In the following it is assumed that the bastion server is `bastion.example.com`, the staging server is `staging.example.com` and the production server is `production.example.com`. The users on the bastion, staging and production server are assumed to have the usernames `bastion`, `staging` and `production`, respectively. You will have to replace all these with their real values.

### Creating the SSH keys

In order to connect into the bastion server, and from there into the deployment server, you need to set up SSH keys. We assume that RSA is used.

Let's start on the bastion server and create an SSH key pair.

```shell
ssh bastion@bastion.example.com
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

Do not choose a passphrase. We need to add the generated public key to the list of authorized keys on the bastion, staging and production server. The easiest way to achieve this is to use `ssh-copy-id`.

```shell
ssh-copy-id -i ~/.ssh/id_rsa bastion@bastion.example.com
ssh-copy-id -i ~/.ssh/id_rsa staging@staging.example.com
ssh-copy-id -i ~/.ssh/id_rsa production@production.example.com
```

Finally, view the value of the generated private key.

```shell
cat ~/.ssh/id_pub
```

The value will be stored as a GitHub Actions secret `BASTION_KEY` in the next section.

### nginx server

Nginx must be running on the deployment server, whether it is for staging or for production. This server should generally proxy requests to port 4200, but should proxy requests to endpoints starting with `/api/` to port 8001. This can be achieved with a configuration like the following.

```
location /api/ {
    proxy_pass http://localhost:8000/;
    proxy_set_header Host $http_host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_redirect off;
    proxy_buffering off;
}

location / {
    proxy_pass http://localhost:4200/;
}
```

An SSL certificate needs to be installed on the server, for example vby means of [Certbot](https://certbot.eff.org).

### GitHub 

The following GitHub secrets need to be defined.

| Name                | Description                                   | Example                |
|---------------------|-----------------------------------------------|------------------------|
| BASTION_HOST        | Domain name of the bastion server.            | bastion.example.com    |
| BASTION_KEY         | Private ssh key. See explanation above.       |                        |
| BASTION_USERNAME    | Username of the user on the bastion server.   | bastion                |
| PRODUCTION_HOST     | Domain name of the production server.         | production.example.com |
| PRODUCTION_USERNAME | Username of the user on the production server | production             |
| REGISTRY            | Container registry for the Docker image       | registry.example.com   |
| REGISTRY_PASSWORD   | Password for the container registry           |                        |
| REGISTRY_USERNAME   | Username for the container registry           |                        |
| STAGING_HOST        | Domain name of the staging server.            | staging.example.com    |
| STAGING_USERNAME    | Username of the user on the staging server    | staging                |

###  Bastion server

As described above, you need to create an SSH key and enable password-free logging in to the bastion, staging and production server.

### Staging server

Docker and Docker Compose must be installed.

In addition, the deployment user must be able to use Docker without `sudo`. 

```shell
sudo usermod -aG docker staging
```

### Production server

Docker and Docker Compose must be installed.

In addition, the deployment user must be able to use Docker without `sudo`.

```shell
sudo usermod -aG docker production
```

## Performing the deployment from GitHub

A deployment to the staging server is made whenever changes have been pushed to the development branch.

A deployment to the production server is made whenever a tag is created.
