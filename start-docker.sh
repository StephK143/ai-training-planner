#!/bin/bash

# Stop any running containers
docker compose down

# Remove any existing volumes (optional, comment out if you want to keep data)
# docker compose down -v

# Build the images
docker compose build --no-cache

# Start the services
docker compose up
