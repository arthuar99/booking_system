# AWS Deployment Files

This directory contains configuration files and scripts for deploying the Booking Platform to AWS.

## Files

- **`deploy.sh`** - Automated script to build and push Docker image to ECR
- **`ecs-task-definition.json`** - ECS Fargate task definition template
- **`apprunner.yaml`** - App Runner configuration (optional)

## Quick Start

### Option 1: AWS App Runner (Easiest)

1. **Push image to ECR:**
   ```bash
   ./aws/deploy.sh
   ```

2. **Create RDS database:**
   - Use AWS Console or CLI (see `docs/AWS_QUICK_START.md`)

3. **Create App Runner service:**
   - Go to AWS Console → App Runner
   - Use the ECR image you just pushed
   - Configure environment variables

### Option 2: ECS Fargate

1. **Push image to ECR:**
   ```bash
   ./aws/deploy.sh
   ```

2. **Update task definition:**
   - Edit `ecs-task-definition.json`
   - Replace `<ACCOUNT_ID>` and `<REGION>` with your values
   - Update environment variables

3. **Register and deploy:**
   ```bash
   aws ecs register-task-definition --cli-input-json file://aws/ecs-task-definition.json
   aws ecs create-service --cluster your-cluster --service-name booking-platform --task-definition booking-platform --launch-type FARGATE
   ```

## Documentation

- **Full Guide**: `docs/AWS_DEPLOYMENT.md`
- **Quick Start**: `docs/AWS_QUICK_START.md`

## GitHub Actions

The repository includes a GitHub Actions workflow (`.github/workflows/deploy-aws.yml`) that automatically:
- Builds Docker image on push to main
- Pushes to ECR
- Ready for ECS/App Runner deployment

**Required Secrets:**
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

## Environment Variables

Required for all deployments:
```
DATABASE_URL=postgresql://username:password@rds-endpoint:5432/booking_platform
SECRET_KEY=<generate-with: openssl rand -hex 32>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

