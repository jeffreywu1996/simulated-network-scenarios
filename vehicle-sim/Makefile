.PHONY: build
build:
	docker compose -f docker/docker-compose.yaml build --no-cache

.PHONY: start
start:
	# docker-compose -f docker/docker-compose.yaml up --build --abort-on-container-exit
	docker compose -f docker/docker-compose.yaml up --abort-on-container-exit

.PHONY: start-rabbitmq
start-rabbitmq:
	docker run -it --rm -d --hostname my-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management
