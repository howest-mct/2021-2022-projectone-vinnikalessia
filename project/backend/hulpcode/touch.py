from smbus import SMBus
from RPi import GPIO
import time

t1 = 13
t2 = 19

teller7 = 0
teller8 = 0

class Touch_klasse:
    # def __init__(self) -> None:
    #     pass

    # def setup(self):
    #     print("setup")
    #     GPIO.setmode(GPIO.BCM)
    #     GPIO.setwarnings(False)
    #     GPIO.setup(t1, GPIO.IN, GPIO.PUD_UP)
    #     GPIO.setup(t2, GPIO.IN, GPIO.PUD_UP)

    def touch1():
        global teller7
        teller7 += 1
        print("AHA! Gezien!")
        print(f"\t je bent {teller7} keer gezien geweest!")
        return teller7

    def touch2():
        global teller8
        teller8 += 1
        print("AHA! Gezien!")
        print(f"\t je bent {teller8} keer gezien geweest!")
        return teller8

# try:
#     setup()
#     while True:
#         if GPIO.input(t1):
#             # GPIO.input(t1)
#             print('input HIGH from 1')
#             touch1()
#         if GPIO.input(t2):
#             print('input HIGH from 2')
#             touch2()
#         else:
#             print('input LOW')
#         time.sleep(1)
# except KeyboardInterrupt:
#     print("KB")
# finally:
#     print("cleanup")
#     GPIO.cleanup() 
