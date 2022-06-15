from PIL import Image, ImageDraw, ImageFont
from subprocess import check_output
import adafruit_ssd1306
from RPi import GPIO
import digitalio
import neopixel
import board
import time
import random

tellerOled = 0
oled_reset = digitalio.DigitalInOut(board.D4)
WIDTH = 128
HEIGHT = 64
BORDER = 1
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)
oled.fill(0)
oled.show()
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
draw.rectangle(
    (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
    outline=0,
    fill=0,
)

class Oled_klasse():
    def lijst(self, tellerKeuze):
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
            draw.text((5, 17), "__ tot 3 spelen __", font=font, fill=255) 
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
        oled.image(image)
        oled.show()

    def display_player(self, randomPlayer):
        draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
        draw.rectangle(
            (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
            outline=0,
            fill=0,
        )
        oled.image(image)
        oled.show()
        if randomPlayer == 0:
            # blauw
            draw.text((25, 25), "    ROOD", font=font, fill=255)
        elif randomPlayer == 1:
            # rood
            draw.text((25, 25), "    BLAUW", font=font, fill=255)
        oled.image(image)
        oled.show()

    def ip_adressen(self):
        print("in status 1")
        ips = str(check_output(['hostname', '--all-ip-addresses']))
        ip = ips.decode(encoding='utf-8').strip()
        ip_adresses = ip.split()
        draw.text((25, 25), f"{ip_adresses[0]}\n{ip_adresses[1]}", font=font, fill=255)
        oled.image(image)
        oled.show()
        time.sleep(2)
        # clear ip adressen?
        draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
        draw.rectangle(
            (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
            outline=0,
            fill=0,
        )
        oled.image(image)
        oled.show()


        draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
        draw.rectangle(
            (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
            outline=0,
            fill=0,
        )
        draw.rectangle( [(0,0), (oled.width, oled.height)], fill=0)
        oled.image(image)
        oled.show()
        print("Clear?")
    
    def oled_clear(self):
        draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
        draw.rectangle(
            (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
            outline=0,
            fill=0,
        )
        draw.rectangle( [(0,0), (oled.width, oled.height)], fill=0)
        oled.image(image)
        oled.show()


    def xyz(self, x, y, z):
        draw.text((5, 17), str(x), font=font, fill=255) 
        draw.text((5, 32), str(y), font=font, fill=255)
        draw.text((5, 47), str(z), font=font, fill=255)
        oled.show()
    
    def bezet(self):
        draw.text((5, 2), "Deze led kan je niet kiezen!\nkies een andere led", font=font, fill=255)# gekozen
        oled.show()