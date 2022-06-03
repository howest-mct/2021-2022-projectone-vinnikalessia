from RPi import GPIO
from SimpleMRFC522 import SimpleMFRC522
import multiprocessing
import time
import sys

reader = SimpleMFRC522()
# kaartje ID: 703057495658
# badge ID: 602271926984
# mijn studentenkaart ID: 1007357894346


def rfid():
    while True:
        id_rfid, text = reader.read_no_block()  # uitlezen van de id_rfid en text
        if (id_rfid is None):  # als er niets wordt uitgelezen
            print("onbekend")
        else:
            print(id_rfid, text)
        time.sleep(2)

def multiproces_rfid():
    p1 = multiprocessing.Process(target = rfid,)
    p1.start()

# try:
#     multiproces_rfid()
# except:
#     print("d")
# finally:
#     GPIO.cleanup()

try:
    while True:
        print("Hold a tag near the reader")
        id, text = reader.read()
        print("ID: %s\nText: %s" % (id,text))
        print("YAAAAAAAY!!!\n")
        time.sleep(5)
        # id_rfid, text = reader.read_no_block()  # uitlezen van de id_rfid en text constant
        if (id is None):  # als er niets wordt uitgelezen
            print("onbekend")
        else:
            print(id, text)
        time.sleep(1)
        # id_rfid, text = reader.read_no_block()  # uitlezen van de id_rfid en text
        # id_rfid, text = reader.read()
        # id_rfid = reader.read_id_no_block()
        # text = "hallo"
        # print(id_rfid, text)
        # if (id_rfid is None):  # als er niets wordt uitgelezen
        #     print("onbekend")
        # else:
        #     print('RFID-tag', id_rfid)
        #     time.sleep(2)
except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    print("cleanup")
    GPIO.cleanup()

# def multiprocess_display_ip():
#     p1 = multiprocessing.Process(target=display_id, args=(rfid_data,))
#     p1.start()
#     print(" Starting DISPLAY ")
#     p1 = threading.Thread(target=check_process_data,
#                           args=(), daemon=True)
#     p1.start()