# Install nginx with Puppet

exec { 'Nginx':
  command  =>'sudo apt -y update && sudo apt -y install nginx && echo "Hello World" > /var/www/html/index.html && new_string="server_name _;\n\trewrite ^\/redirect_me https:\/\/www.github.com\/tallninja permanent;" && sed -i "s/server_name _;/$new_string/" /etc/nginx/sites-available/default && service nginx restart',
  provider => 'shell',
}
