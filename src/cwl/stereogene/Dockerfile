FROM biocontainers/biocontainers

USER root

RUN apt-get update && \
    apt-get install -y \
    r-base \
    libxml2-dev \
    libcurl4-openssl-dev && \
    apt-get clean && \
    apt-get purge && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /root

RUN git clone -b release https://github.com/favorov/stereogene.git

WORKDIR stereogene/src

RUN mkdir -p ./obj

RUN make -f StereoGene.mak
