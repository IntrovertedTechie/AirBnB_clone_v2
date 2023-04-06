 #!/usr/bin/env bash

exec { 'update apt-get':
    command => '/usr/bin/apt-get -y update > /dev/null',
    path    => ['/bin', '/usr/bin'],
    unless  => '/usr/bin/dpkg-query -W --showformat=\'\${Status}\\n\' nginx | /bin/grep -q "install ok installed"',
}

package { 'nginx':
    ensure  => installed,
    require => Exec['update apt-get'],
}
file { '/data/web_static/releases':
  ensure => directory,
  mode   => '0755',
}

file { '/data/web_static/releases/test':
    ensure => directory,
    mode => '0755',
    recurse => true,
    require => File['/data/web_static/releases'],
}

file { '/data/web_static/shared':
    ensure => directory,
    mode => '0755',
    recurse => true,
    require => File['/data/web_static'],
}

file { '/data/web_static/releases/test/index.html':
    ensure => file,
    mode => '0644',
    content => "Hello Nginx!\n",
    require => File['/data/web_static/releases/test'],
    }




file { '/data/web_static/current':
    ensure  => link,
    target  => '/data/web_static/releases/test',
    require => File['/data/web_static'],
    before  => File['/etc/nginx/sites-enabled/default'],
}

file { '/data/web_static':
    ensure => directory,
}

file { '/etc/nginx/sites-enabled/default':
    ensure  => file,
    content => '
        server {
            listen 80;
            listen [::]:80 default_server;

            root /var/www/html;

            index index.html index.htm;

            server_name _;

            location /redirect_me {
                return 301 http://talenthive.tech/;
            }

            location /hbnb_static {
                alias /data/web_static/current/;
                index index.html index.htm;
            }

            error_page 404 /404.html;
            location /404 {
                internal;
                root /usr/share/nginx/html;
            }
        }
    ',
    require => File['/data/web_static/current'],
    notify  => Service['nginx'],
}




exec { 'change ownership of /data directory':
    command => '/bin/chown -R ubuntu:ubuntu /data',
    unless => '/usr/bin/test "$(stat -c %U:%G /data)" = "ubuntu:ubuntu"',
}


$config_file = '/etc/nginx/sites-available/talenthive.tech'
$content_dir = '/data/web_static/current'
$url_path = '/hbnb_static'



$file_content = "server {\n  listen 80;\n  server_name talenthive.tech;\n  location $url_path {\n    alias $content_dir;\n    index index.html;\n  }\n}"

file { $config_file:
    content => $file_content,
    require => Package['nginx'],
}

service { 'nginx':
    ensure => running,
    enable => true,
    require => File[$config_file],
    subscribe => File[$config_file],
}




