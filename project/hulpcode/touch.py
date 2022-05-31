from smbus import SMBus
from RPi import GPIO
import time

t1 = 2
teller = 0


def setup():
    print("setup")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(t1, GPIO.IN, GPIO.PUD_UP)

    # GPIO.add_event_detect(t1, GPIO.FALLING, callback_touch, bouncetime = 100)

def touch():
    global teller
    teller += 1
    print("AHA! Gezien!")
    print(f"\t je bent {teller} keer gezien geweest!")
    return teller

try:
    setup()
    while True:
        print("1...")
        if (GPIO.input(t1) == 0):
            print("UWU")
            touch()
        elif (GPIO.input(t1) == 1):
            print("O-O")
        else:
            print("?")
        time.sleep(1)
except KeyboardInterrupt:
    print("KB")
finally:
    print("cleanup")
    GPIO.cleanup() 
