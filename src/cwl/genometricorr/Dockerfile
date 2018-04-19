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
-e "biocLite('IRanges')" \
-e "biocLite('GenomicRanges')" \
-e "biocLite('rtracklayer')" \
-e "biocLite('TxDb.Hsapiens.UCSC.hg19.knownGene')"

RUN Rscript -e "install.packages('gplots')" \
-e "install.packages('RCurl')" \
-e "install.packages('GenometriCorr', repos='http://genometricorr.sourceforge.net/R/', type='source')"
