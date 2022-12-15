import pytest
import logging
import subprocess
import shlex
import time

from utils import clean_up, wait_for_server_ready
import tctool

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(filename)s: %(message)s')
logger = logging.getLogger(__name__)



@pytest.fixture(scope="session", autouse=True)
def launch_server():
    time.sleep(2)
    wait_for_server_ready()
    logger.info('Wait for logging server to be ready...')

    yield


@pytest.fixture
def setup_test():
    logger.info('Cleaning up')
    clean_up() # cleans up logging db
    tctool.reset() # Resets all network changes
    yield

    clean_up() # cleans up logging db
    tctool.reset() # Resets all network changes
