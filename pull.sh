#!/bin/bash

#set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
USE_TEST_DOCKER_IMAGES=$(/usr/bin/env python -c "from __future__ import print_function; import sys; sys.path += ['$DIR/conglomerate']; from core.config import USE_TEST_DOCKER_IMAGES; print(USE_TEST_DOCKER_IMAGES)")

if [[ "$USE_TEST_DOCKER_IMAGES" == "True" ]]; then
    TEST_IMAGES=cwl/*_test/
    echo $TEST_IMAGES

    for d in $TEST_IMAGES ; do
        IMAGE=${d/cwl/conglomerate}
        IMAGE=${IMAGE%?};
        echo Running: docker pull ${IMAGE}:latest
        docker pull ${IMAGE}:latest
    done
else
    TEST_IMAGES=''
fi

for d in cwl/*/ ; do
    if echo ${TEST_IMAGES[@]} | grep -q -w -v "$d"; then
        IMAGE=${d/cwl/conglomerate}
        IMAGE=${IMAGE%?};
        echo Running: docker pull ${IMAGE}:latest
        docker pull ${IMAGE}:latest
    fi
done
