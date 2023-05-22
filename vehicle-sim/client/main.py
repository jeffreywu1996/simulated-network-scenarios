import logging
import threading
from vehicle import Vehicle

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(filename)s: %(message)s')
logger = logging.getLogger(__name__)


def start_vehicle():
    Vehicle().start()


if __name__ == '__main__':
    logger.info('Starting client...')

    for i in range(10):
        threading.Thread(target=start_vehicle).start()
        threading.Thread(target=start_vehicle).start()
        threading.Thread(target=start_vehicle).start()
        threading.Thread(target=start_vehicle).start()
        threading.Thread(target=start_vehicle).start()
        # start_vehicle()

        import time
        time.sleep(10000)
