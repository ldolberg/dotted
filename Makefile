.PHONY: build up down smoke-test

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

smoke-test: up
	@echo "Running smoke test..."
	docker-compose exec backend python /app/tests/smoke_test.py 