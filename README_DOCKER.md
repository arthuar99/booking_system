# Docker & CI for Booking Platform

Quick guide to run the application with Docker and the CI workflows.

## Local development with Docker Compose

1. Build and start:

```bash
docker-compose up --build
```

2. The API will be available at http://localhost:8000

3. Run database migrations (inside container):

```bash
docker-compose exec web alembic upgrade head
```

## GitHub Actions

- `ci.yml` runs on push and pull requests to `main`. It installs dependencies and can run tests.
- `docker-image.yml` builds and pushes the Docker image to DockerHub. It requires `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` repository secrets.
