from Klasses.Button import Button
import time
from RPi import GPIO

MotorLinksEnable = 9
MotorLinksInput = 10
MotorRechtsEnable = 5
MotorRechtsInput = 11

GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(MotorRechtsEnable, GPIO.OUT)  # All pins as Outputs
GPIO.setup(MotorRechtsInput, GPIO.OUT)
GPIO.setup(MotorLinksEnable, GPIO.OUT)
GPIO.setup(MotorLinksInput, GPIO.OUT)

def myInterrupt(channel):
    start_time = time.time()

    while GPIO.input(channel) == 0: # Wait for the button up
        GPIO.output(MotorRechtsEnable, 1)
        GPIO.output(MotorRechtsInput, 1)

    GPIO.output(MotorRechtsInput, 0)

    buttonTime = time.time() - start_time    # How long was the button down?

    if .1 <= buttonTime < 4:  # Ignore noise
        print('klein')  # 1= brief push

    elif 2 <= buttonTime < 6:
        print('middel')  # 2=

    elif buttonTime >= 8:
        print('groot')  # 3= really long push

GPIO.add_event_detect(15, GPIO.FALLING, callback=myInterrupt, bouncetime=500)

while True:
    time.sleep(50)
