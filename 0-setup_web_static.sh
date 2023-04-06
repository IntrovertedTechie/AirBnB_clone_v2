
#!/usr/bin/env bash

# Bash script that sets up your web servers for the deployment of web_static

# Install Nginx if it not already installed
apt-get -y update > /dev/null
apt-get install -y nginx > /dev/null

# Create the necessary folders and files for web_static deployment
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared
touch /data/web_static/releases/test/index.html

# Create a fake HTML file to test Nginx configuration
echo "Hello Nginx!" >> /data/web_static/releases/test/index.html

# Check if the /data/web_static/current symbolic link already exists, and delete it if it does
if [ -L /data/web_static/current ]
then
    rm -f /data/web_static/current
fi

# Create the symbolic link
ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group
chown -R ubuntu:ubuntu /data/

# Define variables
config_file="/etc/nginx/sites-available/talenthive.tech"
content_dir="/data/web_static/current"
url_path="/hbnb_static"

# Update Nginx configuration file
cat > $config_file <<EOF
server {
    listen 80;
    server_name talenthive.tech;

    location $url_path {
        alias $content_dir;
        index index.html;
    }
}
EOF

# Restart Nginx
sudo service nginx restart



service nginx restart

