from time import sleep
import sys
from RPi import GPIO
from mfrc522 import SimpleMFRC522
# reader = SimpleMFRC522()

def read_rfid():
    print("hallootjes")
    while True:
        reader = SimpleMFRC522()
        id, text = reader.read()
        if id is None:
            print("Niets gevonden")
            id = None
        if text is None:
            print("geen tekst")
            text = "Nothing"
        print(f"dit is het id: {id}")
        sleep(1)
        

try:
    while True:
        print("Hold a tag near the reader")
        read_rfid()
        # text = "HAAAALLLLOOOO"
        # id, text = reader.read()
        # id, text = reader.read_no_block()
        # id = reader.read_id()
        # print("ID: %s\nText: %s" % (id,text))
        sleep(3)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise