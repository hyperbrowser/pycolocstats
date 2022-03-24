FROM biocontainers/biocontainers

USER root

RUN apt-get update && \
    apt-get install -y \
    gcc make autoconf zlib1g-dev libbz2-dev libcurl4-openssl-dev libssl-dev ruby tabix && \
    apt-get clean && \
    apt-get purge && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /root

RUN git clone https://github.com/ryanlayer/giggle.git

WORKDIR giggle

RUN make

WORKDIR bin

RUN mkdir /regiondb && \
wget -nv https://hyperbrowser.uio.no/hb/static/hyperbrowser/files/pycolocstats/lola/LOLACore_170206.tgz -O /regiondb/LOLACore_170206.tgz && \
mkdir -p /regiondb/LOLACore_170206/hg19 && \
mkdir -p /regiondb/LOLACore_170206/hg38 && \
tar xf /regiondb/LOLACore_170206.tgz -C /regiondb/LOLACore_170206 && \
rm /regiondb/LOLACore_170206.tgz && \
mv /regiondb/LOLACore_170206/scratch/ns5bc/resources/regions/LOLACore/hg19/codex /regiondb/LOLACore_170206/hg19/ && \
mv /regiondb/LOLACore_170206/scratch/ns5bc/resources/regions/LOLACore/hg38/codex /regiondb/LOLACore_170206/hg38/ && \
rm -rf /regiondb/LOLACore_170206/scratch/ && \
find /regiondb/LOLACore_170206/ -name "*.narrowPeak" -exec sh -c 'cut -f 1,2,3 $1 > "${1%.narrowPeak}.bed"' _ {} \; -exec rm {} \; && \
find /regiondb/LOLACore_170206/ -name '*.bed' -type f -exec bgzip {} \; && \
find /regiondb/LOLACore_170206/ -name '*.RData' -type f -exec rm {} \;

RUN sed -i 's%#!/bin/sh%#!/bin/bash%g' ../scripts/sort_bed
