#!/bin/bash

set -e

for d in src/pycolocstats/cwl/*/ ; do
    IMAGE=${d/src\/pycolocstats\/cwl/colocstats}
    IMAGE=${IMAGE%?};
    echo Running: push ${IMAGE}:latest
    docker push ${IMAGE}:latest
done
