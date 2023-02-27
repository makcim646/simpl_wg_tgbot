#!/bin/bash

set -e

# Check if CLIENT_NAME argument is provided
if [ -z "$1" ]; then
    echo "Error: CLIENT_NAME argument is not provided"
    exit 1
fi

#get pwd
pwd=$(pwd)

# Remove client from the server configuration
sed -i "/^# BEGIN_PEER $1/,/^# END_PEER $1/d" /etc/wireguard/wg0.conf

# Remove client configuration file
rm -f "$pwd/conf/$1.conf"

# Remove client QR code file
rm -f "$pwd/png/$1.png"

# Reload the WireGuard configuration
wg syncconf wg0 <(wg-quick strip wg0)

echo "Client $1 successfully removed from WireGuard"
