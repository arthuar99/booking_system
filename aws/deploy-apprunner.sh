#!/bin/bash

# Quick App Runner Deployment Script
# This creates an App Runner service from your ECR image

set -e

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
ECR_REPO_NAME=${ECR_REPO_NAME:-booking-platform}
SERVICE_NAME=${SERVICE_NAME:-booking-platform}
AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID:-""}

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 App Runner Deployment${NC}"
echo "=========================="
echo ""

# Get AWS account ID
if [ -z "$AWS_ACCOUNT_ID" ]; then
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
fi

ECR_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:latest"

echo "This script will help you create an App Runner service."
echo ""
echo "Image URI: $ECR_URI"
echo ""
echo -e "${YELLOW}⚠️  You'll need to provide:${NC}"
echo "1. RDS database endpoint"
echo "2. Database credentials"
echo "3. SECRET_KEY (generate with: openssl rand -hex 32)"
echo ""

read -p "Do you have an RDS database ready? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "First, create an RDS database:"
    echo ""
    echo "aws rds create-db-instance \\"
    echo "  --db-instance-identifier booking-platform-db \\"
    echo "  --db-instance-class db.t3.micro \\"
    echo "  --engine postgres \\"
    echo "  --master-username admin \\"
    echo "  --master-user-password YourPassword123! \\"
    echo "  --allocated-storage 20 \\"
    echo "  --publicly-accessible \\"
    echo "  --region $AWS_REGION"
    echo ""
    echo "Then run this script again."
    exit 0
fi

echo ""
read -p "Enter RDS endpoint (e.g., xxxxx.us-east-1.rds.amazonaws.com): " RDS_ENDPOINT
read -p "Enter database username: " DB_USER
read -sp "Enter database password: " DB_PASS
echo ""
read -p "Enter database name [booking_platform]: " DB_NAME
DB_NAME=${DB_NAME:-booking_platform}

# Generate SECRET_KEY if not provided
echo ""
read -p "Enter SECRET_KEY (or press Enter to generate): " SECRET_KEY
if [ -z "$SECRET_KEY" ]; then
    SECRET_KEY=$(openssl rand -hex 32)
    echo "Generated SECRET_KEY: $SECRET_KEY"
fi

DATABASE_URL="postgresql://$DB_USER:$DB_PASS@$RDS_ENDPOINT:5432/$DB_NAME"

echo ""
echo "Creating App Runner service..."
echo "This may take a few minutes..."

# Create App Runner service using AWS CLI
aws apprunner create-service \
  --service-name "$SERVICE_NAME" \
  --source-configuration "{
    \"ImageRepository\": {
      \"ImageIdentifier\": \"$ECR_URI\",
      \"ImageConfiguration\": {
        \"Port\": \"8000\",
        \"RuntimeEnvironmentVariables\": {
          \"DATABASE_URL\": \"$DATABASE_URL\",
          \"SECRET_KEY\": \"$SECRET_KEY\",
          \"ALGORITHM\": \"HS256\",
          \"ACCESS_TOKEN_EXPIRE_MINUTES\": \"60\"
        }
      },
      \"ImageRepositoryType\": \"ECR\"
    },
    \"AutoDeploymentsEnabled\": true
  }" \
  --instance-configuration "{
    \"Cpu\": \"1 vCPU\",
    \"Memory\": \"2 GB\"
  }" \
  --region "$AWS_REGION" \
  > /tmp/apprunner-output.json

SERVICE_ARN=$(cat /tmp/apprunner-output.json | grep -o '"ServiceArn": "[^"]*' | cut -d'"' -f4)
SERVICE_ID=$(echo $SERVICE_ARN | cut -d'/' -f2)

echo ""
echo -e "${GREEN}✅ App Runner service created!${NC}"
echo ""
echo "Service ID: $SERVICE_ID"
echo ""
echo "Getting service URL (this may take a moment)..."
sleep 5

# Get service URL
SERVICE_URL=$(aws apprunner describe-service \
  --service-arn "$SERVICE_ARN" \
  --region "$AWS_REGION" \
  --query 'Service.ServiceUrl' \
  --output text 2>/dev/null || echo "Service is still provisioning...")

if [ "$SERVICE_URL" != "Service is still provisioning..." ]; then
    echo ""
    echo -e "${GREEN}🌐 Your application is available at:${NC}"
    echo "   https://$SERVICE_URL"
    echo ""
    echo "Note: It may take 5-10 minutes for the service to be fully ready."
else
    echo ""
    echo "Service is provisioning. Check status:"
    echo "aws apprunner describe-service --service-arn $SERVICE_ARN --region $AWS_REGION"
    echo ""
    echo "Or visit: https://console.aws.amazon.com/apprunner/"
fi

