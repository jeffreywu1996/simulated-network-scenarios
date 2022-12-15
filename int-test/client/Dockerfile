FROM ubuntu

WORKDIR /work

# nvidia patch
COPY nvidia_patch.sh .
RUN ./nvidia_patch.sh

RUN apt-get update && \
    apt-get install iproute2 iputils-ping -y
RUN apt-get install iptables -y

COPY ./client/requirements.txt .
RUN pip3 install -r requirements.txt


COPY . .

CMD zoro agent start && ./entrypoint.sh
