FROM mcr.microsoft.com/playwright:v1.40.0-focal

WORKDIR /app

# Copy package.json and package-lock.json first for better caching
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy test files
COPY . .

# Install Playwright browsers
RUN npx playwright install

# Expose port for UI mode
EXPOSE 9323

# Default command (overridden by docker-compose)
CMD ["npx", "playwright", "test"] 