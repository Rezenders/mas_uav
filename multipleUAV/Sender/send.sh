#!/bin/sh

echo "Setting hostname..."
echo "127.0.0.1 $HOSTNAME"
echo "127.0.0.1 $HOSTNAME" >> /etc/hosts

echo "Start sending"
python send.py

exec "$@"
