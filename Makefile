.PHONY: build run shell

TAG=hack-holyoke-dating-app/dating-app:latest
GUEST_PATH=/app
HOST_PATH=${PWD}

GUEST_PORT=5000
HOST_PORT=5000

GUEST_SHELL=/bin/bash

# build the docker container
build:
	docker build -t "${TAG}" .

# run flask server in docker
run:
	docker run \
		-it \
		--rm \
		--net host \
		-p "${HOST_PORT}:${GUEST_PORT}" \
		-v "${HOST_PATH}:${GUEST_PATH}" \
		"${TAG}"

shell:
	docker run \
		-it \
		--rm \
		--net host \
		-p "${HOST_PORT}:${GUEST_PORT}" \
		-v "${HOST_PATH}:${GUEST_PATH}" \
		"${TAG}" \
		"${GUEST_SHELL}"
