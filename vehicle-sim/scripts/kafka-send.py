#!/usr/bin/env python
from confluent_kafka import Producer
import socket


TOPIC = 'hello'
conf = {'bootstrap.servers': "localhost:9092",
        'client.id': socket.gethostname()}

producer = Producer(conf)

for i in range(500000):
    producer.produce(TOPIC, key="key", value="value")
    # producer.flush()  # Sync
    print(f" [x] Sent 'Hello World!' {i}")
