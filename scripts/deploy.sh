#!/usr/bin/env bash
# Deploy dairy-cream-price-api to AWS Lambda via ECR.
# Usage: ./scripts/deploy.sh [aws-profile] [aws-region]
set -euo pipefail

AWS_PROFILE="${1:-default}"
AWS_REGION="${2:-us-east-1}"
APP_NAME="dairy-cream-price-api"

ACCOUNT_ID=$(aws sts get-caller-identity --profile "$AWS_PROFILE" --query Account --output text)
ECR_URI="${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${APP_NAME}"

echo "==> Step 1: init + apply ECR/IAM resources"
cd "$(dirname "$0")/../terraform"
terraform init -upgrade
terraform apply -target=aws_ecr_repository.app -target=aws_iam_role.lambda -auto-approve

echo "==> Step 2: authenticate Docker to ECR"
aws ecr get-login-password --region "$AWS_REGION" --profile "$AWS_PROFILE" \
  | docker login --username AWS --password-stdin "${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

echo "==> Step 3: build & push image"
cd ..
docker build --platform linux/amd64 -t "${APP_NAME}:latest" .
docker tag "${APP_NAME}:latest" "${ECR_URI}:latest"
docker push "${ECR_URI}:latest"

echo "==> Step 4: apply remaining resources (Lambda + API GW)"
cd terraform
terraform apply -auto-approve

echo ""
echo "Done. API URL:"
terraform output -raw api_url
