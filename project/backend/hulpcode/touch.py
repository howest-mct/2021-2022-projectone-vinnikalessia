from smbus import SMBus
from RPi import GPIO
import time

t1 = 13
t2 = 19

teller7 = 0
teller8 = 0

class Touch_klasse:
    def touch1():
        global teller7
        teller7 += 1
        print(f"\t je hebt {teller7} keer de touch geraakt!")
        commentaar = "Aanraking touchsensor 1 gedetecteerd"
        waarde = 1
        return commentaar, waarde

    def touch2():
        global teller8
        teller8 += 1
        print(f"\t je bent {teller8} keer de touch geraakt!")
        commentaar = "Aanraking touchsensor 2 gedetecteerd"
        waarde = 1
        return commentaar, waarde

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
