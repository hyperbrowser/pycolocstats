#!/bin/bash

set -e

for d in src/pycolocstats/cwl/*/ ; do
    IMAGE=${d/src\/pycolocstats\/cwl/colocstats}
    IMAGE=${IMAGE%?};
    TOOL=${IMAGE/colocstats}
    echo Running: docker build --cache-from ${IMAGE}:latest --tag ${IMAGE}:latest src/cwl${TOOL}
    docker build --cache-from ${IMAGE}:latest --tag ${IMAGE}:latest src/pycolocstats/cwl${TOOL}
done
