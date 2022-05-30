##################### IMPORT #####################
import json
from numpy import False_
from repositories.DataRepository import DataRepository
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify, request
from selenium import webdriver
from logging import exception
from flask_cors import CORS
import threading
import spidev
import time
from RPi import GPIO

##################### GLOBALE VARIABELEN ######################
global sw_val, x_val, y_val

########### JOYSTICK ###########
# deze hangen aan de mcp
y_as = 0
x_as = 1

# de sw van de joystick aan de rpi
sw = 5

# teller aantal keer sw ingedrukt
teller = 0

# test2
##################### BUSSEN #####################
# de spi-bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10 ** 5


##################### FLASK #####################
# start app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
print("program started")


##################### SETUP #####################
def setup():
    print("setup")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # de joystick
    GPIO.setup(sw, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(sw, GPIO.FALLING, callback_knop, bouncetime = 100)

def callback_knop(pin):
    global teller
    teller += 1
    print("Knop joystick 1 is {0} keer ingedrukt\n".format(teller))
    # joystick_id(pin)
    return teller

def readChannel(channel):
    val = spi.xfer2([1,(8+channel)<<4,0])
    data = ((val[1] << 8) + val[2])
    return data

def joysw_id(sw_id):
    if sw_id == 16:
        commentaar = 'joystick 1 ingedrukt'
        waarde = 1

    elif sw_id == 19:
        commentaar = 'joystick 2 ingedrukt'
        waarde = 1
    return waarde, commentaar

def joystick_id(deviceID):
    if deviceID == 14:
        # eerste joystick => x-as
        commentaar = "joystick 1 registreerde beweging op x-as"
        waarde = readChannel(x_as)
        print(f"dit is x: {waarde}")
        print(commentaar)

    elif deviceID == 15:
        # eerste joystick => y-as
        commentaar = 'joystick 1 registreerde beweging op y-as'
        waarde = readChannel(y_as)
        print(f"dit is y: {waarde}")
        print(commentaar)

    # elif joy_id == 17:
    #     commentaar = 'joystick 2 registreerde beweging op x-as'
    #     waarde = readChannel(x_as2)

    # elif joy_id == 18:
    #     commentaar = 'joystick 2 registreerde beweging op y-as'
    #     waarde = readChannel(y_as2)

    # elif deviceID == 19:
    #     commentaar = 'joystick ingedrukt'
    #     waarde = callback_knop(sw2)
    #     print(commentaar)
    #     print(f"dit is de knop: {waarde}")

    return waarde, commentaar

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
        waarde, commentaar = joystick_id(joy_id)

    elif joy_id in [16, 19]:
        waarde, commentaar = joysw_id(joy_id)
    
    print(f"joystick met id {joy_id}, heeft de waarde {waarde}")
    DataRepository.create_historiek_joy(joy_id, commentaar, waarde)

    socketio.emit('B2F_value_joy_1', {"waarden":{"deviceid":joy_id, "waarde":waarde}}, broadcast = True)
    time.sleep(0.5)

    
    # while True:
    #     sw_val = readChannel(sw) # eigenlijk geen readchannel want via pi niet mcp
    #     print(f"dit is de sw: {sw_val}")

    #     x_val = readChannel(x_as)
    #     print(f"dit is de x: {x_val}")

    #     y_val = readChannel(y_as)
    #     print(f"dit is de y: {y_val}\n")

    #     emit("B2F_value_joy_1", {"x_waarde":x_val}, {"y_waarde":y_val}, {"sw_waarde":sw_val}, broadcast = True)
    #     time.sleep(0.5)


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
        data = DataRepository.create_historiek_joy(gegevens["deviceid"], gegevens["commentaar"], gegevens["waarde"], gegevens["actieid"])
        return jsonify(volgnummer = data), 201

    
##################### STARTEN #####################
# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket.


def start_thread():
    print("***** Starting THREAD *****")
    thread1 = threading.Thread(target = joystick_uitlezen, args = (), daemon = True)
    thread1.start()


##################### SOCKETIO.RUN #####################

if __name__ == "__main__":
    try:
        # debug NIET op True zetten
        setup()
        # start_thread()
        # start_chrome_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug = False, host = '0.0.0.0')
        # joystick_uitlezen()

    except KeyboardInterrupt as e:
        print(e)
    finally:
        print("cleanup pi")
        spi.close()
        GPIO.cleanup()


##################### THREADS #####################

# om de joystick uit te lezen
def joystick_uitlezen():
    try:
        # setup()
        while True:
            # global sw_val, x_val, y_val
            sw_val = readChannel(sw)
            print(f"dit is de sw: {sw_val}")
            x_val = readChannel(x_as)
            print(f"dit is de x: {x_val}")
            y_val = readChannel(y_as)
            print(f"dit is de y: {y_val}\n")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("keyboardinterrupt")
    finally:
        print("cleanup pi")
        spi.close()
        GPIO.cleanup()


