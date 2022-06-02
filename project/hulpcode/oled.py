from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from PIL import Image
import time


try:
    while True:
        # rev.1 users set port=0
        # substitute spi(device=0, port=0) below if using that interface
        im = Image.open("pexels-engin-mataraci-1047369.jpg")

        print(im.format, im.size, im.mode)
        time.sleep(5)
        # substitute bitbang_6800(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface
        serial = i2c(port=1, address=0x3C)

        # substitute ssd1331(...) or sh1106(...) below if using that device
        device = ssd1306(serial)

        with canvas(device, dither=True) as draw:
            draw.rectangle((10, 10, 30, 30), outline="white", fill="red")
        time.sleep(1)
except KeyboardInterrupt as k:
    print(k)
finally:
    print("einde")