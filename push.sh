#!/bin/bash

set -e

for d in cwl/*/ ; do
    IMAGE=${d/cwl/colocstats}
    IMAGE=${IMAGE%?};
    echo Running: push ${IMAGE}:latest
    docker push ${IMAGE}:latest
done
