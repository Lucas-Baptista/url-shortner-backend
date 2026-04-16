.PHONY: setup install dev run db-up redis-up infra-up db-wait db-init down lint format test

APP=app.main:app
CASSANDRA_CONTAINER=cassandra-db
REDIS_CONTAINER=redis
SCHEMA=app/database/schema.cql

setup: install infra-up db-wait db-init
	@echo "Environment ready 🚀"

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

dev: infra-up db-wait db-init run

run:
	@echo "Starting API..."
	uvicorn $(APP) --reload

# 🔥 Infra (Cassandra + Redis)
infra-up: db-up redis-up

db-up:
	@echo "Starting Cassandra..."
	docker compose up -d cassandra

redis-up:
	@echo "Starting Redis..."
	docker compose up -d redis

db-wait:
	@echo "Waiting for Cassandra to be ready..."
	@until docker exec $(CASSANDRA_CONTAINER) cqlsh -e "describe keyspaces" > /dev/null 2>&1; do \
		printf "."; \
		sleep 2; \
	done
	@echo " Cassandra ready"

db-init:
	@echo "Initializing database schema..."
	docker exec -i $(CASSANDRA_CONTAINER) cqlsh < $(SCHEMA)

down:
	@echo "Stopping containers..."
	docker compose down

lint:
	@echo "Running linter..."
	flake8 app

format:
	@echo "Formatting code..."
	black app

test:
	@echo "Running tests..."
	pytest

db-shell:
	docker exec -it $(CASSANDRA_CONTAINER) cqlsh -k url_shortener

redis-shell:
	docker exec -it $(REDIS_CONTAINER) redis-cli