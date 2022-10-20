# Deploying the Web Manager

The Web Manager is deployed using docker compose. The  docker compose require some environment variables to set on the `.env` file.

### `.env` file content

| Variable name | Description                                  | Example                                     |
|---------------|----------------------------------------------|---------------------------------------------|
| PORT          | The port you want the Web Manager to run on. | 4200                                        |
| RUN_MODE      | The mode of deployment you are making        | Either: development, staging, or production |

### Deploying the application
Run
```bash
docker compose down
docker compose up --build
```

If ever the docker image exists you can run
```bash
docker compose up
```

Now your application will be available on `http://server-name:${PORT}`


