from logging import exception
from smbus import SMBus
from RPi import GPIO
import time

motor = 17
t1 = 21
teller = 0

# dit is de beginhoek => 0 punten
hoek = 5

class Motor_klasse():
    def hoek_tot_duty(self, getal):
        # pwm = int((0.6 + ((getal/90)*0.9)*1000))
        print(f"Dit is de hoek: {getal}")
        pwm = int(getal * 0.555555555555)
        print(f"Dit is de hoek in pwm: {pwm}")
        return pwm
    
    def puntentelling(self, speler, punten):
        if speler == 0:
            # rood
            punten += 1
        else:
            # blauw
            punten += 1
        return punten

    # try:
    #     motorpwm = GPIO.PWM(motor, 40)
    #     motorpwm.start(0)
    #     print("Begin scores")
    #     while True:
    #         if GPIO.input(t1) and teller <= 10:
    #             print('input HIGH')
    #             pwm = touch()
    #             motorpwm.ChangeDutyCycle(pwm)
    #             if teller == 10:
    #                 print("Woow!")
    #                 teller = 0
    #                 print("teller is 0")
    #         else:
    #             print('input LOW')
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     # print("terug naar 0")
    #     # motorpwm.ChangeDutyCycle(5)
    #     # time.sleep(0.5)
    #     print("KB")
    # finally:
    #     # print("terug naar 0")
    #     # motorpwm.ChangeDutyCycle(5)
    #     # time.sleep(0.5)
    #     pwm = hoek_tot_duty(0)
    #     motor.ChangeDutyCycle(pwm)
    #     time.sleep(0.2)
    #     print("cleanup")
    #     GPIO.cleanup()