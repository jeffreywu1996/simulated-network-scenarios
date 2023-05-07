#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')


for i in range(500000):
    channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
    print(f" [x] Sent 'Hello World!' {i}")

connection.close()
