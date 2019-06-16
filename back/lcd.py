import time
from RPi import GPIO

from Klasses.IPaddress import IPaddress
from Klasses.LCDPCF import LCDPCF

SDA = 8
SCL = 7
E = 20
RS = 16

display = LCDPCF(SDA, SCL, E, RS, 64)


def setup():
    GPIO.setmode(GPIO.BCM)

ip = IPaddress()


myip = ip.get_IP()
deel1 = ip.get_IP().find('192')
deel2 = ip.get_IP().find(' ')
print(myip[deel1:deel2])









