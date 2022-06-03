from RPi import GPIO
import spidev
import time
########### JOYSTICK ###########
# deze hangen aan de mcp
y_as = 0
x_as = 1

y_as2 = 4
x_as2 = 5

# de sw van de joystick aan de rpi
sw = 5

# teller aantal keer sw ingedrukt
teller = 0
# de spi-bus
spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz = 10 ** 5

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
    print("Knop joystick 1 is {} keer ingedrukt\n".format(teller))
    # socketio.emit('B2F_value_joy_1_sw', {'teller':teller})

def readChannel(channel):
    # wat ik had
    # val = spi.xfer2([1,(8+channel)<<4,0])
    # data = ((val[1] << 8) + val[2])

    # oplossing PJ
    val = spi.xfer2([1,(8|channel)<<4,0])
    data = (((val[1] & 3) << 8) | val[2])
    return data

while True:
    x_val = readChannel(x_as)
    print(f"dit is de x: {x_val}")
    time.sleep(1)
    y_val = readChannel(y_as)
    print(f"dit is de y: {y_val}\n")
    time.sleep(2)