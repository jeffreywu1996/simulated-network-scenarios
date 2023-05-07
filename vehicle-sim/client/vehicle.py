import time
import json
import uuid
import logging
from faker import Faker
from mq import RabbitMQ

fake = Faker()
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(filename)s: %(message)s')
logger = logging.getLogger(__name__)


class Vehicle:
    """
    Simulates a fake vehicle
    Talks to server via MQTT
    """

    def __init__(self, id: str = None):
        """
        id: b7889cce-8f83-4b89-bfa9-ce54c0b59294
        fake_loc: ('42.24113', '-88.3162', 'Crystal Lake', 'US', 'America/Chicago')
        location: {'lat': '42.24113', 'lng': '-88.3162'}
        """
        self.id = id or str(uuid.uuid4())
        fake_loc = fake.local_latlng(country_code='US', coords_only=False)
        self.location = {'lat': fake_loc[0], 'lng': fake_loc[1]}
        self.mq = RabbitMQ(host='localhost')
        self.queue = 'vehicle'
        self.mq.channel.queue_declare(queue=self.queue)

        logger.info(f'Vehicle created, id: {self.id}, location: {self.location}')

    def start(self):
        logger.info('Vehicle started...')
        i = 0
        while True:
            self.location = {
                'lat': str(float(self.location['lat']) + 0.0001),
                'lng': str(float(self.location['lng']) + 0.0001)
            }

            payload = json.dumps({
                'id': self.id,
                'location': self.location,
                'order': i
            })
            self.mq.channel.basic_publish(exchange='', routing_key=self.queue, body=payload)
            logger.info(f'published queue: {self.queue}, payload: {payload}')

            i += 1
            time.sleep(0.1)
