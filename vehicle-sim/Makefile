.PHONY: build
build:
	docker compose -f docker/docker-compose.yaml build --no-cache

.PHONY: start
start:
	# docker-compose -f docker/docker-compose.yaml up --build --abort-on-container-exit
	docker compose -f docker/docker-compose.yaml up --abort-on-container-exit

.PHONY: start-rabbit
start-rabbit:
	docker compose -f docker/docker-compose.rabbit.yaml up -d --remove-orphans

.PHONY: stop-rabbit
stop-rabbit:
	docker compose -f docker/docker-compose.rabbit.yaml down

.PHONY: start-kafka
start-kafka:
	docker compose -f docker/docker-compose.kafka.yaml up -d --remove-orphans

.PHONY: stop-kafka
stop-kafka:
	docker compose -f docker/docker-compose.kafka.yaml down
