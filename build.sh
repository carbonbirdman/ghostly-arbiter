#! /bin/bash
IMAGE_NAME=ghostly
IMAGE_TAG=latest
docker build --file Dockerfile  --tag $IMAGE_NAME:$IMAGE_TAG .
