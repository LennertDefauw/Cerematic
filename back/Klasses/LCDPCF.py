from RPi import GPIO
import time

class LCDPCF():

    def __init__(self, SDA, SCL, E, RS, ID):
        self.SDA = SDA
        self.SCL = SCL
        self.E = E
        self.RS = RS
        self.ID = ID

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(SDA, GPIO.OUT)
        GPIO.setup(SCL, GPIO.OUT)
        GPIO.setup(E, GPIO.OUT)
        GPIO.setup(RS, GPIO.OUT)

    def write_one_bit(self, bit):
        GPIO.output(self.SDA, bit)
        GPIO.output(self.SCL, 1)
        GPIO.output(self.SCL, 0)


    def write_one_byte(self, databyte):
        mask = 0x80
        for i in range(0,8):
            if(databyte&mask == 0):
                self.write_one_bit(0)
            else:
                self.write_one_bit(1)

            mask = mask >> 1

    def start(self, paramid):
        GPIO.output(self.SDA, 1)
        GPIO.output(self.SCL, 1)
        GPIO.output(self.SDA, 0)
        GPIO.output(self.SCL, 0)
        id = paramid
        self.write_one_byte(id)

    def stop(self):
        GPIO.output(self.SDA, 0)
        GPIO.output(self.SCL, 0)
        GPIO.output(self.SDA, 1)
        GPIO.output(self.SCL, 1)

    def ack(self):
        GPIO.setup(self.SDA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.output(self.SCL, 1)
        status = GPIO.input(self.SDA)
        GPIO.output(self.SCL, 0)
        GPIO.setup(self.SDA, GPIO.OUT)
        return status

    def write_item_to_pcf(self, id, databyte):
        self.start(id)
        status = self.ack()
        if(not status):
            self.write_one_byte(databyte)
            if(status):
                print("No acknowledge data")

        else:
            print("No acknowledge addresss")

        self.stop()

    #LCD FUNCTIES
    def send_instruction(self, value):
        GPIO.output(self.E, 1)
        GPIO.output(self.RS, 0)
        self.write_item_to_pcf(self.ID, value)
        GPIO.output(self.E, 0)
        time.sleep(0.01)

    def send_character(self, value):
        GPIO.output(self.E, 1)
        GPIO.output(self.RS, 1)
        self.write_item_to_pcf(self.ID, value)
        GPIO.output(self.E, 0)

    def LCD_init(self):
        self.send_instruction(0x38) #function instruction
        self.send_instruction(0x01) #clear display
        self.send_instruction(0xF) #display on
        self.send_instruction(0x3) #cursor home

    def send_line(self, line):
        self.LCD_init()

        for letter in line:
            self.send_character(ord(letter))

    def send_second_line(self, line):
        self.send_instruction(0xC0)
        for letter in line:
            self.send_character(ord(letter))

