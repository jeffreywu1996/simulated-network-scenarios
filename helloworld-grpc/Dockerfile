FROM python:3.10.5
# FROM ubuntu:18.04

WORKDIR /work
RUN apt-get update && \
    apt-get install iproute2 iputils-ping iptables -y

RUN pip3 install tcconfig \
                 grpcio \
                 grpcio-tools

COPY . .

CMD /bin/bash
