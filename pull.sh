#!/bin/bash

set -e

#for d in cwl/*/ ; do
#    IMAGE=${d/cwl/conglomerate}
#    IMAGE=${IMAGE%?};
#    docker pull ${IMAGE}:latest
#done

docker pull conglomerate/stereogene:latest