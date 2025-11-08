Booking Platform — Project Documentation

Overview

This repository contains a booking platform built with FastAPI and SQLAlchemy. The application exposes REST endpoints and server-rendered pages (Jinja2 templates). Authentication uses JWT tokens. The repository also includes Docker and Terraform assets for local development and optional AWS deployment.

Repository layout

- `app/` — FastAPI application code (routers, models, schemas, templates, static files)
- `aws/terraform/` — Terraform configuration (ECR, App Runner module)
- `.github/workflows/` — GitHub Actions CI and image build workflows
- `docker-compose.yml` — Local development compose file (web + postgres)
- `Dockerfile` — Container image specification for the web service
- `requirements.txt` — Python dependencies
- `docs/` — Additional documentation

Getting started (local development)

1. Prerequisites

   - Docker and Docker Compose (or Docker Desktop)
   - Python 3.12 (for local venv tasks)
   - Terraform (if you intend to provision AWS infra)
   - AWS CLI (optional; required for pushing images to ECR)

2. Environment variables

   - Copy `.env.example` to `.env` and fill values required by your environment.

3. Run locally with Docker Compose

```bash
# from repository root
docker compose up --build
```

- The web application will be available at `http://localhost:8000` by default.
- Apply database migrations after services are healthy:

```bash
docker compose exec web alembic upgrade head
```

4. Run the app locally without Docker (development)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Authentication

- The project uses JWT for authentication. The backend exposes `/auth/login` and `/auth/register` endpoints.
- The `app/core/deps.py` module includes `get_current_user` which validates the token and returns the current user. The function was extended to support tokens stored in cookies.

APIs and server-rendered pages

- Server-rendered templates are under `app/templates/` and static assets under `app/static/`.
- API routers are placed in `app/routers/`. See the `users`, `auth`, `services`, `booking`, and `availability` routers for available endpoints.

CI and CD

- GitHub Actions workflows are available under `.github/workflows/`:
  - `ci.yml` — installs dependencies, creates DB tables, runs smoke checks and tests if available.
  - `docker-image.yml` — builds and pushes Docker images to a container registry (requires secrets).
- The CI workflow supports manual runs via the `workflow_dispatch` trigger.

Infrastructure and deployment

- Terraform configuration is under `aws/terraform/`. It contains modules for creating an ECR repository and deploying an App Runner service.
- Typical deployment steps:
  1. `terraform -chdir=aws/terraform init`
  2. `terraform -chdir=aws/terraform apply -target=module.ecr -auto-approve`
  3. Build, tag and push the Docker image to ECR.
  4. `terraform -chdir=aws/terraform apply -auto-approve` to create the App Runner service.

Security notes

- Do not commit secrets or credentials. Use environment variables and GitHub secrets for CI.
- Use `HttpOnly`, `Secure`, and `SameSite` attributes for cookies when storing JWT tokens.
- Use a strong `SECRET_KEY` and rotate it periodically.

Troubleshooting

- Docker errors related to containerd or blob I/O indicate local Docker corruption; use Docker Desktop -> Troubleshoot -> Clean / Purge data, or reset to factory defaults.
- Terraform provider download timeouts can be caused by local network issues. Use a plugin cache directory (`TF_PLUGIN_CACHE_DIR`) or run Terraform from a stable environment (CI runner).

Where to go next

- Add unit and integration tests under `tests/` and enable CI to fail on test failures.
- Add a `.env.example` (provided) and wire environment variables into `docker-compose.yml`.
- Harden Terraform modules with IAM roles and remote state (S3 + DynamoDB).
