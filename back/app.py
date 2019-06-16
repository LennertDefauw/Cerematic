from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from Klasses.Database import Database
from Klasses.HX711 import HX711
from Klasses.IPaddress import IPaddress
from Klasses.Sonor import Sonor
import time
from RPi import GPIO
from Klasses.LCDPCF import LCDPCF

SDA = 8
SCL = 7
E = 20
RS = 16

detectorrechts = 18
detectorlinks = 23

display = LCDPCF(SDA, SCL, E, RS, 64)

status = 0

app = Flask(__name__)

RedPin = 24
GreenPin = 25
BluePin = 12

DetectorLinks = 23
DetectorRechts = 18

sonorLinks = Sonor(6, 13)
sonorRechts = Sonor(19, 26)

HX711Links = HX711(22, 27)
HX711Rechts = HX711(17, 4)

MotorLinksEnable = 9
MotorLinksInput = 10
MotorRechtsEnable = 5
MotorRechtsInput = 11

buttonrechts = 14
buttonlinks = 15

socketio = SocketIO(app)
CORS(app)

ip = IPaddress()

conn = Database(app=app, user="root", password="#root123", db="dbcerematic", host="localhost", port=3306)

endpoint = '/api/v1'


###############HELPMETHODES######################

def callbackrechts(channel):
    start_time = time.time()

    while GPIO.input(channel) == 0:
        GPIO.output(MotorLinksEnable, 1)
        GPIO.output(MotorLinksInput, 1)

    GPIO.output(MotorLinksInput, 0)

    buttonTime = time.time() - start_time

    data = conn.get_data("SELECT cornflakesID from reservoir where reservoirID = 2")
    cornflakesid = data[0]["cornflakesID"]

    if .1 <= buttonTime < 4:
        conn.set_data("INSERT INTO portie(cornflakesID, grootte, datum, reservoirID) VALUES('%s', 'Klein', NOW(), 2)" % cornflakesid)

    elif 2 <= buttonTime < 6:
        conn.set_data("INSERT INTO portie(cornflakesID, grootte, datum, reservoirID) VALUES('%s', 'Gemiddeld', NOW(), 2)" % cornflakesid)

    elif buttonTime >= 8:
        conn.set_data("INSERT INTO portie(cornflakesID, grootte, datum, reservoirID) VALUES('%s', 'Groot', NOW(), 2)" % cornflakesid)

    myip = ip.get_IP()
    deel1 = ip.get_IP().find('172')
    deel2 = ip.get_IP().find(' ')
    display.send_line("Connection IP:")
    display.send_second_line(myip[deel1:deel2])

def callbacklinks(channel):
    start_time = time.time()

    while GPIO.input(channel) == 0:
        GPIO.output(MotorRechtsEnable, 1)
        GPIO.output(MotorRechtsInput, 1)

    GPIO.output(MotorRechtsInput, 0)

    buttonTime = time.time() - start_time

    data = conn.get_data("SELECT cornflakesID from reservoir where reservoirID = 1")
    cornflakesid = data[0]["cornflakesID"]

    if .1 <= buttonTime < 4:
        conn.set_data("INSERT INTO portie(cornflakesID, grootte, datum, reservoirID) VALUES('%s', 'Klein', NOW(), 1)" % cornflakesid)

    elif 2 <= buttonTime < 6:
        conn.set_data("INSERT INTO portie(cornflakesID, grootte, datum, reservoirID) VALUES('%s', 'Gemiddeld', NOW(), 1)" % cornflakesid)

    elif buttonTime >= 8:
        conn.set_data("INSERT INTO portie(cornflakesID, grootte, datum, reservoirID) VALUES('%s', 'Groot', NOW(), 1)" % cornflakesid)

    myip = ip.get_IP()
    deel1 = ip.get_IP().find('172')
    deel2 = ip.get_IP().find(' ')
    display.send_line("Connection IP:")
    display.send_second_line(myip[deel1:deel2])

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RedPin, GPIO.OUT)
    GPIO.setup(GreenPin, GPIO.OUT)
    GPIO.setup(BluePin, GPIO.OUT)

    GPIO.setup(DetectorLinks, GPIO.IN)
    GPIO.setup(DetectorRechts, GPIO.IN)

    GPIO.setup(MotorRechtsEnable, GPIO.OUT)  # All pins as Outputs
    GPIO.setup(MotorRechtsInput, GPIO.OUT)
    GPIO.setup(MotorLinksEnable, GPIO.OUT)
    GPIO.setup(MotorLinksInput, GPIO.OUT)

    GPIO.setup(buttonrechts, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(buttonlinks, GPIO.IN, GPIO.PUD_UP)


setup()

GPIO.add_event_detect(buttonrechts, GPIO.FALLING, callback=callbackrechts, bouncetime=500)
GPIO.add_event_detect(buttonlinks, GPIO.FALLING, callback=callbacklinks, bouncetime=500)



def showIp():
    time.sleep(5)
    myip = ip.get_IP()
    deel1 = ip.get_IP().find('172')
    deel2 = ip.get_IP().find(' ')

    display.send_line(myip[deel1:deel2])


showIp()

def setupHX711(object, offset, scale):
    object.set_offset(offset)
    object.set_scale(scale)
    object.tare()


def get_data_HX711(hx711):
    val = hx711.get_grams()
    return val

    hx711.power_down()
    time.sleep(.001)
    hx711.power_up()


def get_weight_HX711(hx711):
    gewicht = get_data_HX711(hx711)
    return gewicht



pwm_rood = GPIO.PWM(RedPin, 100)
pwm_groen = GPIO.PWM(GreenPin, 100)
pwm_blauw = GPIO.PWM(BluePin, 100)


def get_rgb(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))


def check_komLinks():
    global valueLinks

    if (GPIO.input(DetectorLinks) == 0):
        return 'Aanwezig'
    else:
        return 'Afwezig'


def check_komRechts():
    global valueRechts

    if (GPIO.input(DetectorRechts) == 0):
        return 'Aanwezig'
    else:
        return 'Afwezig'


def check_distanceLinks():
    afstandlinks = sonorLinks.get_inhoudpercentage()
    return afstandlinks


def check_distanceRechts():
    afstandrechts = sonorRechts.get_inhoudpercentage()
    return afstandrechts


def check_soort(id):
    data = conn.get_data(
        "SELECT c.naam FROM reservoir as r JOIN cornflakes as c on c.cornflakesid = r.cornflakesid WHERE r.reservoirID = '%s'" % id)
    return data

@app.route('/')
def return_hello():
    return 'hello'

@app.route('/api/v1/cornflakes', methods=["GET"])
def get_cornflakes():
    data = conn.get_data("SELECT * from cornflakes")
    return jsonify(data)

@socketio.on('useMotor')
def useMotor(data):
    portie = data["portie"]
    motor = data["motor"]

    if (portie == "Klein"):
        if (motor == "links"):
            display.send_line('Kleine portie ...')
            display.send_second_line('Dispenser A')

            GPIO.output(MotorLinksEnable, GPIO.HIGH)
            GPIO.output(MotorLinksInput, GPIO.HIGH)
            time.sleep(4)
            GPIO.output(MotorLinksInput, GPIO.LOW)

            myip = ip.get_IP()
            deel1 = ip.get_IP().find('172')
            deel2 = ip.get_IP().find(' ')
            display.send_line("Connection IP:")
            display.send_second_line(myip[deel1:deel2])


            data = conn.get_data("SELECT cornflakesID from reservoir where reservoirID = 1")
            cornflakesid = data[0]["cornflakesID"]
            conn.set_data(
                "INSERT INTO portie(cornflakesID, grootte, datum, reservoirID) VALUES('%s', 'Klein', NOW(), 1)" % cornflakesid)
        else:
            display.send_line('Kleine portie ...')
            display.send_second_line('Dispenser B')

            GPIO.output(MotorRechtsEnable, GPIO.HIGH)
            GPIO.output(MotorRechtsInput, GPIO.HIGH)
            time.sleep(4)
            GPIO.output(MotorRechtsInput, GPIO.LOW)

            myip = ip.get_IP()
            deel1 = ip.get_IP().find('172')
            deel2 = ip.get_IP().find(' ')
            display.send_line("Connection IP:")
            display.send_second_line(myip[deel1:deel2])

            data = conn.get_data("SELECT cornflakesID from reservoir where reservoirID = 2")
            cornflakesid = data[0]["cornflakesID"]
            conn.set_data(
                "INSERT INTO portie(cornflakesID, grootte, datum, reservoirID) VALUES('%s', 'Klein', NOW(), 2)" % cornflakesid)

    if (portie == "Gemiddeld"):
        if (motor == "links"):
            display.send_line('Medium portie ...')
            display.send_second_line('Dispenser A')

            GPIO.output(MotorLinksEnable, GPIO.HIGH)
            GPIO.output(MotorLinksInput, GPIO.HIGH)
            time.sleep(6)
            GPIO.output(MotorLinksInput, GPIO.LOW)

            myip = ip.get_IP()
            deel1 = ip.get_IP().find('172')
            deel2 = ip.get_IP().find(' ')
            display.send_line("Connection IP:")
            display.send_second_line(myip[deel1:deel2])

            data = conn.get_data("SELECT cornflakesID from reservoir where reservoirID = 1")
            cornflakesid = data[0]["cornflakesID"]
            conn.set_data(
                "INSERT INTO portie(cornflakesID, grootte, datum, reservoirID) VALUES('%s', 'Gemiddeld', NOW(), 1)" % cornflakesid)
        else:
            display.send_line('Medium portie ...')
            display.send_second_line('Dispenser B')

            GPIO.output(MotorRechtsEnable, GPIO.HIGH)
            GPIO.output(MotorRechtsInput, GPIO.HIGH)
            time.sleep(6)
            GPIO.output(MotorRechtsInput, GPIO.LOW)

            myip = ip.get_IP()
            deel1 = ip.get_IP().find('172')
            deel2 = ip.get_IP().find(' ')
            display.send_line("Connection IP:")
            display.send_second_line(myip[deel1:deel2])

            data = conn.get_data("SELECT cornflakesID from reservoir where reservoirID = 2")
            cornflakesid = data[0]["cornflakesID"]
            conn.set_data(
                "INSERT INTO portie(cornflakesID, grootte, datum, reservoirID) VALUES('%s', 'Gemiddeld', NOW(), 2)" % cornflakesid)

    if (portie == "Groot"):
        if (motor == "links"):
            display.send_line('Grote portie ...')
            display.send_second_line('Dispenser A')

            GPIO.output(MotorLinksEnable, GPIO.HIGH)
            GPIO.output(MotorLinksInput, GPIO.HIGH)
            time.sleep(8)
            GPIO.output(MotorLinksInput, GPIO.LOW)

            myip = ip.get_IP()
            deel1 = ip.get_IP().find('172')
            deel2 = ip.get_IP().find(' ')
            display.send_line("Connection IP:")
            display.send_second_line(myip[deel1:deel2])

            data = conn.get_data("SELECT cornflakesID from reservoir where reservoirID = 1")
            cornflakesid = data[0]["cornflakesID"]
            conn.set_data(
                "INSERT INTO portie(cornflakesID, grootte, datum, reservoirID) VALUES('%s', 'Groot', NOW(), 1)" % cornflakesid)
        else:
            display.send_line('Grote portie ...')
            display.send_second_line('Dispenser B')

            GPIO.output(MotorRechtsEnable, GPIO.HIGH)
            GPIO.output(MotorRechtsInput, GPIO.HIGH)
            time.sleep(8)
            GPIO.output(MotorRechtsInput, GPIO.LOW)

            myip = ip.get_IP()
            deel1 = ip.get_IP().find('172')
            deel2 = ip.get_IP().find(' ')
            display.send_line("Connection IP:")
            display.send_second_line(myip[deel1:deel2])

            data = conn.get_data("SELECT cornflakesID from reservoir where reservoirID = 2")
            cornflakesid = data[0]["cornflakesID"]
            conn.set_data(
                "INSERT INTO portie(cornflakesID, grootte, datum, reservoirID) VALUES('%s', 'Groot', NOW(), 2)" % cornflakesid)


@socketio.on('refreshLinks')
def refresh_links():
    statusLinks = check_komLinks()
    soortLinks = check_soort(1)
    afstandLinks = check_distanceLinks()
    gewichtLinks = get_weight_HX711(HX711Links)

    afstandLinksString = str(round(afstandLinks, 2)) + '%'
    conn.set_data("INSERT INTO meting(sensorID, waarde, datum, reservoirID) VALUES (5, '%s', NOW(), 1)" % statusLinks)
    conn.set_data(
        "INSERT INTO meting(sensorID, waarde, datum, reservoirID) VALUES (3, '%s', NOW(), 1)" % afstandLinksString)
    conn.set_data(
        "INSERT INTO meting(sensorID, waarde, datum, reservoirID) VALUES (1, '%s', NOW(), 1)" % int(gewichtLinks))

    socketio.emit('refreshLinks', {'statuslinks': statusLinks, 'soortlinks': soortLinks, 'afstandlinks': afstandLinks,
                                   'gewichtlinks': gewichtLinks})


@socketio.on('refreshRechts')
def refresh_rechts():
    statusRechts = check_komRechts()
    soortRechts = check_soort(2)
    afstandRechts = check_distanceRechts()
    gewichtRechts = get_weight_HX711(HX711Rechts)

    afstandRechtsString = str(round(afstandRechts, 2)) + '%'
    conn.set_data("INSERT INTO meting(sensorID, waarde, datum, reservoirID) VALUES (5, '%s', NOW(), 2)" % statusRechts)
    conn.set_data(
        "INSERT INTO meting(sensorID, waarde, datum, reservoirID) VALUES (3, '%s', NOW(), 2)" % afstandRechtsString)
    conn.set_data(
        "INSERT INTO meting(sensorID, waarde, datum, reservoirID) VALUES (1, '%s', NOW(), 2)" % int(gewichtRechts))

    socketio.emit('refreshRechts',
                  {'statusrechts': statusRechts, 'soortrechts': soortRechts, 'afstandrechts': afstandRechts,
                   'gewichtrechts': gewichtRechts})


@socketio.on('connectLinks')
def connectLinks():
    statusLinks = check_komLinks()
    soortLinks = check_soort(1)
    afstandLinks = check_distanceLinks()
    setupHX711(HX711Links, 8522636.4375, -854.22)
    gewichtLinks = get_weight_HX711(HX711Links)

    afstandLinksString = str(round(afstandLinks, 2)) + '%'
    conn.set_data("INSERT INTO meting(sensorID, waarde, datum, reservoirID) VALUES (5, '%s', NOW(), 1)" % statusLinks)
    conn.set_data(
        "INSERT INTO meting(sensorID, waarde, datum, reservoirID) VALUES (3, '%s', NOW(), 1)" % afstandLinksString)
    conn.set_data(
        "INSERT INTO meting(sensorID, waarde, datum, reservoirID) VALUES (1, '%s', NOW(), 1)" % int(gewichtLinks))

    socketio.emit('connectLinks', {'statuslinks': statusLinks, 'soortlinks': soortLinks, 'afstandlinks': afstandLinks,
                                   'gewichtlinks': gewichtLinks})

@socketio.on('connectRechts')
def connectRechts():
    statusRechts = check_komRechts()
    soortRechts = check_soort(2)
    afstandRechts = check_distanceRechts()
    setupHX711(HX711Rechts, 8837890.4375, -820.756)
    gewichtRechts = get_weight_HX711(HX711Rechts)

    socketio.emit('connectRechts',
                  {'statusrechts': statusRechts, 'soortrechts': soortRechts, 'afstandrechts': afstandRechts,
                   'gewichtrechts': gewichtRechts})
    afstandRechtsString = str(round(afstandRechts, 2)) + '%'

    conn.set_data("INSERT INTO meting(sensorID, waarde, datum, reservoirID) VALUES (5, '%s', NOW(), 2)" % statusRechts)
    conn.set_data(
        "INSERT INTO meting(sensorID, waarde, datum, reservoirID) VALUES (3, '%s', NOW(), 2)" % afstandRechtsString)
    conn.set_data(
        "INSERT INTO meting(sensorID, waarde, datum, reservoirID) VALUES (1, '%s', NOW(), 2   )" % int(gewichtRechts))


@socketio.on('insertName')
def insert_cornflakes(data):
    naam = data["naam"]
    conn.set_data("INSERT INTO cornflakes(naam) VALUES ('%s')" % naam)
    socketio.emit('successAdd')


@socketio.on('changeCornflakesLinks')
def update_reservoir(data):
    id = data["id"]
    conn.set_data("UPDATE reservoir set cornflakesID = '%s' where reservoirID = 1" % id)
    socketio.emit('successChange')

@socketio.on('changeCornflakesRechts')
def update_reservoir(data):
    id = data["id"]
    conn.set_data("UPDATE reservoir set cornflakesID = '%s' where reservoirID = 2" % id)
    socketio.emit('successChange')

@socketio.on('powerup')
def toggle_power(value):
    global status

    string = str(value["value"])
    value = get_rgb(string)
    rood = int(value[0])
    roodvalue = rood * 100 / 255
    groen = int(value[1])
    groenvalue = groen * 100 / 255
    blauw = int(value[2])
    blauwvalue = blauw * 100 / 255

    setup()

    pwm_rood.start(100)
    pwm_groen.start(100)
    pwm_blauw.start(100)

    if (status == 0):
        status = 1
        socketio.emit('powerup', {'status': status})
        pwm_rood.ChangeDutyCycle(roodvalue)
        pwm_groen.ChangeDutyCycle(groenvalue)
        pwm_blauw.ChangeDutyCycle(blauwvalue)
    else:
        status = 0
        socketio.emit('powerup', {'status': status})
        pwm_rood.ChangeDutyCycle(0)
        pwm_groen.ChangeDutyCycle(0)
        pwm_blauw.ChangeDutyCycle(0)


@socketio.on('rgb')
def toggle_power(value):
    global status
    string = str(value["value"])
    value = get_rgb(string)
    rood = int(value[0])
    roodvalue = rood * 100 / 255
    groen = int(value[1])
    groenvalue = groen * 100 / 255
    blauw = int(value[2])
    blauwvalue = blauw * 100 / 255

    setup()

    pwm_rood.start(100)
    pwm_groen.start(100)
    pwm_blauw.start(100)

    if (status == 1):
        socketio.emit('powerup', {'status': status})
        pwm_rood.ChangeDutyCycle(roodvalue)
        pwm_groen.ChangeDutyCycle(groenvalue)
        pwm_blauw.ChangeDutyCycle(blauwvalue)
    else:
        socketio.emit('powerup', {'status': status})
        pwm_rood.ChangeDutyCycle(0)
        pwm_groen.ChangeDutyCycle(0)
        pwm_blauw.ChangeDutyCycle(0)


@socketio.on('statusLicht')
def start_kleuren():
    if (status == 0):

        socketio.emit('statusLicht', {'status': 0})
    else:

        socketio.emit('statusLicht', {'status': 1})


##########################ADD HEADERS #########################
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# Start app
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
