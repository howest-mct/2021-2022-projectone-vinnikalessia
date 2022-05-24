from repositories.DataRepository import DataRepository
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify
from selenium import webdriver
from logging import exception
from flask_cors import CORS
import threading
import spidev
import time
from RPi import GPIO

global sw_val, x_val, y_val
# de joystick
# deze hangen aan de mcp
y_as = 0
x_as = 1


# de sw van de joystick
sw = 5

# teller aantal keer sw ingedrukt
teller = 0

# de spi
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10 ** 5

def setup():
    print("setup")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
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

# Code voor Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins = "*", logger = False,
                    engineio_logger = False, ping_timeout=1)

CORS(app)

@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)

@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

############################################################################################

# @socketio.on('connect')
# def initial_connection():
#     print('A new client connect')
#     # # Send to the client!
#     # vraag de status op van de lampen uit de DB
#     devicenaam = DataRepository.read_devices()
#     print(f"dit is de devicenaam: {devicenaam}")
#     emit('B2F_devices', {'device': devicenaam}, broadcast=True)


# @socketio.on('F2B_')

try:
    setup()
    while True:
        # global sw_val, x_val, y_val
        sw_val = readChannel(sw)
        print(f"dit is de sw: {sw_val}")
        x_val = readChannel(x_as)
        print(f"dit is de x: {x_val}")
        y_val = readChannel(y_as)
        print(f"dit is de y: {y_val}\n")
        time.sleep(0.5)
except Exception as e:
    print(e)
finally:
    print("cleanup pi")
    spi.close()
    GPIO.cleanup


