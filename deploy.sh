#!/bin/bash
set -e
# === Configuration ===
REMOTE_HOST="ubuntu@54.172.53.178"

COMPOSE_DIR="/home/ubuntu/librarysystem"

if [ -z "$1" ]; then
  echo "Error: IMAGE_TAG not provided."
  echo "Usage: ./deploy.sh <image-tag>"
  exit 1
fi

IMAGE_TAG="$1"
# === SSH Command ===
ssh -o StrictHostKeyChecking=no "$REMOTE_HOST" << EOF
  cd "$COMPOSE_DIR"
  echo "IMAGE_TAG=$IMAGE_TAG" > .env
  echo "$IMAGE_TAG"
  echo "Bringing down service"
  sudo docker-compose -p library-ci -f docker-compose-ci.yml down
  echo "Updating image"
  sudo docker-compose -p library-ci -f docker-compose-ci.yml pull
  echo "Starting service"
  sudo docker-compose -p library-ci -f docker-compose-ci.yml up -d
  echo "Deployment complete."
EOF
