import time
from Klasses.HX711 import HX711


hx = HX711(17, 4)

def setup():
    hx.set_offset(8837890.4375)
    hx.set_scale(-820.756)
    hx.tare()

def loop():
    val = hx.get_grams()
    return val

    hx.power_down()
    time.sleep(.001)
    hx.power_up()

    time.sleep(2)


def get_weight():
    setup()

    for i in range(50):
        gewicht = loop()
        print(gewicht)


get_weight()