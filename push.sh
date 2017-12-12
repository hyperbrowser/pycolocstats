#!/bin/bash

set -e

for d in cwl/*/ ; do
    IMAGE=${d/cwl/conglomerate}
    IMAGE=${IMAGE%?};
    echo Running: push ${IMAGE}:latest
    docker push ${IMAGE}:latest
done
