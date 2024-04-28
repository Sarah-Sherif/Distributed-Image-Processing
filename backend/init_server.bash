# !/bin/bash

# Install required packages
sudo apt install -y python3-pip
sudo apt install -y python3-venv
sudo apt-get install ffmpeg libsm6 libxext6  -y

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