#!/bin/bash

if [ ! -f /etc/ssl/certs/nginx.crt ]; then
openssl req -x509 -nodes -days 365 -newkey rsa:4096 -keyout /etc/nginx/ssl/privkey.pem -out /etc/nginx/ssl/fullchain.pem -subj "/C=TR/ST=Istanbul/L=Istanbul/O=local/CN=peng.com.tr";
echo "Nginx: ssl is set up!";
fi

exec "$@"