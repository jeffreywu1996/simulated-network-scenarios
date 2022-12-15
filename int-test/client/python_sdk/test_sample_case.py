import pytest
import logging
import time

from config import SERVER_IP
from utils import clean_up, append_hash, Counter, wait_until_cnt
from asserter import get_logs, assert_logs
from multiprocessing import Process
import tctool

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(filename)s: %(message)s')
logger = logging.getLogger(__name__)


IGNORE_DELAY = True
MAX_DELAY_IN_MS_NORMAL = 1000
MAX_DELAY_IN_MS = 1000
MAX_MESSAGES = 50

job_to_cnt = dict()  # Maps job id to msg_cnt
counter = Counter()



def on_complete(id):
    counter.increment()
    logger.info(f'Produced {job_to_cnt[id]} to {TOPIC_1}')


def produce_messages(msg_count=MAX_MESSAGES, compression=False):
    counter.reset()
    # Produce code here
    for i in range(1, msg_count + 1):
        payload = f'{i}\rxxxxxpython'
        _id = sdk.async_produce(on_complete, TOPIC_1, payload, worker_id=worker_id)
        job_to_cnt[_id] = i
        # logger.debug(f'Triggered {i} to {TOPIC_1}')

        # fps = 10
        # Warning: don't produce too fast. Network down should happen in middle of producing.
        time.sleep(0.1)

    wait_until_cnt(counter, MAX_MESSAGES)

    del sdk
    time.sleep(3)


@pytest.mark.parametrize("compression", [False, True])
def test_produce_under_normal_network(setup_test, compression):
    """
    """
    logger.info(f'Running python test, compression = {compression}')
    produce_messages(MAX_MESSAGES, compression)
    logger.info('Completed python test')

    # Verifiy test
    logger.info('Starting verifier...')
    logs = get_logs()
    assert len(logs) == MAX_MESSAGES, "Log results should only have 20 messages"

    assert_logs(logs, IGNORE_DELAY=IGNORE_DELAY, MAX_DELAY_IN_MS=MAX_DELAY_IN_MS)


@pytest.mark.parametrize("compression", [False, True])
@pytest.mark.network_test
def test_network_down(setup_test, compression):
    """
    """
    logger.info(f'Running python test, compression = {compression}')
    p = Process(target=produce_messages, args=(MAX_MESSAGES, compression, ))
    p.start()

    # logger.info('Stopping network')
    time.sleep(2)
    tctool.network_down()
    time.sleep(10)
    tctool.network_up()

    p.join()
    time.sleep(2)

    logger.info('Completed python produce test')

    # Verifiy test
    logger.info('Starting verifier...')
    logs = get_logs()
    assert len(logs) == MAX_MESSAGES, "Log results should only have 20 messages"

    assert_logs(logs, IGNORE_DELAY=IGNORE_DELAY, MAX_DELAY_IN_MS=MAX_DELAY_IN_MS)
