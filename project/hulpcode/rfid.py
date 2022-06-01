from RPi import GPIO
from rfidClass import SimpleMFRC522
import time
import sys

rf = SimpleMFRC522()
# kaartje ID: 703057495658
# badge ID: 602271926984
# mijn studentenkaart ID: 1007357894346

try:
    while True:
        # print("Hold a tag near the reader")
        # id, text = rf.read()
        # print("ID: %s\nText: %s" % (id,text))
        # print("YAAAAAAAY!!!\n")
        id_rfid, text = rf.read_no_block()  # uitlezen van de id_rfid en text
        # if (id_rfid is None):  # als er niets wordt uitgelezen
        #     print("onbekend")
        # else:
        print(id_rfid, text)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    print("cleanup")
    GPIO.cleanup()


