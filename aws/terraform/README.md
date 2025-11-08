# Terraform Infrastructure for Booking Platform

This folder contains Terraform modules and configuration to provision AWS infrastructure required to run the Booking Platform.

## Overview

- `modules/ecr` — creates an Amazon ECR repository and enables image scanning on push.
- `modules/apprunner` — deploys the application image to AWS App Runner.

## Quick start

1. Configure AWS credentials in your environment (e.g., `aws configure` or environment variables).
2. Initialize Terraform:

```bash
terraform -chdir=aws/terraform init
```

3. Plan and apply:

```bash
terraform -chdir=aws/terraform plan -out plan.tfplan
terraform -chdir=aws/terraform apply plan.tfplan
```

## Variables

- `region` — AWS region (default: `us-east-1`)
- `ecr_name` — name for the ECR repository
- `image_tag` — image tag to deploy (default: `latest`)
