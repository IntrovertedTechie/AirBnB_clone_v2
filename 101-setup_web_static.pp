 #!/usr/bin/env bash
# Puppet manifest that sets up your web servers for the deployment of web_static

# Install Nginx if it not already installed
package { 'nginx':
  ensure => installed,
}

# Create the necessary folders and files for web_static deployment
file { ['/data/web_static/releases/test', '/data/web_static/shared']:
  ensure => directory,
}

file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => 'Hello Nginx!',
}

# Check if the /data/web_static/current symbolic link already exists, and delete it if it does
file { '/data/web_static/current':
  ensure => absent,
  force  => true,
}

# Create the symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test/',
}

# Give ownership of the /data/ folder to the ubuntu user and group
file { '/data':
  owner => 'ubuntu',
  group => 'ubuntu',
  recurse => true,
}

# Configure Nginx to serve web_static content
file_line { 'add_hbnb_static_location':
  path  => '/etc/nginx/sites-available/default',
  line  => "location /hbnb_static/ {\n\talias /data/web_static/current/;\n}",
  match => '^\s*location \/ {$',
}

service { 'nginx':
  ensure => running,
  enable => true,
  require => Package['nginx'],
}

