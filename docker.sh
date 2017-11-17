#!/bin/bash

set -e

docker login -u $DOCKER_USER -p $DOCKER_PASSWORD

for d in cwl/*/ ; do
    IMAGE=${d/cwl/conglomerate}
    IMAGE=${IMAGE%?};
    TOOL=${IMAGE/conglomerate}
    docker pull ${IMAGE}:latest
    docker build --cache-from ${IMAGE}:latest --tag ${IMAGE}:latest cwl${TOOL}
    docker push ${IMAGE}:latest
done
