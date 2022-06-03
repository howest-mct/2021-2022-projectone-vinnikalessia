from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010
from PIL import Image
import time

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)


try:
    while True:
        with canvas(device, dither = False) as draw:
            print("player 1")
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((30, 40), "__Eliah__", fill="white")
            points = ((123, 32), (118, 37), (108, 37), (108, 27), (118, 27))
            draw.polygon((points), fill="White")
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


