#!/bin/bash
echo "Starting SSH..."
service ssh start
echo "Starting TOR..."
tor -f /etc/tor/torrc &
sleep 5
echo "Starting Nginx..."
nginx -g "daemon off;" &

echo "Services started."

if [ -f /var/lib/tor/hidden_service/hostname ]; then
    echo "Onion service URL: http://$(cat /var/lib/tor/hidden_service/hostname)"
else
    echo "ERROR: Tor hidden service not created!"
    exit 1
fi

tail -f /var/log/nginx/error.log


