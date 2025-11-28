DOCKER_COMPOSE = docker compose --project-directory .
DEV_COMPOSE_FILE = ./docker-compose.dev.yml

dev:
	$(DOCKER_COMPOSE) -f $(DEV_COMPOSE_FILE) up --force-recreate --remove-orphans

cdev:
	$(DOCKER_COMPOSE) -f $(DEV_COMPOSE_FILE) up --force-recreate --remove-orphans --build
