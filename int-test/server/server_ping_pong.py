import json
import os
import requests
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(filename)s: %(message)s')
logger = logging.getLogger(__name__)


TEST_TOPIC_RECIEVE = ''

class Consumer:
    # Test class here
    pass


def get_timestamp():
    """Returns timestamp in ms"""
    return round(time.time() * 1000)


def extract_payload_id(payload: bytes):
    end_idx = payload[:7].find(b'\r')
    if end_idx >= 7 or end_idx == -1:
        payload_id = 'unknown'
    else:
        payload_id = payload.decode('utf-8')[:end_idx]
    return payload_id


def main():
    if os.getenv('TEST_HASH'):
        test_topic = TEST_TOPIC_RECIEVE + '-' + os.getenv('TEST_HASH')

    logger.info(f"Starting ping_pong server with {test_topic}")
    consumer = Consumer('test-ping-pong-server', [(test_topic, 'FIRST')])
    consumer = Consumer()

    while True:
        try:
            data = consumer.poll(1)
            if data:
                if len(data.payload) < 100:
                    print(data.producer_id, " recieved --> ", data.payload)
                else:
                    print(data.producer_id, " recieved --> data size = ", len(data.payload))

                # logger.info('timestamp: {}'.format(data.timestamp))
                payload_id = extract_payload_id(data.payload)
                logger.info('payload_id: {}'.format(payload_id))
                logger.info('delay: {} ms'.format(get_timestamp() - data.timestamp))

                requests.post('http://0.0.0.0:8001/log', json={
                    'id': payload_id,
                    'topic': data.topic,
                    'producer_id': data.producer_id,
                    'sent_timestamp': data.timestamp,
                    'recieve_timestamp': get_timestamp()
                })
                # producer.produce(TEST_TOPIC_RETURN, data.payload)
                # logger.info('published messaged back')
        except Exception as e:
            logger.exception('Error found')
            logger.error(e)



if __name__ == '__main__':
    main()
