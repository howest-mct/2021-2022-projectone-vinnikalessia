# from time import sleep
# import sys
# from RPi import GPIO
# from mfrc522 import SimpleMFRC522
# # reader = SimpleMFRC522()

# def read_rfid():
#     print("hallootjes")
#     while True:
#         reader = SimpleMFRC522()
#         id, text = reader.read()
#         if id is None:
#             print("Niets gevonden")
#             id = None
#         if text is None:
#             print("geen tekst")
#             text = "Nothing"
#         print(f"dit is het id: {id}")
#         sleep(1)
        

# try:
#     while True:
#         print("Hold a tag near the reader")
#         read_rfid()
#         # text = "HAAAALLLLOOOO"
#         # id, text = reader.read()
#         # id, text = reader.read_no_block()
#         # id = reader.read_id()
#         # print("ID: %s\nText: %s" % (id,text))
#         sleep(3)
# except KeyboardInterrupt:
#     GPIO.cleanup()
#     raise


##############################################################################

from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010
from PIL import Image
import time
# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
# substitute bitbang_6800(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface

serial = i2c(port=1, address=0x3C)
# substitute ssd1331(...) or sh1106(...) below if using that device
device = ssd1306(serial)


try:
    print('hello')
    while True:

        with canvas(device, dither = False) as draw:
            print("player 1")
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((30, 40), "__Eliah__", fill="white")
            points = ((123, 32), (118, 37), (108, 37), (108, 27), (118, 27))
            draw.polygon((points), fill="White")
            # draw.polygon(device.bounding_box, outline="white", fill="black")
        time.sleep(3)
        with canvas(device, dither = False) as draw:
            print("player 2")
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((30, 40), "__Aléssia__", fill="white")
            points = ((5, 32), (10, 37), (20, 37), (20, 27), (10, 27))
            draw.polygon((points), fill="White")
        time.sleep(3)
except KeyboardInterrupt as k:
    print(k)
finally:
    print("finally")
    print("Leeg")








