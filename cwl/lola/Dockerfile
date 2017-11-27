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

RUN Rscript -e "install.packages('reshape2')"

RUN wget http://cloud.databio.org.s3.amazonaws.com/regiondb/LOLACore_170206.tgz -O /root/LOLACore_170206.tgz && \
mkdir -p /root/LOLACore_170206 && \
tar xf /root/LOLACore_170206.tgz -C /root/LOLACore_170206 && \
rm /root/LOLACore_170206.tgz
