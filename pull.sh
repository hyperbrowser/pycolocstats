#!/bin/bash

set -e

for d in cwl/*/ ; do
    IMAGE=${d/cwl/conglomerate}
    IMAGE=${IMAGE%?};
    echo Running: docker pull ${IMAGE}:latest
    docker pull ${IMAGE}:latest
done
