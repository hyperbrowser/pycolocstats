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
wget -nv https://hyperbrowser.uio.no/hb/static/hyperbrowser/files/conglomerate/lola/LOLACore_170206.tgz -O /regiondb/LOLACore_170206.tgz && \
mkdir -p /regiondb/LOLACore_170206 && \
tar xf /regiondb/LOLACore_170206.tgz -C /regiondb/LOLACore_170206 && \
rm /regiondb/LOLACore_170206.tgz && \
mv /regiondb/LOLACore_170206/scratch/ns5bc/resources/regions/LOLACore/* /regiondb/LOLACore_170206/ && \
rm -rf /regiondb/LOLACore_170206/scratch/ && \
find /regiondb/LOLACore_170206/ -name "*.narrowPeak" -exec sh -c 'cut -f 1,2,3 $1 > "${1%.narrowPeak}.bed"' _ {} \; -exec rm {} \; && \
find /regiondb/LOLACore_170206/ -name '*.bed' -type f -exec bgzip {} \; && \
find /regiondb/LOLACore_170206/ -name '*.RData' -type f -exec rm {} \;

RUN mkdir /regiondb && \
wget -nv https://hyperbrowser.uio.no/hb/static/hyperbrowser/files/conglomerate/lola/LOLAExt_170206.tgz -O /regiondb/LOLAExt_170206.tgz && \
mkdir -p /regiondb/LOLAExt_170206 && \
tar xf /regiondb/LOLAExt_170206.tgz -C /regiondb/LOLAExt_170206 && \
rm /regiondb/LOLAExt_170206.tgz && \
mv /regiondb/LOLAExt_170206/scratch/ns5bc/resources/regions/LOLACore/* /regiondb/LOLAExt_170206/ && \
rm -rf /regiondb/LOLAExt_170206/scratch/ && \
find /regiondb/LOLAExt_170206/ -name "*.narrowPeak" -exec sh -c 'cut -f 1,2,3 $1 > "${1%.narrowPeak}.bed"' _ {} \; -exec rm {} \; && \
find /regiondb/LOLAExt_170206/ -name '*.bed' -type f -exec bgzip {} \; && \
find /regiondb/LOLAExt_170206/ -name '*.RData' -type f -exec rm {} \;

RUN wget -nv https://hyperbrowser.uio.no/hb/static/hyperbrowser/files/conglomerate/giggle/Giggle_hosted_260218/fantom_sort.tar.gz -O /regiondb/fantom_sort.tar.gz && \
mkdir -p /regiondb/Giggle_hosted_260218/hg19 && \
tar xf /regiondb/fantom_sort.tar.gz -C /regiondb/Giggle_hosted_260218/hg19 && \
rm /regiondb/fantom_sort.tar.gz && \
mkdir /regiondb/Giggle_hosted_260218/hg19/fantom_sort/regions && \
mv /regiondb/Giggle_hosted_260218/hg19/fantom_sort/*.bed.gz /regiondb/Giggle_hosted_260218/hg19/fantom_sort/regions/

RUN wget -nv https://hyperbrowser.uio.no/hb/static/hyperbrowser/files/conglomerate/giggle/Giggle_hosted_260218/roadmap_sort.tar.gz -O /regiondb/roadmap_sort.tar.gz && \
tar xf /regiondb/roadmap_sort.tar.gz -C /regiondb/Giggle_hosted_260218/hg19 && \
rm /regiondb/roadmap_sort.tar.gz && \
mkdir /regiondb/Giggle_hosted_260218/hg19/roadmap_sort/regions && \
mv /regiondb/Giggle_hosted_260218/hg19/roadmap_sort/*.bed.gz /regiondb/Giggle_hosted_260218/hg19/roadmap_sort/regions/

RUN wget -nv https://hyperbrowser.uio.no/hb/static/hyperbrowser/files/conglomerate/giggle/Giggle_hosted_260218/ucscweb_sort_valid_bed.tar.gz -O /regiondb/ucscweb_sort_valid_bed.tar.gz && \
tar xf /regiondb/ucscweb_sort_valid_bed.tar.gz -C /regiondb/Giggle_hosted_260218/hg19 && \
rm /regiondb/ucscweb_sort_valid_bed.tar.gz && \
mkdir /regiondb/Giggle_hosted_260218/hg19/ucscweb_sort_valid_bed/regions && \
mv /regiondb/Giggle_hosted_260218/hg19/ucscweb_sort_valid_bed/*.bed.gz /regiondb/Giggle_hosted_260218/hg19/ucscweb_sort_valid_bed/regions/

RUN sed -i 's%#!/bin/sh%#!/bin/bash%g' ../scripts/sort_bed
