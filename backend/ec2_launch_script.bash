#!/bin/bash

# Update package lists
sudo apt update
sudo apt install -y python3-pip
sudo apt install -y python3-venv

# OpenCL related dependancies
apt-get install ffmpeg libsm6 libxext6  -y

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
aws s3 sync s3://code-directory ~/work/Distributed-Image-Processing/backend
echo "Code downloaded successfully."

# Go to backend directory and create virtual environment
cd ~/work/Distributed-Image-Processing/backend
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt
pip3 install gunicorn

# Start the server
gunicorn -w 4 -b 0.0.0.0 app:app