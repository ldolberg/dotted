.PHONY: build up down smoke-test backend-test

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

smoke-test: up
	@echo "Running smoke test..."
	docker-compose exec backend python /app/tests/smoke_test.py

backend-test:
	@echo "Cleaning up previous services..."
	-docker-compose down # Use - to ignore errors if services are not running
	@echo "Building services..."
	docker-compose build
	@echo "Running backend tests..."
	docker-compose run --rm backend python -m pytest /app/tests/test_users.py 