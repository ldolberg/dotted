.PHONY: build up down smoke-test e2e-test e2e-up e2e-down e2e-ui e2e-report seed-data

build:
	docker-compose build

up:
	docker-compose up --build -d

down:
	docker-compose down

smoke-test: up
	@echo "Running smoke test..."
	docker-compose exec backend python /app/tests/smoke_test.py

# E2E Testing commands
e2e-up:
	@echo "Starting all services including Playwright..."
	docker-compose --profile testing up -d

e2e-down:
	@echo "Stopping all services including Playwright..."
	docker-compose --profile testing down

e2e-test: e2e-up
	@echo "Running Playwright E2E tests..."
	docker-compose exec playwright npm test

e2e-ui: e2e-up
	@echo "Starting Playwright UI mode (accessible at http://localhost:9323)..."
	docker-compose exec playwright npm run test:ui

e2e-report:
	@echo "Showing Playwright test report..."
	docker-compose exec playwright npm run show-report

# Full test suite
test: smoke-test e2e-test
	@echo "All tests completed!"

seed-data:
	docker-compose exec backend python /app/create_test_patients.py