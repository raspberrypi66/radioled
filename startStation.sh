#!/bin/bash
kill $(ps -A -o cmd,pid | egrep "setWifi" | head -n 1 | sed -r -e 's/.* ([0-9]+)$/\1/')
ifdown wlan0
cat /etc/network/interfaces.station > /etc/network/interfaces
/etc/init.d/hostapd stop 
/etc/init.d/isc-dhcp-server stop
ifup wlan0
