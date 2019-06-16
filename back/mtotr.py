import time
from RPi import GPIO

MotorRechtsEnable = 9
MotorRechtsInput = 10

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MotorRechtsInput, GPIO.OUT)
    GPIO.setup(MotorRechtsEnable, GPIO.OUT)


setup()

GPIO.output(MotorRechtsEnable, 1)
GPIO.output(MotorRechtsInput, 1)
time.sleep(20)
GPIO.output(MotorRechtsInput,0)