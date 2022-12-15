import logging
import requests
import json
import subprocess

from config import SERVER_IP

class SDK:
    pass


logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(filename)s: %(message)s')
logger = logging.getLogger(__name__)


def empty_consumers_queue(topic, consumer_id):
    EMPTY_QUEUE_FILE = "./build/empty_queue"
    subprocess.check_call([EMPTY_QUEUE_FILE, topic, consumer_id])
    logger.info(f'Emptied queue for topic: {topic}, consumer_id: {consumer_id}')


def produce_data_to_topic(topic: str, size: int, empty_queue=True, consumer_id='', producer_id='test-producer'):
    """
    Produces messages to a topic
    topic: topic to produce to
    size: how many messages to produce. Messages start with payload = 1, 2, ...
    empty: whether or not to empty queue before producing. Defaults to true
    consumer_id: (required if empty is true)
    producer_id: producer id
    """
    if empty_queue:
        if not consumer_id:
            logger.error('consumer_id is required if empty_queue is True')
            return
        empty_consumers_queue(topic, consumer_id)

    logger.info(f'Producing {size} messages to {topic}')
    vehicle_cfg = vehicle_config('MyVehicle', 'default')
    sdk = SDK(producer_id, PRIORITY.LOW, vehicle_cfg=vehicle_cfg)

    for i in range(1, size + 1):
        payload = f'{i}\rxxxpython'
        sdk.produce(topic, payload)
        print(f'Produced {i} to {topic} by {producer_id}')
