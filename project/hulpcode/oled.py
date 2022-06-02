from subprocess import check_output
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010
from luma.core.virtual import viewport, snapshot, range_overlap
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from PIL import Image
from RPi import GPIO
import time

test_knop = 20
teller = 0
vorige = 0

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

def setup():
    print("setup")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(test_knop, GPIO.IN, GPIO.PUD_UP)

    # GPIO.add_event_detect(sw, GPIO.FALLING, callback_knop, bouncetime = 100)

def callback_knop(pin):
    global teller
    teller += 1
    print("De TEST knop is {} keer ingedrukt\n".format(teller))


def status_1():
    ips = check_output(['hostname', '--all-ip-addresses'])
    write_ip_address(ips)

def write_ip_address(msg):
    print(msg)


try:
    print("😁")
    while True:
        if vorige != teller:
            print("GEDRUKT")
            status_1()
        else:
            print("...")

        print("hello")
        # with canvas(device, dither=True) as draw:
        #     draw.rectangle((10, 10, 30, 30), outline="white", fill="red")
        time.sleep(1)
except KeyboardInterrupt as k:
    print(k)
finally:
    
    print("einde")

# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
# substitute bitbang_6800(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface

# substitute ssd1331(...) or sh1106(...) below if using that device