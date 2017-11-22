FROM biocontainers/biocontainers

USER root

RUN apt-get update && \
    apt-get install -y \
    gcc make autoconf zlib1g-dev libbz2-dev libcurl4-openssl-dev libssl-dev ruby && \
    apt-get clean && \
    apt-get purge && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /root

RUN git clone https://github.com/ryanlayer/giggle.git

WORKDIR /root/giggle/

RUN make

WORKDIR bin
