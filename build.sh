#!/bin/bash

set -e

for d in cwl/*/ ; do
    IMAGE=${d/cwl/colocstats}
    IMAGE=${IMAGE%?};
    TOOL=${IMAGE/colocstats}
    echo Running: docker build --cache-from ${IMAGE}:latest --tag ${IMAGE}:latest cwl${TOOL}
    docker build --cache-from ${IMAGE}:latest --tag ${IMAGE}:latest cwl${TOOL}
done
