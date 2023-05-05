import time
import requests

i = 0
while True:
    try:
        start = time.time()
        r = requests.get(f'http://server:8001/echo/{i}', timeout=3)
        end = time.time()
        print(f'{i} response time: {end - start} seconds')
    except requests.exceptions.ConnectionError:
        print(f'request failed, {r.status_code}')

    i += 1
    time.sleep(1)
