#!/bin/bash

set -e

for d in cwl/*/ ; do
    IMAGE=${d/cwl/conglomerate}
    IMAGE=${IMAGE%?};
    docker push ${IMAGE}:latest
done
