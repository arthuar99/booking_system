# AWS Quick Start Guide

## Fastest Deployment: AWS App Runner

### Prerequisites
- AWS Account
- AWS CLI configured (`aws configure`)
- Docker installed locally

### 5-Minute Deployment

#### 1. Push Image to ECR (2 minutes)

```bash
# Run the deployment script
./aws/deploy.sh

# Or manually:
export AWS_REGION=us-east-1
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create ECR repo
aws ecr create-repository --repository-name booking-platform --region $AWS_REGION

# Login and push
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
docker build -t booking-platform .
docker tag booking-platform:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/booking-platform:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/booking-platform:latest
```

#### 2. Create RDS Database (2 minutes)

```bash
# Create RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier booking-platform-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password YourStrongPassword123! \
  --allocated-storage 20 \
  --publicly-accessible \
  --region us-east-1

# Wait for database to be available (takes 5-10 minutes)
aws rds wait db-instance-available --db-instance-identifier booking-platform-db --region us-east-1

# Get endpoint
aws rds describe-db-instances --db-instance-identifier booking-platform-db --query 'DBInstances[0].Endpoint.Address' --output text
```

#### 3. Create App Runner Service (1 minute)

1. Go to [AWS App Runner Console](https://console.aws.amazon.com/apprunner/)
2. Click "Create service"
3. Select "Container registry" → "Amazon ECR"
4. Choose your repository and image
5. Service name: `booking-platform`
6. CPU: 1 vCPU, Memory: 2 GB
7. Port: 8000
8. Add environment variables:
   ```
   DATABASE_URL=postgresql://admin:YourStrongPassword123!@<rds-endpoint>:5432/booking_platform
   SECRET_KEY=<generate-with: openssl rand -hex 32>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```
9. Click "Create & deploy"

#### 4. Access Your Application

- App Runner will provide a URL like: `https://xxxxx.us-east-1.awsapprunner.com`
- Your app will be available in 5-10 minutes

---

## Alternative: One-Command ECS Deployment

### Using AWS CLI

```bash
# 1. Push image (from deploy.sh or manually)
./aws/deploy.sh

# 2. Register task definition
aws ecs register-task-definition --cli-input-json file://aws/ecs-task-definition.json

# 3. Create cluster (if doesn't exist)
aws ecs create-cluster --cluster-name booking-platform-cluster

# 4. Create service
aws ecs create-service \
  --cluster booking-platform-cluster \
  --service-name booking-platform-service \
  --task-definition booking-platform \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

---

## Cost Comparison

| Service | Monthly Cost | Best For |
|---------|-------------|----------|
| **App Runner** | ~$25-50 | Quick deployment, auto-scaling |
| **ECS Fargate** | ~$30-60 | More control, custom networking |
| **EC2** | ~$15-30 | Cost optimization, full control |

**RDS PostgreSQL**: ~$15-30/month (db.t3.micro)

---

## Required AWS Secrets for GitHub Actions

If using the GitHub Actions workflow (`.github/workflows/deploy-aws.yml`):

1. Go to GitHub repo → Settings → Secrets and variables → Actions
2. Add these secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

To create AWS access keys:
```bash
# Create IAM user with ECR permissions
aws iam create-user --user-name github-actions
aws iam attach-user-policy --user-name github-actions --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess
aws iam create-access-key --user-name github-actions
```

---

## Troubleshooting

### Image push fails
- Check AWS credentials: `aws sts get-caller-identity`
- Verify ECR repository exists
- Check IAM permissions

### App won't start
- Check CloudWatch logs in App Runner/ECS
- Verify DATABASE_URL is correct
- Check RDS security group allows connections

### Database connection fails
- Verify RDS is publicly accessible (for App Runner)
- Check security group allows port 5432
- Verify username/password are correct

---

## Next Steps After Deployment

1. **Set up custom domain** (Route 53)
2. **Enable HTTPS** (automatic with App Runner)
3. **Set up monitoring** (CloudWatch)
4. **Configure backups** (RDS automated backups)
5. **Set up CI/CD** (GitHub Actions workflow)

