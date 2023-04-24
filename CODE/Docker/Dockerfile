From ubuntu:20.04

ARG TARGETPLATFORM=linux/amd64,linux/arm64
ARG DEBIAN_FRONTEND=noninteractive
ARG PUBLIC_MM_TAR_NAME=public_mm_linux_main_2018.tar.bz2

ADD ./$PUBLIC_MM_TAR_NAME ./
ADD ./DataIndexer ./DataIndexer
ADD ./solr_server ./solr_server
RUN apt-get -y update && \
    cd public_mm && \
    apt-get install -y nano python3-pip && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN apt-get update && \
    pip install --upgrade pip && \
    pip install networkx scipy pymetamap && \
    apt-get install -y openjdk-8-jdk && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD ./apache-tomcat-9.0.34 ./apache-tomcat-9.0.34
EXPOSE 8080
ADD ./startup.sh ./startup.sh
RUN chmod +x ./startup.sh
CMD [ "/bin/bash", "-c", "./startup.sh && tail -f /dev/null" ]

