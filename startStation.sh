#!/bin/bash
ifdown wlan0
cat /etc/network/interfaces.station > /etc/network/interfaces
/etc/init.d/hostapd stop 
/etc/init.d/isc-dhcp-server stop
ifup wlan0
