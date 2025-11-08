# Booking System

A cloud-ready booking platform built with FastAPI, SQLAlchemy, JWT authentication, and PostgreSQL.  
Containerized with Docker & docker-compose. Infrastructure managed with Terraform on AWS (ECR & App Runner).

---

## Features

- FastAPI backend with user, service, booking, availability & review models
- JWT authentication (access tokens, role-based protection)
- Profile management API
- Server-rendered frontend with Jinja2 templates
- Docker & docker-compose setup for local/dev environments
- CI/CD with GitHub Actions (build & push Docker images, test hooks)
- Infrastructure as Code with Terraform (ECR, App Runner modules)
- Full documentation & deployment scripts

---

## Quick Start

1. **Clone the repo:**
   ```bash
   git clone https://github.com/arthuar99/booking_system.git
   cd booking_system
