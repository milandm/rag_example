#!/bin/bash

# Variables
IMAGE_NAME="your_image_name"
IMAGE_TAG="your_image_tag"
IMAGE_TAR_PATH="docker_image/\${IMAGE_NAME}_\${IMAGE_TAG}.tar"
IMAGE_FULL_NAME="\${IMAGE_NAME}:\${IMAGE_TAG}"

# Debug: Print the variables
echo "IMAGE_NAME: \$IMAGE_NAME"
echo "IMAGE_TAG: \$IMAGE_TAG"
echo "IMAGE_TAR_PATH: \$IMAGE_TAR_PATH"
echo "IMAGE_FULL_NAME: \$IMAGE_FULL_NAME"

# Check if the image tar file exists
if [ -f "\$IMAGE_TAR_PATH" ]; then
  echo "Loading image from tar file..."
  docker load -i "\$IMAGE_TAR_PATH"
else
  echo "Building image..."
  # Debug: Print the build command before execution
  echo "docker build -t \$IMAGE_FULL_NAME -f ./Dockerfile ."
  docker build -t "\$IMAGE_FULL_NAME" -f ./Dockerfile .
  echo "Saving new image to tar file..."
  mkdir -p docker_image
  # Debug: Print the save command before execution
  echo "docker save -o \$IMAGE_TAR_PATH \$IMAGE_FULL_NAME"
  docker save -o "\$IMAGE_TAR_PATH" "\$IMAGE_FULL_NAME"
fi