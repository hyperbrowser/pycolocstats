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
wget https://hyperbrowser.uio.no/hb/static/hyperbrowser/files/conglomerate/LOLACore_170206.tgz -O /regiondb/LOLACore_170206.tgz && \
mkdir -p /regiondb/LOLACore_170206 && \
tar xf /regiondb/LOLACore_170206.tgz -C /regiondb/LOLACore_170206 && \
rm /regiondb/LOLACore_170206.tgz && \
mv /regiondb/LOLACore_170206/scratch/ns5bc/resources/regions/LOLACore/* /regiondb/LOLACore_170206/ && \
rm -rf /regiondb/LOLACore_170206/scratch/ && \
find /regiondb/LOLACore_170206/ -name '*.bed' -type f -exec bgzip {} \;
