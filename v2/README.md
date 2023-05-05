# Dockerized Network Simulation
Example of how to simulate various network scenarios using dockers

## Use case
TODO

## Get Started
```
make start
```

## Reading Materials
https://www.kai-waehner.de/blog/2022/01/04/when-not-to-use-apache-kafka/
https://www.kai-waehner.de/blog/2021/03/15/apache-kafka-mqtt-sparkplug-iot-blog-series-part-1-of-5-overview-comparison/


### ROS to MQTT
http://wiki.ros.org/mqtt_client#quick-start


### Use AWS iot w/ MQTT
downside: max message size 128kb

For messages larger, should be split up into smaller messages

For bigger payload, use S3.
https://github.com/apoorvam/aws-s3-multipart-upload/blob/master/aws-multipart-upload.go
