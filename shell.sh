# Run the container and execute the entrypoint script
# cleanup afterwards
#! /bin/bash
IMAGE_NAME=ghostly
IMAGE_TAG=latest
USER=user
docker run -it \
--entrypoint /bin/bash \
--volume /home/$USER/appdata/ghostly:/home/birdman/data \
--volume /home/$USER/ghostly/app:/home/birdman/app \
--rm \
$IMAGE_NAME:$IMAGE_TAG 
