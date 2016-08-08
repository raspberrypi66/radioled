#!/bin/bash  
ifdown wlan0
cat /etc/network/interfaces.host > /etc/network/interfaces
ifup wlan0 
sleep 15
#&& sleep 10 && /etc/init.d/isc-dhcp-server start && sleep 3 && /etc/init.d/hostapd start
/etc/init.d/isc-dhcp-server start
/etc/init.d/hostapd start
/etc/init.d/isc-dhcp-server start
