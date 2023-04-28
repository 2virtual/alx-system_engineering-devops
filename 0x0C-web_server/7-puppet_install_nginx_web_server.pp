# Install nginx with Puppet

class nginx_config {
  package { 'nginx':
    ensure => installed,
  }

  file { '/etc/nginx/sites-available/default':
    content => "
server {
    listen 80;
    root /var/www/html;
    index index.html;
    location / {
        return 301 /hello;
    }
    location /hello {
        add_header Content-Type text/plain;
        return 200 'Hello World!';
    }
}
",
  }

  file { '/var/www/html/index.html':
    ensure  => file,
    content => "<html><body>Hello World!</body></html>",
  }

  service { 'nginx':
    ensure => running,
    enable => true,
    require => File['/etc/nginx/sites-available/default'],
  }
}

include nginx_config
