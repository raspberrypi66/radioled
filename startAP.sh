#!/bin/bash 
kill $(ps -A -o cmd,pid | egrep "radio" | head -n 1 | sed -r -e 's/.* ([0-9]+)$/\1/') 
ifdown wlan0
cat /etc/network/interfaces.host > /etc/network/interfaces
ifup wlan0 

while ! ping -c 1 -W 1 192.168.10.1; do
    echo "Waiting for 192.168.10.1 - network interface might be down..."
    sleep 2
done

#&& sleep 10 && /etc/init.d/isc-dhcp-server start && sleep 3 && /etc/init.d/hostapd start
/etc/init.d/isc-dhcp-server stop
sleep 2
/etc/init.d/isc-dhcp-server start
sleep 2
/etc/init.d/hostapd stop
sleep 2
/etc/init.d/hostapd start
sleep 2
python /root/radioled/setWifi.py
