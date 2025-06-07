// global-setup.js
async function globalSetup(config) {
  console.log('🚀 Starting global setup for Playwright tests...');
  
  // Wait for services to be ready
  console.log('⏳ Waiting for frontend and backend services to be ready...');
  
  // You can add health checks here if needed
  // For now, we'll rely on docker-compose dependencies
  
  console.log('✅ Global setup completed successfully');
}

module.exports = globalSetup; 