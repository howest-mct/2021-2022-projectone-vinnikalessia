##################### IMPORT #####################
from repositories.DataRepository import DataRepository
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify, request
from numpy import False_, broadcast
from selenium import webdriver
from logging import exception
from flask_cors import CORS
from smbus import SMBus
from RPi import GPIO
import threading
import spidev
import json
import time

##################### MY IMPORT #####################
from hulpcode.joystick import Joy_klasse
from hulpcode.touch import Touch_klasse


##################### GLOBALE VARIABELEN ######################
global sw_val, x_val, y_val

########### JOYSTICK ###########
# deze hangen aan de mcp
y_as1 = 0
x_as1 = 1
y_as2 = 2
x_as2 = 3

# de sw van de joystick aan de rpi
sw1 = 5
sw2 = 6

# teller aantal keer sw ingedrukt
teller16 = 0
last_val16 = 0
prev_teller16 = 0

teller19 = 0
last_val19 = 0
prev_teller19 = 0

########### TOUCHSENSOR ###########
t1 = 13
t2 = 19

# teller aantal keer getouched
teller7 = 0 # t1
teller8 = 0 # t2

##################### BUSSEN #####################
# de spi-bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.open(0,1)
spi.max_speed_hz = 10 ** 5

i2c = SMBus()
i2c.open(1)

##################### FLASK #####################
# start app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'

socketio = SocketIO(app, cors_allowed_origins="*", 
    logger=False, engineio_logger=False, ping_timeout=1)


CORS(app)
print("program started")


##################### SETUP #####################
def setup():
    print("setup")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # joystick 1
    GPIO.setup(sw1, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(x_as1, GPIO.IN)
    GPIO.setup(y_as1, GPIO.IN)
    GPIO.add_event_detect(sw1, GPIO.FALLING, callback_sw1, bouncetime = 1000)
    
    # joystick 2
    GPIO.setup(sw2, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(x_as2, GPIO.IN)
    GPIO.setup(y_as2, GPIO.IN)
    GPIO.add_event_detect(sw2, GPIO.FALLING, callback_sw2, bouncetime = 1000)

    # touchsensoren
    GPIO.setup(t1, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(t2, GPIO.IN, GPIO.PUD_UP)

##################### CALLBACK #####################
def callback_sw1(pin):
    global teller16
    teller16 += 1
    print("Knop joystick 1 is {} keer ingedrukt\n".format(teller16))
    # socketio.emit('B2F_value_joy_1_sw', {'teller':teller16}) # niet nodig?
    # joystick_id(pin)
    return teller16

def callback_sw2(pin):
    global teller19
    teller19 += 1
    print("Knop joystick 1 is {} keer ingedrukt\n".format(teller19))
    return teller19

##################### FUNCTIONS - JOYSTICK #####################
# def readChannel(channel):
#     val = spi.xfer2([1,(8|channel)<<4,0])
#     data = (((val[1] & 3) << 8) | val[2])
#     return data

def joysw_id(sw_id):
    global teller16, prev_teller16
    # 1 teller voor 2 sw's
    waarde = 0 # als de callback gecalled is, dan 1, anders 0
    if sw_id == 16:
        commentaar = "joystick 1 is niet ingedrukt"
        if teller16 != prev_teller16:
            commentaar = 'joystick 1 ingedrukt'
            waarde = 1
            prev_teller16 = teller16
        socketio.emit('B2F_value_joy_1_sw', {'teller':teller16})

    elif sw_id == 19:
        commentaar = 'joystick 2 ingedrukt'
        waarde = 1
        socketio.emit('B2F_value_joy_2_sw', {'teller':teller19})
    return waarde, commentaar

def joystick_id(deviceID):
    if deviceID == 14:
        commentaar = "joystick 1 registreerde beweging op x-as"
        waarde = Joy_klasse.readChannel(x_as1)
        socketio.emit('B2F_value_joy_1_x', {'joy_1_x':waarde})
        print(f"dit is x van joystick 1: {waarde}")

    elif deviceID == 15:
        commentaar = 'joystick 1 registreerde beweging op y-as'
        waarde = Joy_klasse.readChannel(y_as1)
        socketio.emit('B2F_value_joy_1_y', {'joy_1_y':waarde})
        print(f"dit is y van joystick 1: {waarde}")
        print(commentaar)

    elif deviceID == 17:
        commentaar = 'joystick 2 registreerde beweging op x-as'
        waarde = Joy_klasse.readChannel(x_as2)
        socketio.emit('B2F_value_joy_2_x', {'joy_2_x':waarde})
        print(f"dit is x van joystick 2: {waarde}")

    elif deviceID == 18:
        commentaar = 'joystick 2 registreerde beweging op y-as'
        waarde = Joy_klasse.readChannel(y_as2)
        socketio.emit('B2F_value_joy_2_y', {'joy_2_y':waarde})
        print(f"dit is y van joystick 2: {waarde}\n")
    return waarde, commentaar

##################### FUNCTIONS - TOUCHSENSOR #####################
# def touch1():
#     global teller7
#     teller7 += 1
#     print("AHA! Gezien!")
#     print(f"\t je bent {teller7} keer gezien geweest!")
#     return teller7

# def touch2():
#     global teller8
#     teller8 += 1
#     print("AHA! Gezien!")
#     print(f"\t je bent {teller8} keer gezien geweest!")
#     return teller8

##################### SOCKETIO #####################
@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)

@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    emit('B2F_connected', {'message': "hallo nieuwe user!"})

@socketio.on('F2B_joystick')
def joystick(data):
    # data = json.loads(dictdata) # hoeft niet als je postman op JSON zet en niet op TEXT -_-
    # while True:
    joy_id = data["deviceid"]
    if joy_id in [14, 15, 17, 18]:
        # waarde, commentaar = joystick_id(joy_id)
        waarde, commentaar = joystick_id(joy_id)

    elif joy_id in [16, 19]:
        waarde, commentaar = joysw_id(joy_id)

    DataRepository.create_historiek(joy_id, commentaar, waarde)

@socketio.on('F2B_touch')
def touch(data):
    touch_id = data['deviceid']
    if touch_id == 7:
        print(f"sensor 1: {touch_id}")
        teller7, commentaar, waarde = Touch_klasse.touch1()
        print(teller7)

    elif touch_id == 8:
        print(f"sensor 2: {touch_id}")
        teller8, commentaar, waarde = Touch_klasse.touch2()
        print(teller8)

    else:
        print('IDK')
    DataRepository.create_historiek(touch_id, commentaar, waarde)


##################### ENDPOINTS #####################
endpoint = '/api/v1'

@app.route('/')
def info():
    return jsonify(info = 'Please go to the endpoint ' + endpoint)

# devices
@app.route(endpoint + '/devices/', methods = ['GET'])
def get_devices():
    if request.method == 'GET':
        data = DataRepository.read_devices()
        if data is not None:
            return jsonify(devices = data), 200
        else:
            return jsonify(message = "error"), 404

@app.route(endpoint + '/devices/<deviceID>/', methods = ['GET'])
def get_device(deviceID):
    if request.method == "GET":
        print(deviceID)
        data = DataRepository.read_device_by_id(deviceID)
        if data is not None:
            return jsonify(device = data), 200
        else:
            return jsonify(message = "error"), 404

# spelers
@app.route(endpoint + '/players/', methods = ['GET'])
def get_players():
    if request.method == "GET":
        data = DataRepository.read_alle_spelers()
        if data is not None:
            return jsonify(spelers = data), 200
        else:
            return jsonify(message = "error"), 404

@app.route(endpoint + '/players/<playerID>/', methods = ['GET'])
def get_player(playerID):
    if request.method == "GET":
        print(playerID)
        data = DataRepository.read_speler_by_id(playerID)
        if data is not None:
            return jsonify(speler = data), 200
        else:
            return jsonify(message = "error"), 404

# historiek/waarden
@app.route(endpoint + '/waarden/', methods = ['GET'])
def get_waarden_joy():
    if request.method == "GET":
        data = DataRepository.read_alle_waarden()
        if data is not None:
            return jsonify(historiek = data), 200
        else:
            print("error")
            return jsonify(message = "error"), 404
    elif request.method == 'POST':
        gegevens = DataRepository.json_or_formdata(request)
        print(gegevens)
        data = DataRepository.create_historiek(gegevens["deviceid"], gegevens["commentaar"], gegevens["waarde"], gegevens["actieid"])
        return jsonify(volgnummer = data), 201

    
##################### THREADS #####################
# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket. 


# def start_thread_teller():
#     print("***** Starting THREAD teller *****")
#     thread2 = threading.Thread(target = teller_doorsturen, args = (), daemon = True)
#     thread2.start()
#     #threading.Timer(10, joystick_uitlezen).start()    

# # # om de joystick uit te lezen ===> ToDo!!!!
# def teller_doorsturen():
#     global teller, socketio, last_val
#     while True:
#         if teller != last_val:
#             print("sending teller")
#             # het aantal keren gedrukt op de joystick
#             socketio.emit('B2F_value_joy_1_sw', {'teller':teller})
#             last_val = teller
#         time.sleep(.5)

def start_thread():
    print("***** Starting THREAD *****")
    thread1 = threading.Thread(target = joystick_uitlezen, args = (), daemon = True)
    thread2 = threading.Thread(target = touch_uitlezen, args = (), daemon = True)
    # thread1.start()
    thread2.start()
    # threading.Timer(1, joystick_uitlezen).start() # niet nodig want anders start je het 2 keer


def joystick_uitlezen():
    while True:
        print("\n***Joysticks uitlezen***")
        for joy_id in [14, 15, 17, 18]:
            waarde, commentaar = joystick_id(joy_id)
            if waarde > 800 or waarde < 200:
                DataRepository.create_historiek(joy_id, commentaar, waarde)
        for joy_id in [16, 19]:
            waarde, commentaar = joysw_id(joy_id)
            if waarde == 1:
                DataRepository.create_historiek(joy_id, commentaar, waarde)
        time.sleep(0.7)

def touch_uitlezen():
    while True:
        print("\n***Touchs uitlezen***")
        if GPIO.input(t1):
            waarde, commentaar = Touch_klasse.touch1()
            print(waarde, commentaar, "😁")
        elif GPIO.input(t2):
            waarde, commentaar = Touch_klasse.touch2()
            print(waarde, commentaar, "😎")
        else:
            print("Geen touch")
        time.sleep(0.7)

##################### SOCKETIO.RUN #####################

if __name__ == "__main__":
    try:
        # debug NIET op True zetten
        setup()
        start_thread()
        # start_chrome_thread()
        # start_thread_teller()
        print("**** Starting APP ****")
        socketio.run(app,debug = False, host = '0.0.0.0')
    except KeyboardInterrupt as e:
        print(e)
    finally:
        print("cleanup pi")
        spi.close()
        GPIO.cleanup()




