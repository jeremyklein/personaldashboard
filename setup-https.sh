#!/bin/bash
set -e

# This script sets up HTTPS for your DigitalOcean Droplet
# Usage: ./setup-https.sh yourdomain.com

if [ $# -ne 1 ]; then
  echo "Usage: $0 yourdomain.com"
  exit 1
fi

DOMAIN=$1
IP=$(curl -s http://checkip.amazonaws.com)
EMAIL="admin@${DOMAIN}"

echo "Setting up HTTPS for domain: $DOMAIN (IP: $IP)"

# Update the NGINX config with your domain
sed -i "s/domain.com/${DOMAIN}/g" nginx/default.conf
sed -i "s/server_name _;/server_name ${DOMAIN};/g" nginx/default.conf

# Update environment variables
grep -q "DOMAIN=" .env || echo "DOMAIN=${DOMAIN}" >> .env
sed -i "s/ALLOWED_HOSTS=.*/ALLOWED_HOSTS=${DOMAIN},${IP}/g" .env

# Create initial dummy certificate
mkdir -p ./certbot/conf/live/${DOMAIN}
mkdir -p ./certbot/www

# Start containers
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d nginx

# Get SSL certificate
echo "Requesting Let's Encrypt certificate for ${DOMAIN}..."
docker-compose -f docker-compose.prod.yml run --rm certbot certonly --webroot \
  --webroot-path=/var/www/certbot \
  --email ${EMAIL} \
  --agree-tos \
  --no-eff-email \
  --force-renewal \
  -d ${DOMAIN}

# Restart containers
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d

echo "HTTPS setup complete! Your site should be available at https://${DOMAIN}"
echo "Make sure your domain's DNS A record points to ${IP}"