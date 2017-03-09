#!/usr/bin/python
# Example using a character LCD connected to a Raspberry Pi or BeagleBone Black.
import time

import Adafruit_CharLCD as LCD

def getifip(ifn):
   import socket,fcntl,struct
   sck = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
   return socket.inet_ntoa(fcntl.ioctl(sck.fileno(),0x8915,struct.pack('256s',bytes(ifn[:15], 'utf-8')))[20:24])
   print(socket.gethostbyname(socket.gethostname()))
# Raspberry Pi pin configuration:
lcd_rs        = 17  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 27
lcd_d4        = 22
lcd_d5        = 24
lcd_d6        = 23
lcd_d7        = 18
lcd_backlight = 4

# BeagleBone Black configuration:
# lcd_rs        = 'P8_8'
# lcd_en        = 'P8_10'
# lcd_d4        = 'P8_18'
# lcd_d5        = 'P8_16'
# lcd_d6        = 'P8_14'
# lcd_d7        = 'P8_12'
# lcd_backlight = 'P8_7'

# Define LCD column and row size for 16x2 LCD.
#lcd_columns = 16
#lcd_rows    = 2

# Alternatively specify a 20x4 LCD.
lcd_columns = 20
lcd_rows    = 4

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

# Print a two line message
lcd.message('Getting Ip Address')
my_ip=getifip('wlan0')
print(my_ip)

# Wait 5 seconds
time.sleep(2.0)

# Demo showing the cursor.

lcd.clear()

lcd.message('IP %s' % (my_ip))



