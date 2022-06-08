from subprocess import check_output
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010
from luma.core.virtual import viewport, snapshot, range_overlap
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from PIL import Image
from RPi import GPIO
import time

test_knop1 = 20
test_knop2 = 21
teller = 0
vorige = 0

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

def setup():
    print("setup")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(test_knop1, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(test_knop2, GPIO.IN, GPIO.PUD_UP)

    GPIO.add_event_detect(test_knop1, GPIO.FALLING, callback_knopu, bouncetime = 500)
    GPIO.add_event_detect(test_knop2, GPIO.FALLING, callback_knopd, bouncetime = 500)

def callback_knopu(pin):
    global teller
    if teller <= 3 or teller >= 0:
        teller += 1
        print("De TEST knop is {} keer ingedrukt\n".format(teller))
    return teller

def callback_knopd(pin):
    global teller
    if teller <= 3 or teller >= 0:
        teller -= 1
        print("De TEST knop is {} keer ingedrukt\n".format(teller))
    return teller

def status_1():
    ips = check_output(['hostname', '--all-ip-addresses'])
    write_ip_address(ips)

def write_ip_address(msg):
    print(msg)
    with canvas(device, dither = False) as draw:
        draw.text((30, 40), msg, fill="white")
    time.sleep(3)


def status_2():
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

try:
    setup()
    vorige = 0
    while True:
        # eerst controleren of je teller niet de range overschrijdt
        if teller > 3:
            print("groter dan 3!!")
            teller = 3
        elif teller < 0:
            print("kleiner dan 0!!")
            teller = 0
        print(f"dit is de teller: {teller}")
        if teller == 0:
            with canvas(device, dither = False) as draw:
                print("player 2")
                draw.rectangle(device.bounding_box, outline="white", fill="black")
                draw.text((5, 2), "__ tot 1 spelen __", fill="white")
                draw.text((5, 17), "   tot 3 spelen", fill="red") # gekozen
                draw.text((5, 32), "   tot 5 spelen", fill="white")
                draw.text((5, 47), "   tot 9 spelen", fill="white")
            # time.sleep(3)
        elif teller == 1:
            with canvas(device, dither = False) as draw:
                print("player 2")
                draw.rectangle(device.bounding_box, outline="white", fill="black")
                draw.text((5, 2), "   tot 1 spelen", fill="white")
                draw.text((5, 17), "__ tot 3 spelen __", fill="red") # gekozen
                draw.text((5, 32), "   tot 5 spelen", fill="white")
                draw.text((5, 47), "   tot 9 spelen", fill="white")
            # time.sleep(3)
        elif teller == 2:
            with canvas(device, dither = False) as draw:
                print("player 2")
                draw.rectangle(device.bounding_box, outline="white", fill="black")
                draw.text((5, 2), "   tot 1 spelen", fill="white")
                draw.text((5, 17), "   tot 3 spelen", fill="red") # gekozen
                draw.text((5, 32), "__ tot 5 spelen __", fill="white")
                draw.text((5, 47), "   tot 9 spelen", fill="white")
            # time.sleep(3)
        elif teller == 3:
            with canvas(device, dither = False) as draw:
                print("player 2")
                draw.rectangle(device.bounding_box, outline="white", fill="black")
                draw.text((5, 2), "   tot 1 spelen", fill="white")
                draw.text((5, 17), "   tot 3 spelen", fill="red") # gekozen
                draw.text((5, 32), "   tot 5 spelen", fill="white")
                draw.text((5, 47), "__ tot 9 spelen __", fill="white")
        else:
            print("KAN NIET")
        time.sleep(0.5)

        # with canvas(device, dither = False) as draw:
        #     print("player 2")
        #     draw.rectangle(device.bounding_box, outline="white", fill="black")
        #     draw.text((30, 40), "__Aléssia__", fill="white")
        #     points = ((5, 32), (10, 37), (20, 37), (20, 27), (10, 27))
        #     draw.polygon((points), fill="White")
        # time.sleep(3)

        ##########################################################
        # print(vorige, teller)
        # if vorige != teller:
        #     print("GEDRUKT")
        #     status_2()
        #     vorige = teller
        # else:
        #     print("...Playing...")

        # print("hello")
        # with canvas(device, dither=True) as draw:
        #     draw.rectangle((10, 10, 30, 30), outline="white", fill="black")
        # time.sleep(1)
except KeyboardInterrupt as k:
    print(k)
finally:
    
    print("einde")

# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
# substitute bitbang_6800(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface

# substitute ssd1331(...) or sh1106(...) below if using that device