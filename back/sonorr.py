import time

from Klasses.Sonor import Sonor

sonorlinks = Sonor(19,26)

while True:
    print(sonorlinks.get_distance())
    time.sleep(1)