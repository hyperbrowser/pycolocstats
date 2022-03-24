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

RUN git clone -b release https://github.com/favorov/stereogene.git

WORKDIR stereogene/src

RUN mkdir -p ./obj

RUN make -f StereoGene.mak

RUN Rscript -e 'install.packages("markdown", repos = "https://cran.revolutionanalytics.com")'

RUN Rscript -e 'install.packages("rmarkdown", repos = "https://cran.revolutionanalytics.com")'

RUN wget https://github.com/jgm/pandoc/releases/download/1.15.1/pandoc-1.15.1-1-amd64.deb && \
dpkg -i pandoc-1.15.1-1-amd64.deb && \
rm pandoc-1.15.1-1-amd64.deb