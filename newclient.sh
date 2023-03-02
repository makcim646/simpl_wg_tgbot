#!/bin/bash

set -e

# Check if CLIENT_NAME argument is provided
if [ -z "$1" ]; then
    echo "Error: CLIENT_NAME argument is not provided"
    exit 1
fi

# Get the next available internal IPv4 address for the client
octet=2
while grep AllowedIPs /etc/wireguard/wg0.conf | cut -d "." -f 4 | cut -d "/" -f 1 | grep -q "$octet"; do
    (( octet++ ))
done

if [ "$octet" -eq 255 ]; then
    echo "Error: WireGuard internal subnet is full"
    exit 1
fi

#get pwd
pwd=$(pwd)

#chek folders
if [ ! -d "$pwd/conf" ]; then
  mkdir $pwd/conf
fi
if [ ! -d "$pwd/png" ]; then
  mkdir $pwd/png
fi


# Generate the keys and PSK
key=$(wg genkey)
psk=$(wg genpsk)

# Configure client in the server
cat << EOF >> /etc/wireguard/wg0.conf
# BEGIN_PEER $1
[Peer]
PublicKey = $(echo $key | wg pubkey)
PresharedKey = $psk
AllowedIPs = 10.7.0.$octet/32, $(yggdrasilctl getSelf | awk '/IPv6 subnet/{print $3}' | cut -d '/' -f 1)$octet/128
# END_PEER $1
EOF

# Create client configuration
cat << EOF > "$pwd/conf/$1.conf"
[Interface]
Address = 10.7.0.$octet/24, $(yggdrasilctl getSelf | awk '/IPv6 subnet/{print $3}' | cut -d '/' -f 1)$octet/64
DNS = 8.8.8.8, 1.1.1.1
PrivateKey = $key

[Peer]
PublicKey = $(awk '/PrivateKey/{print $3}' /etc/wireguard/wg0.conf | wg pubkey)
PresharedKey = $psk
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = $(awk '/ENDPOINT/{print $3}' /etc/wireguard/wg0.conf):$(awk '/ListenPort/{print $3}' /etc/wireguard/wg0.conf)
PersistentKeepalive = 25
EOF

# Generate QR code for the client configuration
qrencode -l L < $pwd/conf/$1.conf -o $pwd/png/$1.png

# Reload the WireGuard configuration
wg addconf wg0 <(sed -n "/^# BEGIN_PEER $1/,/^# END_PEER $1/p" /etc/wireguard/wg0.conf)

echo "Client $1 successfully added to WireGuard"
