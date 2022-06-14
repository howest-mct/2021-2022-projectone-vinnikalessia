# # from RPi import GPIO
# # from SimpleMRFC522 import SimpleMFRC522
# # import multiprocessing
# # import time
# # import sys

# # reader = SimpleMFRC522()
# # # kaartje ID: 703057495658
# # # badge ID: 602271926984
# # # mijn studentenkaart ID: 1007357894346


# # def rfid():
# #     while True:
# #         id_rfid, text = reader.read_no_block()  # uitlezen van de id_rfid en text
# #         if (id_rfid is None):  # als er niets wordt uitgelezen
# #             print("onbekend")
# #         else:
# #             print(id_rfid, text)
# #         time.sleep(2)

# # def multiproces_rfid():
# #     p1 = multiprocessing.Process(target = rfid,)
# #     p1.start()

# # try:
# #     multiproces_rfid()
# # except:
# #     print("d")
# # finally:
# #     GPIO.cleanup()

# # try:
# #         # # print("Hold a tag near the reader")
# #         # # id, text = rf.read()
# #         # # print("ID: %s\nText: %s" % (id,text))
# #         # # print("YAAAAAAAY!!!\n")
# #         # id_rfid, text = rf.read_no_block()  # uitlezen van de id_rfid en text constant
# #         # # if (id_rfid is None):  # als er niets wordt uitgelezen
# #         # #     print("onbekend")
# #         # # else:
# #         # print(id_rfid, text)
# #         # time.sleep(1)
# #     while True:
# #             id_rfid, text = reader.read_no_block()  # uitlezen van de id_rfid en text
# #             print(id_rfid, text)
# #             if (id_rfid is None):  # als er niets wordt uitgelezen
# #                 print("onbekend")
# #             else:
# #                 print('RFID-tag', id_rfid)
# #                 time.sleep(2)

# # except KeyboardInterrupt:
# #     GPIO.cleanup()
# # finally:
# #     print("cleanup")
# #     GPIO.cleanup()

# # def multiprocess_display_ip():
# #     p1 = multiprocessing.Process(target=display_id, args=(rfid_data,))
# #     p1.start()
# #     print(" Starting DISPLAY ")
# #     p1 = threading.Thread(target=check_process_data,
# #                           args=(), daemon=True)
# #     p1.start()
# #########################################################################
# # x (horizontaal), y (verticaal), z (hoogte)
# import time
# import board
# import neopixel
# from RPi import GPIO


# # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# # NeoPixels must be connected to D10, D12, D18 or D21 to work.
# pixel_pin = board.D18

# # The number of NeoPixels
# # num_pixels = 27 # ik heb 27 neopixels
# num_pixels = 3

# # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
# ORDER = neopixel.GRB

# pixels = neopixel.NeoPixel(
#     pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
# )

# neopixel_dict = {
#         0:[1, 1, 1], 1:[2, 1, 1], 2:[3, 1, 1], 
#         3:[3, 2, 1], 4:[2, 2, 1], 5:[1, 2, 1],
#         6:[1, 3, 1], 7:[2, 3, 1], 8:[3, 3, 1],

#         9:[3, 3, 2], 10:[2, 3, 2], 11:[1, 3, 2], 
#         12:[1, 2, 2], 13:[2, 2, 2], 14:[3, 2, 2],
#         15:[3, 1, 2], 16:[2, 1, 2], 17:[1, 1, 2],

#         18:[1, 1, 3], 19:[2, 1, 3], 20:[3, 1, 3], 
#         21:[3, 2, 3], 22:[2, 2, 3], 23:[1, 2, 3],
#         24:[1, 3, 3], 25:[2, 3, 3], 26:[3, 3, 3],
#         }

# lijst = []



# def get_key(val):
#     for key, value in neopixel_dict.items():
#          if val == value:
#              return key
#     return "key doesn't exist"
 
# # met sorted werken als je gaat vergelijken
# win_combinaties = {
#     1:[0,1,2], 2:[3,4,5], 3:[6,7,8], 4:[0,5,6], 5:[1,4,7], 6:[2,3,8], 
#     7:[0,4,8], 8:[2,4,6], 9:[15,16,17], 10:[12,13,14], 11:[9,10,11], 
#     12:[11,12,17], 13:[10,13,16], 14:[9,14,15], 15:[9,13,17], 16:[11,13,15],
#     17:[18,19,20], 18:[21,22,23], 19:[24,25,26], 20:[18,23,24], 21:[19,22,25], 
#     22:[20,21,26], 23:[18,22,26], 24:[20,22,24], 25:[0,17,18], 26:[1,16,19], 
#     27:[2,15,20], 28:[0,16,20], 29:[2,16,18], 30:[1,13,25], 31:[5,12,23], 
#     32:[6,11,24], 33:[0,12,14], 34:[6,12,18], 35:[7,13,19], 36:[3,14,21], 
#     37:[8,9,26], 38:[2,14,26], 39:[8,14,20], 40:[3,13,23], 41:[7,10,25], 
#     42:[5,13,21], 43:[6,10,26], 44:[8,10,24], 45:[4,13,22], 46:[0,6,8], 
#     47:[6,13,20], 48:[2,13,24], 49:[0,13,26], 50:[8,12,18]}

# # om eerste neopixel aan te steken met rood
# # pixels[0] = (255, 0, 0)

# try:
#     while True:
#         # # msg = [1, 1, 1]
#         # msg = int(input("getal: "))
#         # lijst.append(msg)
#         # msg = int(input("getal: "))
#         # lijst.append(msg)
#         # msg = int(input("getal: "))
#         # lijst.append(msg)
#         # print(lijst)
#         # if lijst == neopixel_dict[0]:
#         #     print("yes")
#         # else:
#         #     print("nope")
#         # print(get_key(lijst))
#         # # combinatie wordt dus gevonden in de dict en men weet op welke plaats het staat  (key)
#         # pixels[get_key(lijst)]
#         # # zou het onthouden of niet?

#         ##########################################################################################
#         pixels[0] = (255, 0, 0)
#         pixels[0] = (0, 0, 0)
#         print("licht!")
#         time.sleep(1)
#         ##########################################################################################
#         # time.sleep(2)
#         # lijst = []
#         # keuzex = int(input(f"Geef een eerste nummer in van 1 tot 3: "))
#         # lijst.append(keuzex)
#         # print(type(keuzex))
#         # keuzey = int(input(f"Geef een tweede nummer in van 1 tot 3: "))
#         # lijst.append(keuzey)
#         # keuzez = int(input(f"Geef een derde nummer in van 1 tot 3: "))
#         # lijst.append(keuzez)
#         # print(lijst)
#         # # pixels[lijst] = (255, 0, 0)
#         # if lijst in neopixel_dict:
#         #     print("yes")
#         # else:
#         #     print("nope")
# except KeyboardInterrupt as k:
#     print(k)
# finally:
#     GPIO.cleanup()
#     print("done")


# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 9

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


win_combinaties = {
    1:[0,1,2], 2:[3,4,5], 3:[6,7,8], 4:[0,5,6], 5:[1,4,7], 6:[2,3,8], 
    7:[0,4,8], 8:[2,4,6], 9:[15,16,17], 10:[12,13,14], 11:[9,10,11], 
    12:[11,12,17], 13:[10,13,16], 14:[9,14,15], 15:[9,13,17], 16:[11,13,15],
    17:[18,19,20], 18:[21,22,23], 19:[24,25,26], 20:[18,23,24], 21:[19,22,25], 
    22:[20,21,26], 23:[18,22,26], 24:[20,22,24], 25:[0,17,18], 26:[1,16,19], 
    27:[2,15,20], 28:[0,16,20], 29:[2,16,18], 30:[1,13,25], 31:[5,12,23], 
    32:[6,11,24], 33:[0,12,14], 34:[6,12,18], 35:[7,13,19], 36:[3,14,21], 
    37:[8,9,26], 38:[2,14,26], 39:[8,14,20], 40:[3,13,23], 41:[7,10,25], 
    42:[5,13,21], 43:[6,10,26], 44:[8,10,24], 45:[4,13,22], 46:[0,6,8], 
    47:[6,13,20], 48:[2,13,24], 49:[0,13,26], 50:[8,12,18]}


lijst = [12, 18, 8, 1, 13, 4, 7, 0]

while True:
    for key, value in win_combinaties.items():
        # if set(lijst).intersection(value):
        if len(set(lijst) & set(value)) == 2:
            print(key)
            print("yess")
            print(len(set(lijst) & set(value)))
        else:
            print("nope")
    
    print("einde")
    time.sleep(0.5)
    
    
    
    
    # for i in win_combinaties.values():
    #     if set(lijst).intersection(i):
    #         print("yess")
    #         print(set(lijst).intersection(i))
    #         print(win_combinaties.keys())
    #     else:
    #         print("nope")


    # for i in win_combinaties.values():
    #     set(lijst) & set(i)
    #     print(set(lijst) & set(i))
    #     print("yeeeesss")


        # for val in i:
        # else:
        #     print("neeee")
    # if lijst in win_combinaties.values():
    #     print("YYYEEESSS!")
    # else:
    #     print("nope")
    
    
    # Comment this line out if you have RGBW/GRBW NeoPixels
    # pixels.fill((255, 0, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((255, 0, 0, 0))
    # pixels[0] = (255, 0, 0)
    # pixels.show()
    # print("licht 1!")
    # time.sleep(1)
    # pixels[0] = (0, 0, 0)
    # pixels.show()
    # time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 255, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 255, 0, 0))
    # pixels[1] = (0, 0, 255)
    # pixels.show()
    # print("licht 2!")
    # time.sleep(1)
    # pixels[1] = (0, 0, 0)
    # pixels.show()
    # time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 0, 255))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 0, 255, 0))
    # pixels[2] = (0, 255, 0)
    # pixels.show()
    # print("licht 3!")
    # time.sleep(1)
    # pixels[2] = (0, 0, 0)
    # pixels.show()
    # time.sleep(1)

    # pixels[0] = (255, 0, 0)
    # pixels[1] = (0, 255, 0)
    # pixels[2] = (0, 0, 255)
    # pixels.show()
    # print("licht!")
    # time.sleep(1)
    # pixels[2] = (0, 0, 0)
    # pixels.show()
    # time.sleep(1)

    rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step