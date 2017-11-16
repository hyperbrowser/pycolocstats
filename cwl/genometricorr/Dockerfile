FROM biocontainers/biocontainers

RUN conda install r-base

RUN echo "r <- getOption('repos'); r['CRAN'] <- 'http://cran.us.r-project.org'; options(repos = r);" > ~/.Rprofile

RUN Rscript -e "options(install.packages.compile.from.source='never')" \
-e "source('http://bioconductor.org/biocLite.R')" \
-e "biocLite('IRanges')" \
-e "biocLite('GenomicRanges')" \
-e "biocLite('rtracklayer')" \
-e "biocLite('TxDb.Hsapiens.UCSC.hg19.knownGene')"

RUN Rscript -e "install.packages('gplots')" \
-e "install.packages('RCurl')" \
-e "install.packages('GenometriCorr', repos='http://genometricorr.sourceforge.net/R/', type='source')"