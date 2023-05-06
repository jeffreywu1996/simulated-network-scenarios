# Dockerized Network Simulation
Example of how to simulate various network scenarios using dockers

## Use case
Test performance of pub/sub sdk under poor network scenarios.
- Have server running in server docker
- Have sdk running continious pub/sub in client docker
- Run tc command to shape network traffic like adding delay, package loss, limit bandwidth
- Verify for dropped messages, if messages are delievered in order


![network-simulation drawio (1)](https://user-images.githubusercontent.com/13981821/236593235-c4d36d7a-82cd-4f26-8c6e-010f9d9ca8b2.png)


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
