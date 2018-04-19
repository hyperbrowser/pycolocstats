FROM biocontainers/biocontainers

USER root

RUN apt-get update && \
    apt-get install -y \
    gcc make autoconf zlib1g-dev libbz2-dev libcurl4-openssl-dev libssl-dev ruby liblzo2-dev tabix && \
    apt-get clean && \
    apt-get purge && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install bx-python numpy

WORKDIR /root

RUN git clone https://github.com/hyperbrowser/goshifter.git

WORKDIR goshifter

RUN wget -nv https://hyperbrowser.uio.no/hb/static/hyperbrowser/files/conglomerate/goShifter/hg38_eur.tar.gz && \
tar -xzf hg38_eur.tar.gz && \
rm hg38_eur.tar.gz && \
chmod -R 777 /root
