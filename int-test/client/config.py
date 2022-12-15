import os

IS_DOCKER = os.getenv('IS_DOCKER', 'false') == 'true'

if IS_DOCKER:
    CLIENT_IP = 'http://client:8001'
    SERVER_IP = 'http://server:8001'
else:
    CLIENT_IP = 'http://0.0.0.0:8001'
    SERVER_IP = 'http://0.0.0.0:8001'

TEST_TOPIC_RECIEVE = 'test-ping-pong'
TEST_TOPIC_RETURN = 'test-ping-pong'
