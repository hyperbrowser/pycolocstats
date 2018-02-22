FROM biocontainers/biocontainers

USER root

RUN apt-get update && \
    apt-get install -y \
    gcc make autoconf zlib1g-dev libbz2-dev libcurl4-openssl-dev libssl-dev ruby && \
    apt-get clean && \
    apt-get purge && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN conda install -c bioconda bx-python

RUN pip install numpy

WORKDIR /root

RUN git clone https://github.com/hyperbrowser/goshifter.git

WORKDIR goshifter

RUN wget https://hyperbrowser.uio.no/hb/static/hyperbrowser/files/conglomerate/goShifter/hg38_eur.tar.gz && \
tar -xzf hg38_eur.tar.gz && \
rm hg38_eur.tar.gz