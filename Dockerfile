FROM ubuntu:16.04

RUN apt-get -y update
RUN apt-get -y install openssl curl 
RUN apt-get -y install python python-pip 
RUN apt-get -y install golang
RUN apt-get -y install git 

RUN pip install pycrypto

#ENV GOPATH=/go

#RUN mkdir /go && \
#    go get github.com/github-release/github-release