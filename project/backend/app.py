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
    return teller

def readChannel(channel):
    val = spi.xfer2([1,(8+channel)<<4,0])
    data = ((val[1] << 8) + val[2])
    return data

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
    joy_id = data['deviceid']
    # waarde = data['waarde']
    
    if joy_id == 14:
        # eerste joystick => x-as
        commentaar = "joystick 1 registreerde beweging op x-as"
        waarde = readChannel(x_as)
        print(f"dit is x: {waarde}")
        return waarde

    elif joy_id == 15:
        # eerste joystick => y-as
        commentaar = 'joystick 1 registreerde beweging op y-as'
        waarde = readChannel(y_as)
        print(f"dit is y: {waarde}")
        return waarde

    elif joy_id == 16:
        # eerste joystick => sw
        commentaar = 'joystick ingedrukt'
        # postman en hardware veranderen samen de waarde.
        # wanneer je drukt +1, wanneer postman send +1 en de waarde past zich aan beide aan
        waarde = callback_knop(sw)
        print(f"dit is de knop: {waarde}")
        return waarde

    # elif joy_id == 17:
    #     commentaar = 'joystick 2 registreerde beweging op x-as'
    #     waarde = readChannel(x_as2)
    #     return waarde

    # elif joy_id == 18:
    #     commentaar = 'joystick 2 registreerde beweging op y-as'
    #     waarde = readChannel(y_as2)
    #     return waarde

    print(f"joystick {joy_id} met de waarde {waarde}")

    # DataRepository.create_historiek_joy_1(joy_id, waarde, commentaar)
    DataRepository.create_hahah(joy_id, waarde, commentaar)

    data = DataRepository.read_alle_waarden()
    socketio.emit('B2F_value_joy_1', {joy_id: waarde}, broadcast = True)
    print(f"dit is data: {data}")

    # joystick 1 x-as
    if joy_id == 14:
        print("keuze van de joystick speler 1 op x-as")
    
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

@app.route(endpoint + '/waarden/', methods = ['GET'])
def waarden():
    if request.method == "GET":
        data = DataRepository.read_alle_waarden()
        if data is not None:
            return jsonify(historiek = data), 200
        else:
            print("error")
            return jsonify(message = "error"), 404
    
    ############################################################################################

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

    # if __name__ == '__main__':
    #     try:
    #         setup()
    #         # start_thread()
    #         # start_chrome_thread()
    #         print("**** Starting APP ****")
    #         socketio.run(app, debug = False, host = '0.0.0.0')
    #         # joystick_uitlezen()
    #     except KeyboardInterrupt:
    #         print ('KeyboardInterrupt exception is caught')
    #     finally:
    #         GPIO.cleanup()

if __name__ == "__main__":
    try:
        # debug NIET op True zetten
        setup()
        socketio.run(app, debug = False, host = '0.0.0.0')

    except KeyboardInterrupt as e:
        print(e)
    finally:
        print("cleanup pi")
        spi.close()
        GPIO.cleanup()


# # om de joystick uit te lezen
# def joystick_uitlezen():
#     try:
#         # setup()
#         while True:
#             # global sw_val, x_val, y_val
#             sw_val = readChannel(sw)
#             print(f"dit is de sw: {sw_val}")
#             x_val = readChannel(x_as)
#             print(f"dit is de x: {x_val}")
#             y_val = readChannel(y_as)
#             print(f"dit is de y: {y_val}\n")
#             time.sleep(0.5)
#     except KeyboardInterrupt:
#         print("keyboardinterrupt")
#     finally:
#         print("cleanup pi")
#         spi.close()
#         GPIO.cleanup()


