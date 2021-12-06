FROM ubuntu:16.04

RUN apt-get -y update && \
    apt-get -y install openssl curl python