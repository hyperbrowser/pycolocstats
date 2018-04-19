#!/bin/bash

#set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
USE_TEST_DOCKER_IMAGES=$(/usr/bin/env python -c "from __future__ import print_function; import sys; sys.path += ['$DIR/src/pycolocstats']; from core.config import USE_TEST_DOCKER_IMAGES; print(USE_TEST_DOCKER_IMAGES)")

if [[ "$USE_TEST_DOCKER_IMAGES" == "True" ]]; then
    TEST_IMAGES=cwl/*_test/
else
    TEST_IMAGES=''
fi

for d in cwl/*/ ; do
    if echo ${TEST_IMAGES[@]} | grep -q -w -v ${d%?}_test/; then
        if [[ $d != *_test/ || "$USE_TEST_DOCKER_IMAGES" == "True" ]]; then
            IMAGE=${d/cwl/conglomerate}
            IMAGE=${IMAGE%?};
            echo Running: docker pull ${IMAGE}:latest
            docker pull ${IMAGE}:latest
        fi
    fi
done
