ssh ssda@ssdadev "cd webmanager/frontend; git checkout development; git pull; docker-compose down; docker-compose up --build -d"
