FROM biocontainers/biocontainers

USER root

RUN apt-get update && \
    apt-get install -y \
    r-base \
    libxml2-dev \
    libcurl4-openssl-dev \
    tabix && \
    apt-get clean && \
    apt-get purge && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN echo "r <- getOption('repos'); r['CRAN'] <- 'http://cran.us.r-project.org'; options(repos = r);" > ~/.Rprofile

RUN Rscript -e "source('http://bioconductor.org/biocLite.R')" \
-e "biocLite('LOLA')"

RUN Rscript -e "install.packages('reshape2')" \
-e "install.packages('simpleCache')"

RUN mkdir /regiondb && \
wget -nv https://hyperbrowser.uio.no/hb/static/hyperbrowser/files/pycolocstats/lola/LOLACore_170206.tgz -O /regiondb/LOLACore_170206.tgz && \
mkdir -p /regiondb/LOLACore_170206/hg19 && \
mkdir -p /regiondb/LOLACore_170206/hg38 && \
tar xf /regiondb/LOLACore_170206.tgz -C /regiondb/LOLACore_170206 && \
rm /regiondb/LOLACore_170206.tgz && \
mv /regiondb/LOLACore_170206/scratch/ns5bc/resources/regions/LOLACore/hg19/codex /regiondb/LOLACore_170206/hg19/ && \
mv /regiondb/LOLACore_170206/scratch/ns5bc/resources/regions/LOLACore/hg38/codex /regiondb/LOLACore_170206/hg38/ && \
rm -rf /regiondb/LOLACore_170206/scratch/
