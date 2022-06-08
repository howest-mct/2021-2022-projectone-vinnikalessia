# from RPi import GPIO
# from SimpleMRFC522 import SimpleMFRC522
# import multiprocessing
# import time
# import sys

# reader = SimpleMFRC522()
# # kaartje ID: 703057495658
# # badge ID: 602271926984
# # mijn studentenkaart ID: 1007357894346


# def rfid():
#     while True:
#         id_rfid, text = reader.read_no_block()  # uitlezen van de id_rfid en text
#         if (id_rfid is None):  # als er niets wordt uitgelezen
#             print("onbekend")
#         else:
#             print(id_rfid, text)
#         time.sleep(2)

# def multiproces_rfid():
#     p1 = multiprocessing.Process(target = rfid,)
#     p1.start()

# try:
#     multiproces_rfid()
# except:
#     print("d")
# finally:
#     GPIO.cleanup()

# try:
#         # # print("Hold a tag near the reader")
#         # # id, text = rf.read()
#         # # print("ID: %s\nText: %s" % (id,text))
#         # # print("YAAAAAAAY!!!\n")
#         # id_rfid, text = rf.read_no_block()  # uitlezen van de id_rfid en text constant
#         # # if (id_rfid is None):  # als er niets wordt uitgelezen
#         # #     print("onbekend")
#         # # else:
#         # print(id_rfid, text)
#         # time.sleep(1)
#     while True:
#             id_rfid, text = reader.read_no_block()  # uitlezen van de id_rfid en text
#             print(id_rfid, text)
#             if (id_rfid is None):  # als er niets wordt uitgelezen
#                 print("onbekend")
#             else:
#                 print('RFID-tag', id_rfid)
#                 time.sleep(2)

# except KeyboardInterrupt:
#     GPIO.cleanup()
# finally:
#     print("cleanup")
#     GPIO.cleanup()

# def multiprocess_display_ip():
#     p1 = multiprocessing.Process(target=display_id, args=(rfid_data,))
#     p1.start()
#     print(" Starting DISPLAY ")
#     p1 = threading.Thread(target=check_process_data,
#                           args=(), daemon=True)
#     p1.start()
#########################################################################
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import time
from RPi import GPIO

oled_reset = digitalio.DigitalInOut(board.D4)

WIDTH = 128
HEIGHT = 64  # Change to 64 if needed
BORDER = 1

i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

tellerKeuze = 0
app_running = True

image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

t1 = 13
t2 = 19

GPIO.setup(t1, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(t2, GPIO.IN, GPIO.PUD_UP)

try:
    while app_running and True:
        print("Kies tot hoeveel er gespeeld wordt")
        if tellerKeuze > 3:
                tellerKeuze = 3
        elif tellerKeuze < 0:
            tellerKeuze = 0
        print(tellerKeuze)
        draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
        draw.rectangle(
            (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
            outline=0,
            fill=0,
        )        
        if tellerKeuze == 0:
            print("keuze 1")
            draw.text((5, 2), "__ tot 1 spelen __", font=font, fill=255)# gekozen
            draw.text((5, 17), "   tot 3 spelen", font=font, fill=255) 
            draw.text((5, 32), "   tot 5 spelen", font=font, fill=255)
            draw.text((5, 47), "   tot 9 spelen", font=font, fill=255)
        elif tellerKeuze == 1:
            print("keuze 2")
            draw.text((5, 2), "   tot 1 spelen", font=font, fill=255)# gekozen
            draw.text((5, 17), "__  tot 3 spelen __", font=font, fill=255) 
            draw.text((5, 32), "   tot 5 spelen", font=font, fill=255)
            draw.text((5, 47), "   tot 9 spelen", font=font, fill=255)

        elif tellerKeuze == 2:
            print("keuze 3")
            draw.text((5, 2), "   tot 1 spelen", font=font, fill=255)# gekozen
            draw.text((5, 17), "   tot 3 spelen", font=font, fill=255) 
            draw.text((5, 32), "__ tot 5 spelen __", font=font, fill=255)
            draw.text((5, 47), "   tot 9 spelen", font=font, fill=255)

        elif tellerKeuze == 3:
            print("keuze 4")
            draw.text((5, 2), "   tot 1 spelen", font=font, fill=255)# gekozen
            draw.text((5, 17), "   tot 3 spelen", font=font, fill=255) 
            draw.text((5, 32), "   tot 5 spelen", font=font, fill=255)
            draw.text((5, 47), "__ tot 9 spelen __", font=font, fill=255)
        else:
            print("KAN NIET")
        # als touchsensor aanraking ziet, dan start spel
        oled.image(image)
        oled.show()
        if GPIO.input(t1) or GPIO.input(t2):
            # dus als er input is van t1/t2
            print('touchsensor aangeraakt => confirm de keuze')
            print(f"dit is de tellerKeuze: {tellerKeuze}")
        else:
            time.sleep(0.2)
        if not app_running:
            print("done")
        

except KeyboardInterrupt as k:
    print(k)
finally:
    print("cleanup pi")
    GPIO.cleanup()
    oled.fill(0)
    oled.show()

