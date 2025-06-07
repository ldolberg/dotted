# Playwright E2E Tests for Dotted SaaS Reminder Service

This directory contains end-to-end tests for the Dotted application using Playwright.

## Prerequisites

- Docker and Docker Compose installed
- The main application services (frontend, backend, db, redis) should be running

## Quick Start

### 1. Start the Playwright service

```bash
# From the root directory of the project
docker-compose --profile testing up playwright -d
```

### 2. Run tests

```bash
# Run all tests
docker-compose exec playwright npm test

# Run tests with UI mode (accessible at http://localhost:9323)
docker-compose exec playwright npm run test:ui

# Run tests in headed mode (with browser visible)
docker-compose exec playwright npm run test:headed

# Run specific test file
docker-compose exec playwright npx playwright test tests/homepage.spec.js

# Run tests in debug mode
docker-compose exec playwright npm run test:debug
```

### 3. View test reports

```bash
# View HTML test report
docker-compose exec playwright npm run show-report

# The report will be available at http://localhost:9323 when show-report is running
```

## Test Structure

```
tests/e2e/
├── tests/
│   ├── homepage.spec.js      # Homepage functionality tests
│   ├── patients.spec.js      # Patients page functionality tests
│   └── navigation.spec.js    # Navigation and routing tests
├── playwright.config.js      # Playwright configuration
├── global-setup.js          # Global test setup
├── package.json             # Dependencies and scripts
└── Dockerfile              # Playwright container configuration
```

## Available Test Scripts

- `npm test` - Run all tests in headless mode
- `npm run test:ui` - Run tests with Playwright UI (great for debugging)
- `npm run test:headed` - Run tests with browser visible
- `npm run test:debug` - Run tests in debug mode
- `npm run show-report` - Show HTML test report
- `npm run codegen` - Generate tests by recording interactions

## Test Configuration

The tests are configured to:
- Run against multiple browsers (Chromium, Firefox, WebKit)
- Test mobile viewports (Pixel 5, iPhone 12)
- Generate screenshots on failure
- Record videos on failure
- Generate HTML reports
- Retry failed tests in CI environment

## Environment Variables

- `BASE_URL`: Frontend URL (default: http://frontend:3000)
- `API_URL`: Backend URL (default: http://backend:80)

## Writing New Tests

1. Create a new `.spec.js` file in the `tests/` directory
2. Follow the existing patterns in the sample tests
3. Use descriptive test names and group related tests with `test.describe()`
4. Use page object models for complex interactions
5. Add appropriate waits and assertions

## Troubleshooting

### Tests failing to connect to services
- Ensure all main application services are running: `docker-compose up -d`
- Check that the frontend is accessible at the configured BASE_URL
- Verify network connectivity between containers

### UI mode not accessible
- Make sure port 9323 is not blocked by firewall
- Ensure the Playwright container is running with the UI script

### Permission issues
- Make sure the test results and report directories are writable
- Check Docker volume permissions

## Example Usage

```bash
# Start all services including Playwright
docker-compose --profile testing up -d

# Run tests and generate report
docker-compose exec playwright npm test

# View the results
docker-compose exec playwright npm run show-report

# Clean up
docker-compose --profile testing down
``` 