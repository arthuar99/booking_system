#!/bin/bash

# AWS Deployment Script for Booking Platform
# This script helps deploy to AWS ECR and optionally to ECS/App Runner

set -e

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
ECR_REPO_NAME=${ECR_REPO_NAME:-booking-platform}
AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID:-""}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 AWS Deployment Script${NC}"
echo "================================"
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI is not installed${NC}"
    echo "Install it from: https://aws.amazon.com/cli/"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker is not running${NC}"
    exit 1
fi

# Get AWS account ID if not provided
if [ -z "$AWS_ACCOUNT_ID" ]; then
    echo "Getting AWS account ID..."
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    if [ -z "$AWS_ACCOUNT_ID" ]; then
        echo -e "${RED}❌ Could not get AWS account ID. Is AWS CLI configured?${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✓${NC} AWS Account ID: $AWS_ACCOUNT_ID"
echo -e "${GREEN}✓${NC} Region: $AWS_REGION"
echo -e "${GREEN}✓${NC} Repository: $ECR_REPO_NAME"
echo ""

# Step 1: Create ECR repository if it doesn't exist
echo "Step 1: Checking ECR repository..."
if aws ecr describe-repositories --repository-names $ECR_REPO_NAME --region $AWS_REGION &> /dev/null; then
    echo -e "${GREEN}✓${NC} ECR repository already exists"
else
    echo "Creating ECR repository..."
    aws ecr create-repository --repository-name $ECR_REPO_NAME --region $AWS_REGION
    echo -e "${GREEN}✓${NC} ECR repository created"
fi

# Step 2: Login to ECR
echo ""
echo "Step 2: Logging in to ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
echo -e "${GREEN}✓${NC} Logged in to ECR"

# Step 3: Build Docker image
echo ""
echo "Step 3: Building Docker image..."
docker build -t $ECR_REPO_NAME:latest .
echo -e "${GREEN}✓${NC} Docker image built"

# Step 4: Tag image
echo ""
echo "Step 4: Tagging image..."
ECR_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:latest"
docker tag $ECR_REPO_NAME:latest $ECR_URI
echo -e "${GREEN}✓${NC} Image tagged: $ECR_URI"

# Step 5: Push to ECR
echo ""
echo "Step 5: Pushing image to ECR..."
docker push $ECR_URI
echo -e "${GREEN}✓${NC} Image pushed to ECR"

echo ""
echo -e "${GREEN}✅ Deployment to ECR completed!${NC}"
echo ""
echo "Next steps:"
echo "1. Update ECS task definition with image: $ECR_URI"
echo "2. Or create App Runner service using this image"
echo "3. Or update existing ECS service"
echo ""
echo "Image URI: $ECR_URI"

