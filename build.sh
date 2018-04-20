#!/bin/bash

set -e

for d in src/cwl/*/ ; do
    IMAGE=${d/src\/cwl/colocstats}
    IMAGE=${IMAGE%?};
    TOOL=${IMAGE/colocstats}
    echo Running: docker build --cache-from ${IMAGE}:latest --tag ${IMAGE}:latest cwl${TOOL}
    docker build --cache-from ${IMAGE}:latest --tag ${IMAGE}:latest cwl${TOOL}
done
