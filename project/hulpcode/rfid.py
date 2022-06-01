from RPi import GPIO
from rfidClass import SimpleMFRC522
import time

rf = SimpleMFRC522()

try:
    print("hello")
    while True:
        rf.read()
        time.sleep(1)
        rf.read_id()
        time.sleep(1)
except KeyboardInterrupt:
    print("KB")
finally:
    GPIO.cleanup()