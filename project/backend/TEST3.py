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

try:
    while True:
        ips = check_output(['hostname', '--all-ip-addresses'])
        ip = ips.decode(encoding='UTF-8').strip()
        ip_adresses = ip.split()
        draw.text((15, 15), f"{ip_adresses[0]}\n{ip_adresses[1]}", font=font, fill=255)
        oled.image(image)
        oled.show()
        time.sleep(1)
except KeyboardInterrupt as k:
    print(k)
finally:
    print("bye")