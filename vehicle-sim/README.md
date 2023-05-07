# Simulation of vehicles using IoT
This project attempts to simulate a vehicle in different network scenarios communicating with a server

## Technologies
This project attempts to compare various technologies, naming AMQP and MQTT in handling poor network scenarios
### Guarentees
We want the following guarentees:
- No package drops
- Guarenteed ordering

Here we will look at RabbitMQ (AMQP) and RabbitMQ(MQTT) to look at if either fullfills the guarentees

### APIs
1. Produce
2. Consume

### Diagrams

## Get Started
```
make start
```
Starts two dockers like the image above, one client and one server.
You can add more client and server code to suit your needs. Some examples are a REST endpoint, pub/sub, file download streaming APIs...
Usually we will perform network shaping on the client side since it is more likely for network instability on the client side in real world scenario.
However, you can also shape network on server side to test client behaviors when server has network issues.

## Reading Materials
https://www.rabbitmq.com/tutorials/tutorial-one-python.html
https://www.kai-waehner.de/blog/2021/03/15/apache-kafka-mqtt-sparkplug-iot-blog-series-part-1-of-5-overview-comparison/
https://www.hivemq.com/blog/creating-iiot-data-pipeline-using-mqtt-and-kafka/
https://www.instaclustr.com/support/documentation/kafka-connect/accessing-and-using-kafka-connect/using-kafka-mqtt/
https://www.influxdata.com/blog/mqtt-vs-kafka-iot-advocates-perspective-part-3/
https://github.com/InfluxCommunity/kafka_mqtt_tutorial/blob/0b3090cc1e430fdad545348a07b9c945dd54660c/part2/mqtt_producer.py
