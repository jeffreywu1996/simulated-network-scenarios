import time
import uuid
import logging
from faker import Faker

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
        logger.info(f'Vehicle created, id: {self.id}, location: {self.location}')

    def start(self):
        logger.info('Vehicle started...')
        while True:
            self.location = {
                'lat': str(float(self.location['lat']) + 0.0001),
                'lng': str(float(self.location['lng']) + 0.0001)
            }

            logger.info(f'id: {self.id}, location: {self.location}')
            time.sleep(1)
