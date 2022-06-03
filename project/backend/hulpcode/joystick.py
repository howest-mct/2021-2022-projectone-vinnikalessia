from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify, request
from flask_cors import CORS
from RPi import GPIO
import spidev
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", 
    logger=False, engineio_logger=False, ping_timeout=1)
CORS(app)
########### JOYSTICK ###########
# deze hangen aan de mcp
y_as1 = 0
x_as1 = 1
y_as2 = 3
x_as2 = 4

# de sw van de joystick aan de rpi
sw1 = 5
sw2 = 6

teller16 = 0
last_val16 = 0
prev_teller16 = 0

teller19 = 0
last_val19 = 0
prev_teller19 = 0

# teller aantal keer sw ingedrukt
teller = 0
# de spi-bus
spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz = 10 ** 5

# def setup():
#     print("setup")
#     GPIO.setwarnings(False)
#     GPIO.setmode(GPIO.BCM)

#     # de joystick
#     GPIO.setup(sw, GPIO.IN, GPIO.PUD_UP)
#     GPIO.add_event_detect(sw, GPIO.FALLING, callback_knop, bouncetime = 100)

class Joy_klasse:
    # def callback_knop(pin):
    # global teller
    # teller += 1
    # print("Knop joystick 1 is {} keer ingedrukt\n".format(teller))
    # # socketio.emit('B2F_value_joy_1_sw', {'teller':teller})
    
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

    def readChannel(channel):
        # wat ik had
        # val = spi.xfer2([1,(8+channel)<<4,0])
        # data = ((val[1] << 8) + val[2])

        # oplossing PJ
        val = spi.xfer2([1,(8|channel)<<4,0])
        data = (((val[1] & 3) << 8) | val[2])
        return data

    def joystick_id(deviceID):
        if deviceID == 14:
            commentaar = "joystick 1 registreerde beweging op x-as"
            # waarde = readChannel(x_as1)
            waarde = Joy_klasse.readChannel(x_as1)
            socketio.emit('B2F_value_joy_1_x', {'joy_1_x':waarde})
            print(f"dit is x van joystick 1: {waarde}")
            # print(commentaar)

        elif deviceID == 15:
            commentaar = 'joystick 1 registreerde beweging op y-as'
            waarde = Joy_klasse.readChannel(y_as1)
            socketio.emit('B2F_value_joy_1_y', {'joy_1_y':waarde})
            print(f"dit is y van joystick 1: {waarde}")
            # print(commentaar)

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

# while True:
#     x_val = readChannel(x_as)
#     print(f"dit is de x: {x_val}")
#     time.sleep(1)
#     y_val = readChannel(y_as)
#     print(f"dit is de y: {y_val}\n")
#     time.sleep(2)