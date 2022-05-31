from smbus import SMBus
from RPi import GPIO
import time

t1 = 21
teller = 0


def setup():
    print("setup")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(t1, GPIO.IN, GPIO.PUD_UP)
    # touch sensoren hebben geen mcp nodig????


def touch():
    global teller
    teller += 1
    print("AHA! Gezien!")
    print(f"\t je bent {teller} keer gezien geweest!")
    return teller

try:
    setup()
    while True:
        if GPIO.input(t1):
            print('input HIGH')
            touch()
        else:
            print('input LOW')

        time.sleep(1)
except KeyboardInterrupt:
    print("KB")
finally:
    print("cleanup")
    GPIO.cleanup() 
