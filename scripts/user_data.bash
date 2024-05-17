# update the code
sudo aws s3 cp s3://code-directory/ /home/ubuntu/work/Distributed-Image-Processing/ --recursive

# move the new index.html and index.js to /var/www/html
sudo cp /home/ubuntu/work/Distributed-Image-Processing/index.* /var/www/html/

# restart app
sudo systemctl restart app