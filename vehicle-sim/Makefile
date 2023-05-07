.PHONY: build
build:
	docker compose -f docker/docker-compose.yaml build --no-cache

.PHONY: start
start:
	# docker-compose -f docker/docker-compose.yaml up --build --abort-on-container-exit
	docker compose -f docker/docker-compose.yaml up --abort-on-container-exit
