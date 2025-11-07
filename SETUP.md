# Booking Platform Setup Guide

## Prerequisites

- Docker Desktop installed and running
- Git (for cloning the repository)

## Quick Start with Docker

1. **Ensure Docker Desktop is running**
   ```bash
   docker info
   ```
   If this fails, start Docker Desktop and wait for it to fully initialize.

2. **Create environment file (optional)**
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

3. **Start the application**
   ```bash
   ./start.sh
   ```
   Or manually:
   ```bash
   docker compose up -d --build
   ```

4. **Access the application**
   - Web interface: http://localhost:8000
   - API docs: http://localhost:8000/docs
   - Database: localhost:5432

## Environment Variables

Create a `.env` file in the project root with:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/booking_platform
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**Note:** When using Docker Compose, the `DATABASE_URL` will automatically use `db` as the hostname instead of `localhost`.

## Docker Commands

### Start services
```bash
docker compose up -d
```

### View logs
```bash
docker compose logs -f
docker compose logs -f web    # Web service only
docker compose logs -f db      # Database service only
```

### Stop services
```bash
docker compose down
```

### Stop and remove volumes (clean slate)
```bash
docker compose down -v
```

### Rebuild after code changes
```bash
docker compose up -d --build
```

### Execute commands in container
```bash
docker compose exec web bash
docker compose exec web python -m alembic upgrade head
```

### Check service status
```bash
docker compose ps
```

## Development Without Docker

1. **Install Python 3.12** and create a virtual environment:
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL** locally and update `.env` with your database URL

4. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Troubleshooting

### Docker daemon not running
- Open Docker Desktop
- Wait 30-60 seconds for it to fully start
- If issues persist, reset Docker Desktop: Settings → Troubleshoot → Reset to factory defaults

### Port already in use
- Change ports in `docker-compose.yml` if 8000 or 5432 are already in use

### Database connection errors
- Ensure the database service is healthy: `docker compose ps`
- Check database logs: `docker compose logs db`
- Verify environment variables are set correctly

### Application won't start
- Check application logs: `docker compose logs web`
- Verify all dependencies are installed
- Ensure database is ready before the web service starts

## Project Structure

```
booking_platform/
├── app/
│   ├── core/          # Core configuration and utilities
│   ├── database/      # Database connection and session management
│   ├── models/        # SQLAlchemy models
│   ├── routers/       # API route handlers
│   ├── schemas/       # Pydantic schemas
│   ├── static/        # Static files (CSS, JS)
│   └── templates/     # Jinja2 templates
├── docker-compose.yml # Docker Compose configuration
├── Dockerfile         # Docker image definition
└── requirements.txt    # Python dependencies
```

## CI/CD

The project includes GitHub Actions workflows:
- **CI** (`.github/workflows/ci.yml`): Runs on push/PR to main branch
- Tests, linting, and application health checks

## Security Notes

- **Never commit** `.env` files to version control
- Change default `SECRET_KEY` in production
- Use strong database passwords in production
- Consider using Docker secrets or a secrets manager for production deployments

