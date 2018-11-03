.PHONY: docker docker-build

TAG=hack-holyoke-dating-app/dating-app:latest
GUEST_PATH=/app
HOST_PATH=${PWD}

# docker: runs the development docker container
docker:
	docker run \
		-it \
		--rm \
		--net host \
		-v "${HOST_PATH}:${GUEST_PATH}" \
		"${TAG}"

# docker-build: builds the development docker container
docker-build:
	docker build -t "${TAG}" .
