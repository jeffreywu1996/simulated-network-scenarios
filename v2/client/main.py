import time
import requests

i = 0
while True:
    r = requests.get(f'http://server:8001/echo/{i}')

    i += 1
    time.sleep(1)
