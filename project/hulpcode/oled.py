from smbus import SMBus
from RPi import GPIO
import time

i2c = SMBus()
i2c.open(1)

def setup():
    print("setup")
    GPIO.setmode(GPIO.BCM)

def versturen(msg):
    print("bericht:")
    i2c.write_byte(0x3C, 0xFF)

try:
    while True:
        msg = 15
        versturen(msg) # string => int?
        time.sleep(1)
except KeyboardInterrupt:
    print("KB")
finally:
    print("cleanup pi")
    GPIO.cleanup()



