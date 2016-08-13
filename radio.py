#!/usr/bin/env python

# RASPBERRY PI VERSION

# NOTE: You need to have PIL installed for your python at the Pi

from lib_oled96 import ssd1306
from time import sleep
import time
import socket
import fcntl
import struct
from PIL import ImageFont, ImageDraw, Image
import mpd
 
client = mpd.MPDClient()
client.connect("127.0.0.1", 6600)
client.play(0) 
#cs = client.status()
#print cs['time']

font = ImageFont.load_default()


from smbus import SMBus                  #  These are the only two variant lines !!
i2cbus = SMBus(0)                        #
# 1 = Raspberry Pi but NOT early REV1 board
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915, 
        struct.pack('256s', ifname[:15])
    )[20:24])

oled = ssd1306(i2cbus)
draw = oled.canvas   # "draw" onto this canvas, then call display() to send the canvas contents to the hardware.

draw.rectangle((0, 0, oled.width-1, oled.height-1), outline=20, fill=0)
font = ImageFont.truetype('/root/radioled/FreeSans.ttf', 14)
draw.text((0, 0), 'You\'re Listening to', font=font, fill=1)
draw.text((0, 15), 'Cat Radio Online', font=font, fill=1)
#draw.text((0, 30), "Time: %s" %time.strftime("%H:%M:%S"), font=font, fill=1)
draw.text((0, 45), 'IP:'+get_ip_address('wlan0'), font=font, fill=1)
oled.display()

loopCheck=0
previousTime=0

while True:
 draw.rectangle((0, 45, oled.width-1, 30), outline=0, fill=0)
 draw.text((0, 30), "Time: %s" %time.strftime("%H:%M:%S"), font=font, fill=1) 
 oled.display()
 sleep(0.5)
 if(loopCheck>6):
  loopCheck=0
  cs = client.status()
  if(cs['time'] is not None):
   if(cs['time'] ==  previousTime):
    client.play(0)
   else:
    previousTime=cs['time']
    sleep(1)
  
 loopCheck+=1

