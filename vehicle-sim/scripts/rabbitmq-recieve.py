#!/usr/bin/env python
import json
import pika, sys, os

db = {}

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='vehicle')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        decoded = json.loads(body.decode('utf-8'))
        id = decoded['id']
        order = decoded['order']

        if id not in db:
            db[id] = []

        if len(db[id]) > 0:
            assert db[id][-1] + 1 == order, f'out of order: {db[id][-1]} < {order}, id: {id}'
        db[id].append(order)

    channel.basic_consume(queue='vehicle', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
