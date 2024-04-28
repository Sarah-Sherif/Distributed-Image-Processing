#!/bin/bash

# Update package lists
sudo apt update

# Install unzip (if not already installed)
sudo apt install -y unzip

# Install AWS CLI (if not already installed)
if ! command -v aws &> /dev/null
then
    echo "AWS CLI is not installed. Installing..."
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    echo "AWS CLI installed successfully."
else
    echo "AWS CLI is already installed."
fi

# Download code from S3
echo "Downloading code from S3..."
mkdir ~/work/Distributed-Image-Processing/backend
aws s3 sync s3://code-directory/backend ~/work/Distributed-Image-Processing/backend
echo "Code downloaded successfully."

# Init the API
echo "Initializing API..."
chmod +x ~/work/Distributed-Image-Processing/backend/init_server.bash
~/work/Distributed-Image-Processing/backend/init_server.bash

