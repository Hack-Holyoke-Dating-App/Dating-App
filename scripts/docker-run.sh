#!/usr/bin/env bash
docker run -it --rm --net host -v "$PWD:/app" "hack-holyoke-dating-app/dating-app:latest"