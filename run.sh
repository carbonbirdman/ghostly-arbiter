#! /bin/bash
# Runs with the default entrypoint defined in the Dockerfile
IMAGE_NAME=ghostly
IMAGE_TAG=latest
docker run -d -it \
--entrypoint /bin/bash \
--volume /home/$USER/appdata/ghostly:/home/birdman/data \
--volume /home/$USER/ghostly/app:/home/birdman/app \
-p 80:5001 \
--rm \
$IMAGE_NAME:$IMAGE_TAG 
