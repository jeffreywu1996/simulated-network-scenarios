import logging
import pika
import paho.mqtt.client as mqtt

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(filename)s: %(message)s')
logger = logging.getLogger(__name__)

class MQTT:
    def __init__(self, host: str, port: int, username: str = None, password: str = None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = mqtt.Client()
        self.client.username_pw_set(username, password)
        self.client.connect(host, port)

    def publish(self, topic: str, payload: str):
        self.client.publish(topic, payload)


class RabbitMQ:
    def __init__(self, host: str = 'localhost', port: int = 5672):
        self.host = host

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()


    def __del__(self):
        if hasattr(self, 'connection'):
            self.connection.close()
