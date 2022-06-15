from logging import exception
from smbus import SMBus
from RPi import GPIO
import time

# motor1 = 17
# motor2 = 27
motor1 = 33
motor2 = 35

control = [2,3,4,5,6,7,8,9,10,11]

teller1 = 0
teller2 = 0

# dit is de beginhoek => 0 punten
# hoek = 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor1, GPIO.OUT)
GPIO.setup(motor2, GPIO.OUT)
pwm_motor1 = GPIO.PWM(motor1, 50)
pwm_motor2 = GPIO.PWM(motor2, 50)
pwm_motor1.start(2.5)
pwm_motor2.start(2.5)


class Motor_klasse():
    def puntentelling(self, speler, punten):
        global teller1, teller2
        if speler == 0:
            punten += 1
            motor1.ChangeDutyCycle(control[teller1])
        elif speler == 1:
            motor2.ChangeDutyCycle(control[teller2])
            punten += 1
        time.sleep(0.2)
        print(teller1, teller2)
        return punten
    
    def motor_stop(self):
        global teller1, teller2
        teller1 = 0
        teller2 = 0
        print("turning back to 0")
        motor1.ChangeDutyCycle(2)
        motor2.ChangeDutyCycle(2)
        time.sleep(1)
        motor1.ChangeDutyCycle(0)
        motor2.ChangeDutyCycle(0)


    # def hoek_tot_duty(self, getal):
    #     # pwm = int((0.6 + ((getal/90)*0.9)*1000))
    #     print(f"Dit is de hoek: {getal}")
    #     pwm = int(getal * 0.555555555555)
    #     print(f"Dit is de hoek in pwm: {pwm}")
    #     return pwm
    
    # def puntentelling(self, speler, punten):
    #     if speler == 0:
    #         # rood
    #         punten += 1
    #     else:
    #         # blauw
    #         punten += 1
    #     return punten
    
    # def punt_bij(self, speler):
    #     global hoek1, hoek2
    #     if speler == 0:
    #         hoek1 += 9
    #         pwm = self.hoek_tot_duty(hoek1)
    #         pwm_motor1.ChangeDutyCycle(pwm)
    #     elif speler == 1:
    #         hoek2 += 9
    #         pwm = self.hoek_tot_duty(hoek2)
    #         pwm_motor2.ChangeDutyCycle(pwm)
    
    # def motor_stop(self):
    #     pwm_motor1.stop()
    #     pwm_motor2.stop()

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