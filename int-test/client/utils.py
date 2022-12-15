import time
import os
import logging
import uuid
import requests
import threading

from config import SERVER_IP

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(filename)s: %(message)s')
logger = logging.getLogger(__name__)


class Counter():
    def __init__(self, value=0):
        self.value = value
        self.thread_lock = threading.Lock()

    def increment(self):
        with self.thread_lock:
            self.value += 1

    def get(self):
        return self.value

    def reset(self):
        with self.thread_lock:
            self.value = 0


def get_timestamp():
    """Returns timestamp in ms"""
    return round(time.time() * 1000)

def new_id():
    """Returns unique uuid"""
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(time.time())))


def append_hash(s):
    """Appends hash from end of string"""
    if 'TEST_HASH' not in os.environ:
        raise Exception('ERROR: env var TEST_HASH not defined')
    return s + '-' + os.getenv('TEST_HASH')


def clean_up():
    """Cleans up logging db"""
    res = requests.get('{}/clear'.format(SERVER_IP))
    if res:
        logger.info('Successfully cleaned up log server')
        return True
    else:
        logger.error('Failed to clean up log server, {}'.format(res.status_code))
        return False


def wait_for_server_ready(increment=3, max_wait=50):
    """Wait for logging server to be ready
    """
    wait = 0
    while wait < max_wait:
        try:
            requests.get('{}/log'.format(SERVER_IP))
            logger.info('log server is ready')
            return

        except requests.exceptions.ConnectionError:
            logger.info('Server is not ready... {} out of {}'.format(wait, max_wait))

        time.sleep(increment)
        wait += increment


def extract_payload_id(payload: bytes):
    end_idx = payload[:7].find(b'\r')
    if end_idx >= 7 or end_idx == -1:
        payload_id = 'unknown'
    else:
        payload_id = payload.decode('utf-8')[:end_idx]
    return payload_id


def wait_until_cnt(counter: Counter, MAX_MESSAGES: int):
    """
    counter: Counter object
    """
    MAX_WAIT = 30
    logger.info(f'waiting until {MAX_MESSAGES} messages are recieved...')

    t = 0
    while t < MAX_WAIT:
        t += 1
        count = counter.get()
        if count == MAX_MESSAGES:
            logger.info(f'At count {count}, all message recieved stop.')
            return

        logger.info(f'Waiting {t} out of {MAX_WAIT}. {count} / {MAX_MESSAGES} messages')
        time.sleep(1)

    logger.error('Max wait achieved, timeout wait')
