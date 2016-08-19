#!/usr/bin/env python
from bottle import route, run, template,request
from lib_oled96 import ssd1306
from PIL import ImageFont, ImageDraw, Image
from smbus import SMBus 
import socket
import fcntl
import struct
import subprocess

font = ImageFont.load_default()
i2cbus = SMBus(0) 
oled = ssd1306(i2cbus)                                                             
draw = oled.canvas   # "draw" onto this canvas, then call display() to send the canvas contents to the hardware.

def get_ip_address(ifname):                                                        
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                                                        
    try:                                                                                                        
     return socket.inet_ntoa(fcntl.ioctl(                                                                       
         s.fileno(),                                                                                            
         0x8915,                                                                                                
         struct.pack('256s', ifname[:15])                                                                       
     )[20:24])                                                                                                  
    except IOError:                                                                                             
     subprocess.Popen("/root/radioled/startAP.sh")                                                              
     return " -- not set --"   
                                                                                                                
draw.rectangle((0, 0, oled.width-1, oled.height-1), outline=20, fill=0)                                         
font = ImageFont.truetype('/root/radioled/FreeSans.ttf', 14)  
draw.text((0, 0), 'Wifi-Configuration', font=font, fill=1) 
draw.text((0, 25), 'Please browse to', font=font, fill=1)
draw.text((0, 45), 'IP:'+get_ip_address('wlan0'), font=font, fill=1)
oled.display() 
@route('/listWifi')
def index():
    playlist = subprocess.check_output("iwlist wlan0 scanning | grep ESSID | grep -o '\"[^\"]\+\"'", shell=True, stderr=subprocess.STDOUT)  
    playlist=playlist.splitlines()
    output="<form action=\"/setWifi\" method=post>SSID:<select name=ssid>"
    for ssid in playlist :
     output+=("<option value="+ssid+">"+ssid+"</option>") 
    output+="</select><br/>password<input type=password name=password><br/><input type=submit></form>"
    return ('<b>Choose you WiFi</b><br/>'+output+"")

@route('/setWifi',method='POST')
def setWifi():
    ssid = request.forms.get('ssid')
    password = request.forms.get('password')
    print ssid
    print password
    if(ssid!='' and password!=''):
     subprocess.call("wpa_passphrase \""+ssid+"\" "+password+" >> /etc/wpa_supplicant/wpa_supplicant.conf ",shell=True)
     subprocess.Popen("/root/radioled/startStation.sh")
    return ('please wait for restart network!')
run(host='', port=8080)
