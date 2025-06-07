# SaaS Reminder Service

A cloud-based appointment reminder system for healthcare providers, featuring patient management, communication preferences, and secure access control.

![Architecture Diagram](docs/architecture.png)

## Key Features

- Patient Management (CRUD operations)
- JWT-based Authentication & Authorization
- Role-based Access Control (Admin/Staff roles)
- Google OAuth Integration
- Communication Preferences Management
- Audit Logging & Soft Deletes
- Responsive Web Interface
- Comprehensive Test Coverage (Unit, Integration, E2E)

## Technology Stack

### Backend Services
- **Framework**: Python Flask
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Cache**: Redis
- **Auth**: JWT, OAuth2
- **API Docs**: Swagger UI (Planned)

### Frontend
- **Framework**: React 18
- **State Management**: Context API
- **UI Library**: Ant Design
- **Routing**: React Router 6
- **Testing**: Playwright, Jest

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **CI/CD**: GitHub Actions (Planned)

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 6.2+
- Docker 20.10+ (Optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-org/saas-reminder-service.git
cd saas-reminder-service
```

2. Set up backend dependencies:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. Set up frontend dependencies:
```bash
cd ../frontend
npm install
```

## Configuration

1. Create backend environment file:
```bash
cd backend
cp .env.example .env
```
Edit `.env` with your credentials:
```ini
DATABASE_URL=postgresql://user:password@localhost:5432/app_db
REDIS_URL=redis://localhost:6379
JWT_SECRET_KEY=your-secure-secret-here
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

2. Initialize database:
```bash
python create_tables.py
alembic upgrade head
```

## Running the Application

### Development Mode
Start backend:
```bash
flask run --port=8000 --debug
```

Start frontend:
```bash
cd frontend
npm start
```

### Docker Setup
```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- PGAdmin: http://localhost:5050
- Redis Commander: http://localhost:8081

## API Documentation

Access Swagger UI (after starting backend):
```bash
http://localhost:8000/api/docs
```

Example API Request:
```bash
curl -X GET "http://localhost:8000/api/v1/patients" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

### E2E Tests
```bash
docker-compose --profile testing up -d
docker-compose exec playwright npm test
```

## Deployment

### Production Considerations
- Use managed PostgreSQL (AWS RDS, Supabase)
- Configure Redis persistence
- Set up reverse proxy (Nginx)
- Implement monitoring (Prometheus/Grafana)
- Enable HTTPS with Let's Encrypt
- Configure proper JWT secret rotation

### Environment Variables
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| DATABASE_URL | PostgreSQL connection URL | Yes | - |
| JWT_SECRET_KEY | JWT signing key | Yes | - |
| REDIS_URL | Redis connection URL | No | redis://redis:6379 |
| GOOGLE_CLIENT_ID | Google OAuth client ID | No | - |
| GOOGLE_CLIENT_SECRET | Google OAuth client secret | No | - |

## Development Setup

### Code Style
- Python: PEP8 with Black formatting
- JavaScript: ESLint with Airbnb style guide
- SQL: SQLFluff

### Useful Commands
```bash
# Run database migrations
alembic revision --autogenerate -m "migration message"
alembic upgrade head

# Format code
cd backend && black .
cd frontend && npm run format

# Check dependency updates
pip list --outdated
npm outdated
```

## Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -am 'Add some feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open Pull Request

## License
MIT License (see [LICENSE](LICENSE) file)
