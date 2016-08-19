#!/bin/bash
kill $(ps -A -o cmd,pid | egrep "setWi" | head -n 1 | sed -r -e 's/.* ([0-9]+)$/\1/')
ifdown wlan0
cat /etc/network/interfaces.station > /etc/network/interfaces
/etc/init.d/hostapd stop 
/etc/init.d/isc-dhcp-server stop
ifup wlan0
while ! ping -c 1 -W 1 8.8.8.8; do
    echo "Waiting for online network interface might be down..."
    sleep 2
done

python /root/radioled/radio.py
