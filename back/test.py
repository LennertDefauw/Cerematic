from Klasses.Button import Button
import time

button = Button(14)

def test(channel):
    print("test")

button.on_press(test)

while True:
    time.sleep(100)