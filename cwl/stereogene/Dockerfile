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

RUN git clone https://github.com/favorov/stereogene.git

WORKDIR /root/stereogene/

RUN git checkout release

WORKDIR /root/stereogene/src

RUN make