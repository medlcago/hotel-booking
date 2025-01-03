COMPOSE_DEV=docker-compose -f docker-compose.dev.yaml
COMPOSE_PROD=docker-compose -f docker-compose.yaml

.PHONY: up-dev down-dev logs-dev up-prod down-prod logs-prod

up-dev:
	$(COMPOSE_DEV) up -d

down-dev:
	$(COMPOSE_DEV) down

logs-dev:
	$(COMPOSE_DEV) logs -f

up-prod:
	$(COMPOSE_PROD) up -d

down-prod:
	$(COMPOSE_PROD) down

logs-prod:
	$(COMPOSE_PROD) logs -f