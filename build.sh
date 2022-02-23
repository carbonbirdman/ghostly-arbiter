#! /bin/bash
IMAGE_NAME=ghostly2
IMAGE_TAG=latest
docker build --file Dockerfile  --tag $IMAGE_NAME:$IMAGE_TAG .
