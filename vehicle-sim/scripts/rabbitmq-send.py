#!/usr/bin/env python
import time
import os
import pika

MQ_HOST = os.getenv('MQTT_HOST', 'localhost')

print(MQ_HOST)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=MQ_HOST))
channel = connection.channel()

channel.queue_declare(queue='hello')

# Turn on delivery confirmations
# This confirms delievery before sending the next message
# https://pika.readthedocs.io/en/stable/examples/blocking_publish_mandatory.html
# This guarentees that the message is delivered
channel.confirm_delivery()


for i in range(500000):
    channel.basic_publish(exchange='', routing_key='hello', body=f'Hello World! {i}')
    print(f" [x] Sent 'Hello World!' {i}")
    time.sleep(0.5)

connection.close()
