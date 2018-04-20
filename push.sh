#!/bin/bash

set -e

for d in src/cwl/*/ ; do
    IMAGE=${d/src\/cwl/colocstats}
    IMAGE=${IMAGE%?};
    echo Running: push ${IMAGE}:latest
    docker push ${IMAGE}:latest
done
