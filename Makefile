.PHONY: build run shell

build:
	./scripts/docker-build.sh

run:
	./scripts/docker-run.sh

shell:
	./scripts/docker-shell.sh
