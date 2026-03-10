.PHONY: setup install dev run db-up db-wait db-init down lint format test

APP=app.main:app
CASSANDRA_CONTAINER=cassandra-db
SCHEMA=app/database/schema.cql

setup: install db-up db-wait db-init
	@echo "Environment ready 🚀"

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

dev: db-up db-wait db-init run

run:
	@echo "Starting API..."
	uvicorn $(APP) --reload

db-up:
	@echo "Starting Cassandra..."
	docker compose up -d cassandra

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
	docker exec -it cassandra-db cqlsh -k url_shortener