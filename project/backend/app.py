##################### IMPORT #####################
from curses import REPORT_MOUSE_POSITION
import json
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

##################### GLOBALE VARIABELEN #####################
global sw_val, x_val, y_val

########### JOYSTICK ###########
# deze hangen aan de mcp
y_as = 0
x_as = 1
# de sw van de joystick aan de rpi
sw = 5
# teller aantal keer sw ingedrukt
teller = 0
x_pos = 0
y_pos = 0
##################### BUSSEN #####################
# de spi-bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10 ** 5

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
    print(teller)
    teller += 1
    print("Button pressed {0}\n".format(teller))

def readChannel(channel):
    val = spi.xfer2([1,(8+channel)<<4,0])
    data = ((val[1] << 8) + val[2])
    return data

##################### FLASK #####################
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins = "*", logger = False,
                    engineio_logger = False, ping_timeout=1)

CORS(app)

@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)

endpoint = '/api/v1'

@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

@app.route(endpoint + '/devices/', methods = ['GET'])
def devices():
    if request.method == 'GET':
        data = DataRepository.read_devices()
        if data is not None:
            return jsonify(devices = data), 200
        else:
            return jsonify(message = "error"), 404

@app.route(endpoint + '/devices/<deviceID>/', methods = ['GET'])
def device(deviceID):
    if request.method == "GET":
        print(deviceID)
        data = DataRepository.read_device_by_id(deviceID)
        if data is not None:
            return jsonify(device = data), 200
        else:
            return jsonify(message = "error"), 404

@app.route(endpoint + '/players/', methods = ['GET'])
def players():
    if request.method == "GET":
        data = DataRepository.read_alle_spelers()
        if data is not None:
            return jsonify(spelers = data), 200
        else:
            return jsonify(message = "error"), 404

@app.route(endpoint + '/players/<playerID>/', methods = ['GET'])
def player(playerID):
    if request.method == "GET":
        print(playerID)
        data = DataRepository.read_speler_by_id(playerID)
        if data is not None:
            return jsonify(speler = data), 200
        else:
            return jsonify(message = "error"), 404

@app.route(endpoint + '/waarden/', methods = ['GET', 'POST'])
def waarden():
    if request.method == "GET":
        data = DataRepository.read_alle_waarden()
        if data is not None:
            return jsonify(waarden = data), 200
        else:
            return jsonify(message = "error"), 404
    elif request.method == "POST":
        gegevens = DataRepository.json_or_formdata(request)
        nieuw_id = DataRepository.create_historiek(
            gegevens['actiedatum'], gegevens['actieid'], gegevens['commentaar'], gegevens['deviceid'], gegevens['waarde']
        )
        return jsonify(volgnummer = nieuw_id)

############################################################################################

@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    devicenaam = DataRepository.read_devices()
    emit('B2F_devices', {'device': devicenaam}, broadcast=True)

# waarden van de 1ste joystick
@socketio.on('F2B_getJoystick_1')
def get_values_joy_1():
    global x_pos
    while True:
        # de x-waarde
        x_val = readChannel(x_as)
        print(f"dit is de x: {x_val}")
        if(x_val >= 950):
            x_pos += 1
        elif(x_val <= 150):
            x_pos -= 1
        print(x_pos)

        # de y-waarde
        y_val = readChannel(y_as)
        print(f"dit is de x: {y_val}")
        if(y_val >= 950):
            y_pos += 1
        elif(y_val <= 150):
            y_pos -= 1
        print(y_pos)


# def joystick_uitlezen():
#     try:
#         # setup()
#         while True:
#             global x_pos
#             # global sw_val, x_val, y_val
#             sw_val = readChannel(sw)
#             print(f"dit is de sw: {sw_val}")
#             x_val = readChannel(x_as)
#             print(f"dit is de x: {x_val}")
#             y_val = readChannel(y_as)
#             print(f"dit is de y: {y_val}\n")

#             if(x_val >= 950 and x_pos < 2):
#                 x_pos += 1

#             elif(x_val <= 150 and x_pos > -2):
#                 x_pos -= 1
#             print(f"Dit is de positie: {x_pos}")

#             time.sleep(0.5)
#     except KeyboardInterrupt:
#         print("keyboardinterrupt")
#     finally:
#         print("cleanup pi")
#         spi.close()
#         GPIO.cleanup()

# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket.

# def all_out():
#     while True:
#         print("***all out***")
#         time.sleep(0.5)

# def start_thread():
#     print("***** Starting THREAD *****")
#     thread = threading.Thread(target = all_out, args = (), daemon = True)
#     thread.start()


if __name__ == '__main__':
    try:
        setup()
        # start_thread()
        # start_chrome_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug = False, host = '0.0.0.0')
        # joystick_uitlezen()
    except KeyboardInterrupt:
        print ('KeyboardInterrupt exception is caught')
    finally:
        GPIO.cleanup()
