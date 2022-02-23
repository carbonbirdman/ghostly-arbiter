# Run the container and execute the entrypoint script
# cleanup afterwards
#! /bin/bash
IMAGE_NAME=ghostly2
IMAGE_TAG=latest
USER=ac1201
docker run -it \
--entrypoint /bin/bash \
--volume /home/$USER/data/ghostly:/home/birdman/data \
--volume /home/$USER/ghostly/app:/home/birdman/app \
--rm \
$IMAGE_NAME:$IMAGE_TAG 
