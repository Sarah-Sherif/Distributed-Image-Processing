# !/bin/bash

# Install Apache web server
sudo apt install apache2 -y

# Move the index.html file to the web server root directory
sudo cp /home/ubuntu/work/Distributed-Image-Processing/index.html /var/www/html