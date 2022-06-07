##############################################################################
# import random


# try:
#     while True:
#         speler = random.randint(1,2)
#         if speler == 1:
#             print("player1")
#         elif speler == 2:
#             print("player2")
#         else:
#             print("ONBEKEND")
# except KeyboardInterrupt as kb:
#     print(kb)
# finally:
#     print("einde")
##############################################################################
from luma.core.virtual import viewport, snapshot, range_overlap
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.oled.device import ssd1306
from luma.core.render import canvas
from subprocess import check_output
from logging import exception
from smbus import SMBus
from PIL import Image
from RPi import GPIO
import spidev
import time


########### JOYSTICK ###########
# deze hangen aan de mcp
y_as1 = 0
x_as1 = 1
y_as2 = 2
x_as2 = 3

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

########### TOUCH ###########
t1 = 13
t2 = 19

teller7 = 0
teller8 = 0

########### OLED ###########
test_knop = 20
tellerOled = 0
vorigeOled = 0

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

########### MOTOR ###########
motor1 = 17
motor2 = 27

tellerm1 = 0
tellerm2 = 0

# dit is de beginhoek => 0 punten
hoek = 5

########### BUTTON ###########
knop_up1 = 12
knop_down1 = 16
knop_up2 = 20
knop_down2 = 21


########### FUNCTION ###########
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

    # touchsensoren
    GPIO.setup(motor1, GPIO.OUT)
    # GPIO.setup(motor2, GPIO.OUT)

    # knopjes
    GPIO.setup(knop_up1, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(knop_up1, GPIO.FALLING, callback_knop_up1, bouncetime = 1000)

    GPIO.setup(knop_down1, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(knop_down1, GPIO.FALLING, callback_knop_down1, bouncetime = 1000)

    GPIO.setup(knop_up2, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(knop_up2, GPIO.FALLING, callback_knop_up2, bouncetime = 1000)

    GPIO.setup(knop_down2, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(knop_down2, GPIO.FALLING, callback_knop_down2, bouncetime = 1000)




def callback_sw1(pin):
    global teller16, teller19
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


def joysw_id(sw_id):
    global teller16, prev_teller16, teller19, prev_teller19
    # 1 teller voor 2 sw's
    waarde = 0 # als de callback gecalled is, dan 1, anders 0
    if sw_id == 16:
        commentaar = "joystick 1 is niet ingedrukt"
        if teller16 != prev_teller16:
            commentaar = 'joystick 1 ingedrukt'
            waarde = 1
            prev_teller16 = teller16

    elif sw_id == 19:
        commentaar = 'joystick 2 niet ingedrukt'
        if teller19 != prev_teller19:
            commentaar = "joystick 2 ingedrukt"
            waarde = 1
            prev_teller19 = teller19
    return waarde, commentaar

def joystick_id(deviceID):
    if deviceID == 14:
        commentaar = "joystick 1 registreerde beweging op x-as"
        waarde = readChannel(x_as1)
        print(f"dit is x van joystick 1: {waarde}")

    elif deviceID == 15:
        commentaar = 'joystick 1 registreerde beweging op y-as'
        waarde = readChannel(y_as1)
        print(f"dit is y van joystick 1: {waarde}")
        print(commentaar)

    elif deviceID == 17:
        commentaar = 'joystick 2 registreerde beweging op x-as'
        waarde = readChannel(x_as2)
        print(f"dit is x van joystick 2: {waarde}")

    elif deviceID == 18:
        commentaar = 'joystick 2 registreerde beweging op y-as'
        waarde = readChannel(y_as2)
        print(f"dit is y van joystick 2: {waarde}\n")
    return waarde, commentaar

def hoek_tot_duty(getal):
    print(f"Dit is de hoek: {getal}")
    pwm = int(getal * 0.555555)
    print(f"Dit is de hoek in pwm: {pwm}")
    return pwm

def readChannel(channel):
    val = spi.xfer2([1,(8|channel)<<4,0])
    data = (((val[1] & 3) << 8) | val[2])
    return data

def joystick_uitlezen():
    while True:
        print("\n***Joysticks uitlezen***")
        for joy_id in [14, 15, 17, 18]:
            waarde, commentaar = joystick_id(joy_id)
            if waarde > 800 or waarde < 200:
                print(f"histooorry created: {waarde} '{commentaar}'")
        for joy_id in [16, 19]:
            waarde, commentaar = joysw_id(joy_id)
            if waarde == 1:
                print(f"histooorry created: {waarde} '{commentaar}'")
        time.sleep(0.7)

try:
    setup()
    while True:
        print('hello world!')
        joystick_uitlezen()
except KeyboardInterrupt as k:
    print(k)
finally:
    print("cleanup pi")
    spi.close()
    GPIO.cleanup()