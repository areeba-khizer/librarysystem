#!/bin/bash
 
set -e
 
# === Configuration ===
REMOTE_HOST="ubuntu@54.172.53.178"
COMPOSE_DIR="/home/ubuntu/librarysystem"
 
# === SSH Command ===
ssh -i -o StrictHostKeyChecking=no "$REMOTE_HOST" << EOF
  cd "$COMPOSE_DIR"
  echo "Bringing down service"
  sudo docker-compose -p library-ci -f docker-compose-ci.yml down
  echo "Updating image"
  sudo docker-compose -p library-ci -f docker-compose-ci.yml pull
  echo "Starting service"
  sudo docker-compose -p library-ci -f docker-compose-ci.yml up
