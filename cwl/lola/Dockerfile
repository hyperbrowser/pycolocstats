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

RUN echo "r <- getOption('repos'); r['CRAN'] <- 'http://cran.us.r-project.org'; options(repos = r);" > ~/.Rprofile

RUN Rscript -e "source('http://bioconductor.org/biocLite.R')" \
-e "biocLite('LOLA')"

RUN Rscript -e "install.packages('reshape2')" \
-e "install.packages('simpleCache')"

RUN mkdir /regiondb && \
wget http://cloud.databio.org.s3.amazonaws.com/regiondb/LOLACore_170206.tgz -O /regiondb/LOLACore_170206.tgz && \
mkdir -p /regiondb/LOLACore_170206 && \
tar xf /regiondb/LOLACore_170206.tgz -C /regiondb/LOLACore_170206 && \
rm /regiondb/LOLACore_170206.tgz

RUN mv /regiondb/LOLACore_170206/scratch/ns5bc/resources/regions/LOLACore/* /regiondb/LOLACore_170206/ && rm -rf /regiondb/LOLACore_170206/scratch/
