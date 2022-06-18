from PIL import Image, ImageDraw, ImageFont
from subprocess import check_output
import adafruit_ssd1306
from RPi import GPIO
import digitalio
import neopixel
import board
import time
import random


class Oled_klasse():
    def __init__(self) -> None:
        self.tellerOled = 0
        self.oled_reset = digitalio.DigitalInOut(board.D4)
        self.WIDTH = 128
        self.HEIGHT = 64
        self.BORDER = 1
        self.i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(self.WIDTH, self.HEIGHT, self.i2c, addr=0x3C, reset=self.oled_reset)
        self.oled.fill(0)
        self.oled.show()
        self.image = Image.new("1", (self.oled.width, self.oled.height))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()
        self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=255, fill=255)
        self.draw.rectangle(
            (self.BORDER, self.BORDER, self.oled.width - self.BORDER - 1, self.oled.height - self.BORDER - 1),
            outline=0,
            fill=0,
        )

    def lijst(self, tellerKeuze):
        self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=255, fill=255)
        self.draw.rectangle(
            (self.BORDER, self.BORDER, self.oled.width - self.BORDER - 1, self.oled.height - self.BORDER - 1),
            outline=0,
            fill=0,
        )
        if tellerKeuze == 0:
            self.draw.text((5, 2), "__ tot 1 spelen __", font=self.font, fill=255)
            self.draw.text((5, 17), "   tot 3 spelen", font=self.font, fill=255) 
            self.draw.text((5, 32), "   tot 5 spelen", font=self.font, fill=255)
            self.draw.text((5, 47), "   tot 9 spelen", font=self.font, fill=255)

        elif tellerKeuze == 1:
            self.draw.text((5, 2), "   tot 1 spelen", font=self.font, fill=255)
            self.draw.text((5, 17), "__ tot 3 spelen __", font=self.font, fill=255) 
            self.draw.text((5, 32), "   tot 5 spelen", font=self.font, fill=255)
            self.draw.text((5, 47), "   tot 9 spelen", font=self.font, fill=255)

        elif tellerKeuze == 2:
            self.draw.text((5, 2), "   tot 1 spelen", font=self.font, fill=255)
            self.draw.text((5, 17), "   tot 3 spelen", font=self.font, fill=255) 
            self.draw.text((5, 32), "__ tot 5 spelen __", font=self.font, fill=255)
            self.draw.text((5, 47), "   tot 9 spelen", font=self.font, fill=255)

        elif tellerKeuze == 3:
            self.draw.text((5, 2), "   tot 1 spelen", font=self.font, fill=255)
            self.draw.text((5, 17), "   tot 3 spelen", font=self.font, fill=255) 
            self.draw.text((5, 32), "   tot 5 spelen", font=self.font, fill=255)
            self.draw.text((5, 47), "__ tot 9 spelen __", font=self.font, fill=255)
        self.oled.image(self.image)
        self.oled.show()

    def display_player(self, randomPlayer):
        self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=255, fill=255)
        self.draw.rectangle(
            (self.BORDER, self.BORDER, self.oled.width - self.BORDER - 1, self.oled.height - self.BORDER - 1),
            outline=0,
            fill=0,
        )
        self.oled.image(self.image)
        self.oled.show()
        if randomPlayer == 0:
            # blauw
            self.draw.text((25, 25), "    ROOD", font=self.font, fill=255)
        elif randomPlayer == 1:
            # rood
            self.draw.text((25, 25), "    BLAUW", font=self.font, fill=255)
        self.oled.image(self.image)
        self.oled.show()

    def ip_adressen(self):
        self.oled_clear()
        ips = check_output(['hostname', '--all-ip-addresses'])
        ip = ips.decode(encoding='UTF-8').strip()
        ip_adresses = ip.split()
        self.draw.text((15, 15), f"{ip_adresses[0]}\n{ip_adresses[1]}", font=self.font, fill=255)
        self.oled.image(self.image)
        self.oled.show()
        time.sleep(4)
        # clear ip adressen?
        self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=255, fill=255)
        self.draw.rectangle(
            (self.BORDER, self.BORDER, self.oled.width - self.BORDER - 1, self.oled.height - self.BORDER - 1),
            outline=0,
            fill=0,
        )
        self.oled.image(self.image)
        self.oled.show()
        self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=255, fill=255)
        self.draw.rectangle(
            (self.BORDER, self.BORDER, self.oled.width - self.BORDER - 1, self.oled.height - self.BORDER - 1),
            outline=0,
            fill=0,
        )
        self.draw.rectangle( [(0,0), (self.oled.width, self.oled.height)], fill=0)
        self.oled.image(self.image)
        self.oled.show()
    
    def oled_clear(self):
        self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=255, fill=255)
        self.draw.rectangle(
            (self.BORDER, self.BORDER, self.oled.width - self.BORDER - 1, self.oled.height - self.BORDER - 1),
            outline=0,
            fill=0,
        )
        self.draw.rectangle( [(0,0), (self.oled.width, self.oled.height)], fill=0)
        self.oled.image(self.image)
        self.oled.show()


    def xyz(self, x, y, z):
        self.draw.text((5, 17), str(x), font=self.font, fill=255) 
        self.draw.text((5, 32), str(y), font=self.font, fill=255)
        self.draw.text((5, 47), str(z), font=self.font, fill=255)
        self.oled.image(self.image)
        self.oled.show()
    
    def bezet(self):
        self.draw.text((5, 2), "Deze led kan je niet kiezen!\nkies een andere led", font=self.font, fill=255)# gekozen
        self.oled.image(self.image)
        self.oled.show()
        time.sleep(1)