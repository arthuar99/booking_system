Deployment Guide

This document describes steps to deploy the Booking Platform to AWS using Terraform and App Runner. It assumes you have AWS credentials configured and `terraform` installed.

1. Provision infrastructure (ECR and App Runner)

```bash
cd aws/terraform
terraform init
# create ECR repo first
terraform apply -target=module.ecr -auto-approve
```

2. Build and push the Docker image to ECR

```bash
# get the ECR repository URL from Terraform
REPO_URL=$(terraform output -raw ecr_repository_url)
# login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${REPO_URL%%/*}
# build and tag
docker build -t booking_platform:latest .
docker tag booking_platform:latest ${REPO_URL}:latest
# push
docker push ${REPO_URL}:latest
```

3. Deploy the service

```bash
terraform apply -auto-approve
```

4. Apply database migrations

- If you provisioned RDS, set `DATABASE_URL` locally with the RDS endpoint and run:

```bash
alembic upgrade head
```

Notes

- Configure Terraform remote state for team usage.
- Ensure App Runner has permissions to pull from ECR or create an IAM role for it.
