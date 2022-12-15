FROM ubuntu

WORKDIR /work

# nvidia patch
COPY nvidia_patch.sh .
RUN ./nvidia_patch.sh

RUN apt-get update && \
    apt-get install iproute2 iputils-ping -y

COPY ./server/requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./server .

CMD ["./launch.sh"]

EXPOSE 8001
