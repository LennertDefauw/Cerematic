import time
from RPi import GPIO

class Sonor():
    def __init__(self, TRIG, ECHO):
        #De pinmodes instellen adhv parameters
        self.TRIG = TRIG
        self.ECHO = ECHO

        self.pulse_start = 0
        self.pulse_end = 0
        self.pulse_duration = 0
        self.distance = 0

        #BCM pinmode gebruiken
        GPIO.setmode(GPIO.BCM)

        #De trigger is de output, echo input
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)


    def read_info(self):
        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)

        while(GPIO.input(self.ECHO) == 0):
            self.pulse_start = time.time()

        while(GPIO.input(self.ECHO) == 1):
            self.pulse_end = time.time()


    def calculate_distance(self):
        self.pulse_duration = self.pulse_end - self.pulse_start

        self.distance = self.pulse_duration * 17150

        self.distance = round(self.distance, 2)


    def get_distance(self):
        self.read_info()
        self.calculate_distance()
        return self.distance

    def get_inhoudpercentage(self):
        distance = self.get_distance()
        value = (1 - distance / 20.5) * 100
        if(value > 0):
            return value
        else:
            return 0