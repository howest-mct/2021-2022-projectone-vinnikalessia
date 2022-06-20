# from logging import exception
from smbus import SMBus
from RPi import GPIO
import time

class Motor_klasse():
    def __init__(self) -> None:
        self.motor1 = 19
        self.motor2 = 13

        self.control = [2,3,4,5,6,7,8,9,10,11]
        self.teller1 = 0
        self.teller2 = 0

        self.hoek1 = 5
        self.hoek2 = 5

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor1, GPIO.OUT)
        GPIO.setup(self.motor2, GPIO.OUT)

        self.pwm_motor1 = GPIO.PWM(self.motor1, 50)
        self.pwm_motor2 = GPIO.PWM(self.motor2, 50)
        self.pwm_motor1.start(2.5)
        self.pwm_motor2.start(2.5)

    def puntentelling(self, speler, punten):
        if speler == 0:
            punten += 1
            self.pwm_motor1.ChangeDutyCycle(self.control[self.teller1])
        elif speler == 1:
            self.pwm_motor2.ChangeDutyCycle(self.control[self.teller2])
            punten += 1
        time.sleep(0.2)
        return punten
    
    def punt_bij(self, speler):
        if speler == 0:
            self.hoek1 += 9
            pwm = self.hoek_tot_duty(self.hoek1)
            self.pwm_motor1.ChangeDutyCycle(pwm)
        elif speler == 1:
            self.hoek2 += 9
            pwm = self.hoek_tot_duty(self.hoek2)
            self.pwm_motor2.ChangeDutyCycle(pwm)
    
    def motor_stop(self):
        self.teller1 = 0
        self.teller2 = 0
        print("turning back to 0")
        self.pwm_motor1.ChangeDutyCycle(2)
        self.pwm_motor2.ChangeDutyCycle(2)
        time.sleep(1)
        self.pwm_motor1.ChangeDutyCycle(0)
        self.pwm_motor2.ChangeDutyCycle(0)


    def hoek_tot_duty(self, getal):
        # pwm = int((0.6 + ((getal/90)*0.9)*1000))
        print(f"Dit is de hoek: {getal}")
        pwm = int(getal * 0.555555555555)
        print(f"Dit is de hoek in pwm: {pwm}")
        return pwm
    
    def motor_stop(self):
        self.pwm_motor1.stop()
        self.pwm_motor2.stop()
