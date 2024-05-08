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
mkdir /home/ubuntu/work/Distributed-Image-Processing/backend
aws s3 cp s3://code-directory/ /home/ubuntu/work/Distributed-Image-Processing/ --recursive
echo "Code downloaded successfully."

# Init Apache
echo "Initializing Apache..."
chmod +x /home/ubuntu/work/Distributed-Image-Processing/init_apache.bash
/home/ubuntu/work/Distributed-Image-Processing/init_apache.bash

# Init the API
echo "Initializing WSGI server..."
chmod +x /home/ubuntu/work/Distributed-Image-Processing/init_server.bash
/home/ubuntu/work/Distributed-Image-Processing/init_server.bash

