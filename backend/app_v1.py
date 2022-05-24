from logging import exception
import spidev
import time
from RPi import GPIO

# de joystick
# deze hangen aan de mcp
y_as = 0
x_as = 1


# de knop van de joystick
knop = 5

# teller aantal keer knop ingedrukt
teller = 0

# de spi
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10 ** 5

def setup():
    print("setup")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(knop, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(knop, GPIO.FALLING, callback_knop, bouncetime = 100)

def callback_knop(pin):
    global teller
    print(teller)
    teller += 1
    print("Button pressed {0}\n".format(teller))


def readChannel(channel):
    val = spi.xfer2([1,(8+channel)<<4,0])
    data = ((val[1] << 8) + val[2])
    return data


try:
    setup()
    while True:
        sw_val = readChannel(knop)
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


