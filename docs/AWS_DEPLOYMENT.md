# AWS Deployment Guide

This guide covers multiple AWS deployment options for the Booking Platform.

## Table of Contents
1. [AWS App Runner (Recommended - Easiest)](#aws-app-runner)
2. [AWS ECS with Fargate](#aws-ecs-with-fargate)
3. [AWS EC2](#aws-ec2)
4. [Database Setup (RDS PostgreSQL)](#database-setup-rds-postgresql)
5. [Environment Variables](#environment-variables)

---

## AWS App Runner (Recommended - Easiest)

**Best for:** Quick deployment, automatic scaling, minimal configuration

### Prerequisites
- AWS Account
- Docker image pushed to ECR (Elastic Container Registry) or DockerHub
- RDS PostgreSQL instance (see Database Setup section)

### Steps

#### 1. Push Docker Image to ECR

```bash
# Install AWS CLI if not already installed
# Configure AWS credentials
aws configure

# Create ECR repository
aws ecr create-repository --repository-name booking-platform --region us-east-1

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and tag image
docker build -t booking-platform .
docker tag booking-platform:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/booking-platform:latest

# Push to ECR
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/booking-platform:latest
```

#### 2. Create App Runner Service

1. Go to AWS Console → App Runner
2. Click "Create service"
3. Choose "Container registry" → "Amazon ECR"
4. Select your repository and image
5. Configure service:
   - **Service name**: `booking-platform`
   - **Virtual CPU**: 1 vCPU
   - **Memory**: 2 GB
   - **Port**: 8000
   - **Environment variables**: (see Environment Variables section)
6. Configure auto-scaling (optional)
7. Create service

#### 3. Configure Environment Variables

In App Runner service settings, add:
```
DATABASE_URL=postgresql://username:password@rds-endpoint:5432/booking_platform
SECRET_KEY=your-production-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## AWS ECS with Fargate

**Best for:** More control, custom networking, production workloads

### Prerequisites
- AWS Account
- Docker image in ECR
- RDS PostgreSQL instance
- VPC and Security Groups configured

### Steps

#### 1. Create ECR Repository and Push Image

```bash
# Same as App Runner step 1
aws ecr create-repository --repository-name booking-platform --region us-east-1
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker build -t booking-platform .
docker tag booking-platform:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/booking-platform:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/booking-platform:latest
```

#### 2. Create Task Definition

Use the provided `aws/ecs-task-definition.json` or create via console:

1. Go to ECS → Task Definitions → Create new
2. Configure:
   - **Task definition family**: `booking-platform`
   - **Launch type**: Fargate
   - **CPU**: 1024 (1 vCPU)
   - **Memory**: 2048 (2 GB)
   - **Container**: 
     - Image: `<account-id>.dkr.ecr.us-east-1.amazonaws.com/booking-platform:latest`
     - Port: 8000
     - Environment variables: (see Environment Variables section)

#### 3. Create ECS Service

1. Go to ECS → Clusters → Create cluster
2. Choose "Fargate" networking
3. Create service:
   - **Task definition**: `booking-platform`
   - **Service name**: `booking-platform-service`
   - **Number of tasks**: 2 (for high availability)
   - **Load balancer**: Application Load Balancer (optional but recommended)

#### 4. Configure Load Balancer (Optional)

1. Create Application Load Balancer
2. Configure target group (port 8000)
3. Add health check: `/` or `/docs`
4. Attach to ECS service

---

## AWS EC2

**Best for:** Full control, custom configurations, cost optimization

### Steps

#### 1. Launch EC2 Instance

1. Go to EC2 → Launch Instance
2. Choose Ubuntu 22.04 LTS or Amazon Linux 2023
3. Instance type: t3.medium or larger
4. Configure security group:
   - SSH (22) from your IP
   - HTTP (80) from anywhere
   - HTTPS (443) from anywhere
   - Custom TCP (8000) from anywhere (or ALB only)

#### 2. Install Docker on EC2

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@<ec2-ip>

# Install Docker
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
newgrp docker

# Install AWS CLI (optional, for pulling from ECR)
sudo apt-get install -y awscli
```

#### 3. Deploy Application

```bash
# Clone repository
git clone https://github.com/your-username/booking_system.git
cd booking_system

# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://username:password@rds-endpoint:5432/booking_platform
SECRET_KEY=your-production-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
EOF

# Build and run
docker compose up -d --build
```

#### 4. Set Up Nginx Reverse Proxy (Recommended)

```bash
# Install Nginx
sudo apt-get install -y nginx

# Configure Nginx
sudo nano /etc/nginx/sites-available/booking-platform
```

Add configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/booking-platform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. Set Up SSL with Let's Encrypt

```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## Database Setup (RDS PostgreSQL)

### Create RDS Instance

1. Go to RDS → Create database
2. Choose PostgreSQL 15
3. Configuration:
   - **DB instance identifier**: `booking-platform-db`
   - **Master username**: `admin` (or your choice)
   - **Master password**: Strong password (save this!)
   - **DB instance class**: db.t3.micro (free tier) or db.t3.small
   - **Storage**: 20 GB (or as needed)
   - **VPC**: Default or your VPC
   - **Public access**: Yes (for App Runner) or No (for ECS/EC2 in VPC)
   - **Security group**: Create new or use existing

### Configure Security Group

1. Go to EC2 → Security Groups
2. Find your RDS security group
3. Add inbound rule:
   - **Type**: PostgreSQL
   - **Port**: 5432
   - **Source**: Your application security group or specific IP

### Get Connection String

After RDS is created, get the endpoint:
```
Endpoint: booking-platform-db.xxxxx.us-east-1.rds.amazonaws.com
Port: 5432
```

Connection string format:
```
postgresql://username:password@booking-platform-db.xxxxx.us-east-1.rds.amazonaws.com:5432/booking_platform
```

### Initialize Database

```bash
# Connect to RDS (from your local machine or EC2)
psql -h booking-platform-db.xxxxx.us-east-1.rds.amazonaws.com -U admin -d booking_platform

# Or use Docker
docker run -it --rm postgres:15 psql -h booking-platform-db.xxxxx.us-east-1.rds.amazonaws.com -U admin -d booking_platform

# Run migrations (if using Alembic)
# Or tables will be created automatically on first app start
```

---

## Environment Variables

### Required Variables

```bash
DATABASE_URL=postgresql://username:password@rds-endpoint:5432/booking_platform
SECRET_KEY=your-strong-secret-key-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Generating SECRET_KEY

```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -hex 32
```

### Setting in AWS

**App Runner:**
- Service → Configuration → Environment variables

**ECS:**
- Task Definition → Container definitions → Environment variables

**EC2:**
- Create `.env` file or use systemd environment file

---

## Security Best Practices

1. **Never commit secrets** to Git
2. **Use AWS Secrets Manager** for production:
   ```bash
   aws secretsmanager create-secret \
     --name booking-platform/secrets \
     --secret-string '{"DATABASE_URL":"...","SECRET_KEY":"..."}'
   ```
3. **Use IAM roles** instead of access keys when possible
4. **Enable VPC** for database (private subnet)
5. **Use SSL/TLS** for all connections
6. **Regular backups** of RDS database
7. **Enable CloudWatch** logging and monitoring

---

## Monitoring and Logging

### CloudWatch Logs

- **App Runner**: Automatic logging to CloudWatch
- **ECS**: Configure log driver in task definition
- **EC2**: Install CloudWatch agent

### Health Checks

- Application: `http://your-app/` or `http://your-app/docs`
- Database: RDS automatic health checks

---

## Cost Estimation

### App Runner
- ~$25-50/month for 1 vCPU, 2GB RAM (always running)

### ECS Fargate
- ~$30-60/month for 2 tasks (1 vCPU, 2GB each)

### EC2
- ~$15-30/month for t3.medium instance

### RDS
- ~$15-30/month for db.t3.micro (free tier eligible)
- ~$30-60/month for db.t3.small

**Total estimated cost**: $40-120/month depending on configuration

---

## Troubleshooting

### Application won't start
- Check CloudWatch logs
- Verify environment variables
- Check database connectivity
- Verify security group rules

### Database connection errors
- Check RDS security group allows connections
- Verify DATABASE_URL format
- Check RDS is in same VPC (for ECS/EC2)

### High costs
- Use smaller instance sizes
- Enable auto-scaling down
- Use RDS free tier
- Consider reserved instances

---

## Next Steps

1. Set up CI/CD to automatically deploy on push
2. Configure custom domain with Route 53
3. Set up monitoring alerts
4. Configure backup strategy
5. Set up staging environment

