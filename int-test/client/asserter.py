import logging
import requests
import json

from config import SERVER_IP
from utils import get_timestamp, extract_payload_id


logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(filename)s: %(message)s')
logger = logging.getLogger(__name__)


def get_logs() -> list:
    logger.info('Getting test results from logs')
    res = requests.get('{}/logs'.format(SERVER_IP))
    logs = json.loads(res.text)
    logger.info('got logs, size: {}'.format(len(logs)))
    return logs


def log_to_server(data, consumer_id=None):
    payload_id = extract_payload_id(data.payload)
    requests.post('{}/log'.format(SERVER_IP), json={
        'id': payload_id,
        'topic': data.topic,
        'producer_id': data.producer_id,
        'sent_timestamp': data.timestamp,
        'recieve_timestamp': get_timestamp(),
        'consumer_id': consumer_id
    })


def assert_producer_id(logs: dict(), IGNORE_DELAY=False, MAX_DELAY_IN_MS=1000):
    """
    Asserts orders of messages in each of its producer_id
    """
    last_count = dict() # data_dict = {'producer_id': last_count,}
    for entry in logs:
        producer_id = entry['producer_id']
        _id = int(entry['id'])
        # Check payload order
        last_id = last_count.get(producer_id, 0) + 1
        assert _id == last_id, f'order is wrong: expect: {_id}, got {last_id}, producer_id: {producer_id}'
        last_count[producer_id] = _id

        # Check timestamp delay
        time_diff = entry['recieve_timestamp'] - entry['sent_timestamp']
        if not IGNORE_DELAY:
            assert time_diff < MAX_DELAY_IN_MS, "Message delay exceeded {}ms".format(MAX_DELAY_IN_MS)
        logger.info('logs -> producer_id: {}, n: {}, delay: {}'.format(producer_id, _id, time_diff))


def assert_logs(logs, IGNORE_DELAY=True, MAX_DELAY_IN_MS=1000):
    n = 1
    for entry in logs:
        # Check payload order
        assert int(entry['id']) == n, f'order is wrong, n = {n}, entry = {entry}'

        # Check timestamp delay
        time_diff = entry['recieve_timestamp'] - entry['sent_timestamp']
        if not IGNORE_DELAY:
            assert time_diff < MAX_DELAY_IN_MS, "Message delay exceeded {}ms".format(MAX_DELAY_IN_MS)
        logger.info('log -> n: {}, delay: {}'.format(n, time_diff))
        n += 1
