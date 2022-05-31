from logging import exception
from smbus import SMBus
from RPi import GPIO
import time



motor = 17
t1 = 21
teller = 0


def setup():
    print("setup")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motor, GPIO.OUT)
    GPIO.setup(t1, GPIO.IN, GPIO.PUD_UP)



def touch():
    global teller
    teller += 1
    print("AHA! Gezien!")
    print(f"\t je bent {teller} keer gezien geweest!")
    return teller

def hoek_tot_duty(getal):
    # pwm = int((0.6 + ((getal/90)*0.9)*1000))
    pwm = int(getal * 0.555555555555)
    print(f"Dit is de hoek in pwm: {pwm}")
    print(type(pwm))
    return pwm


try:
    setup()
    motorpwm = GPIO.PWM(motor, 50)
    motorpwm.start(0)
    print("Hello")
    msg = int(input("geef hoek in tot 180: "))
    hoek = hoek_tot_duty(msg)
    motorpwm.ChangeDutyCycle(hoek)
    time.sleep(0.3)
except KeyboardInterrupt:
    print("KB")
finally:
    print("cleanup")
    GPIO.cleanup()