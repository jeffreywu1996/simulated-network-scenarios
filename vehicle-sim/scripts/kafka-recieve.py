from confluent_kafka import Consumer

TOPIC = 'hello'
conf = {'bootstrap.servers': "localhost:9092",
        'group.id': "foo2",
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False
}

consumer = Consumer(conf)
running = True

try:
    consumer.subscribe([TOPIC])

    while running:
        msg = consumer.poll(timeout=1.0)
        if msg is None: continue

        if msg.error():
            print(f'ERROR: {msg.error()}')
        else:
            print(f'Message recieved: topic: {msg.topic()}, key: {msg.key()}, value: {msg.value()}, timestamp: {msg.timestamp()}')
finally:
    # Close down consumer to commit final offsets.
    consumer.close()
