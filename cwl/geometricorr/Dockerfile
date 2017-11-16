FROM biocontainers/biocontainers

RUN conda install r-base

RUN Rscript -e "source('http://bioconductor.org/biocLite.R')" \
-e "biocLite('IRanges')" \
-e "biocLite('GenomicRanges')" \
-e "biocLite('rtracklayer')" \
-e "biocLite('TxDb.Hsapiens.UCSC.hg19.knownGene')"

RUN Rscript -e "install.packages('gplots', repos = 'http://cran.us.r-project.org')" \
-e "install.packages('RCurl', repos = 'http://cran.us.r-project.org')" \
-e "install.packages('GenometriCorr', repos='http://genometricorr.sourceforge.net/R/', type='source')"