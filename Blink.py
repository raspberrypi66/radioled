#!/usr/bin/python

# Codeing By IOXhop : www.ioxhop.com
# Sonthaya Nongnuch : www.fb.me/maxthai

import time
from Arduino import *

pin = 203

def main():
	pinMode(pin, OUTPUT)
	
	while True:
		digitalWrite(pin, HIGH)
		delay(500)
		digitalWrite(pin, LOW)
		delay(500):q!

if __name__ == '__main__':
    main()