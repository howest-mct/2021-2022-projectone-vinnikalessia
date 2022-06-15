# from logging import exception
# from smbus import SMBus
# from RPi import GPIO
# import time

# GPIO.setmode(GPIO.BOARD)

# # motor1 = 13
# # motor2 = 19

# # GPIO.setup(motor1, GPIO.OUT)
# # GPIO.setup(motor2, GPIO.OUT)

# GPIO.setup(33, GPIO.OUT)
# GPIO.setup(35, GPIO.OUT)
# pwm_motor1 = GPIO.PWM(33, 100)
# pwm_motor2 = GPIO.PWM(35, 100)
# pwm_motor1.start(0)
# pwm_motor2.start(0)
# time.sleep(1)

# hoek1 = 2
# hoek2 = 2

# teller1 = 0
# teller2 = 0

# def hoek_tot_duty(getal):
#     # pwm = int((0.6 + ((getal/90)*0.9)*1000))
#     print(f"Dit is de hoek: {getal}")
#     pwm = int(getal * 0.555555555555)
#     print(f"Dit is de hoek in pwm: {pwm}")
#     return pwm

# def puntentelling(speler, punten):
#     if speler == 0:
#         punten += 1
#     else:
#         punten += 1
#     return punten

# def punt_bij(speler):
#     global hoek1, hoek2
#     if speler == 0:
#         hoek1 += 0.5
#         pwm = hoek_tot_duty(hoek1)
#         print(f"dit is PWM 1: {pwm}")
#         pwm_motor1.ChangeDutyCycle(pwm)
#     elif speler == 1:
#         hoek2 += 0.5
#         pwm = hoek_tot_duty(hoek2)
#         print(f"dit is PWM 2: {pwm}")
#         pwm_motor2.ChangeDutyCycle(pwm)

# def motor_stop():
#     pwm_motor1.stop()
#     pwm_motor2.stop()


# duty1 = 2
# duty2 = 2

# try:
#     print("Begin scores")
#     while True:
#         msg = int(input(f"geef een getal in 0 of 1: "))
#         if duty1 < 12 and msg == 1:
#             print(f"duty 1: {duty1}")
#             print("draaien")
#             pwm_motor1.ChangeDutyCycle(1+duty1)
#             time.sleep(0.5)
#             duty1 += 1

#         elif duty2 < 12 and msg == 0:
#             print(f"duty 2: {duty2}")
#             print("draaien")
#             pwm_motor2.ChangeDutyCycle(1+duty2)
#             time.sleep(0.5)
#             duty2 += 1

#         elif duty1 > 12:
#             duty1 = 2
#         elif duty2 > 12:
#             duty2 = 2
#         # if msg == 0:
#         #     print("0")
#         #     teller1 += 1
#         #     hoek1 += 9
#         #     # pwm = hoek_tot_duty(hoek2)
#         #     print(f"dit is PWM 1: {hoek1}")
#         #     pwm_motor1.ChangeDutyCycle(hoek1)
#         #     if teller1 == 10:
#         #         print("Woow!")
#         #         teller1 = 0
#         #         print("teller1 is 0")
#         # elif msg == 1:
#         #     print("1")
#         #     teller2 += 1
#         #     hoek2 += 9
#         #     # pwm = hoek_tot_duty(hoek2)
#         #     print(f"dit is PWM 1: {hoek2}")
#         #     pwm_motor2.ChangeDutyCycle(hoek2)
#         #     if teller2 == 10:
#         #         print("Woow!")
#         #         teller2 = 0
#         #         print("teller2 is 0")
#         # else:
#         #     print("NOPE")
#         time.sleep(1)
# except KeyboardInterrupt:
#     # print("terug naar 0")
#     # motorpwm.ChangeDutyCycle(5)
#     # time.sleep(0.5)
#     print("KB")
# finally:
#     print("turning back to 0")
#     pwm_motor1.ChangeDutyCycle(2)
#     pwm_motor2.ChangeDutyCycle(2)
#     time.sleep(1)
#     pwm_motor1.ChangeDutyCycle(0)
#     pwm_motor2.ChangeDutyCycle(0)
#     # print("terug naar 0")
#     # motorpwm.ChangeDutyCycle(5)
#     # time.sleep(0.5)
#     # pwm = hoek_tot_duty(0)
#     # pwm_motor1.ChangeDutyCycle(pwm)
#     # pwm_motor2.ChangeDutyCycle(pwm)
#     pwm_motor1.stop()
#     pwm_motor2.stop()
#     time.sleep(0.5)
#     print(duty1)
#     print(duty2)
#     print("cleanup")
#     GPIO.cleanup()


# # ########################################################################

# # from RPi import GPIO
# # import time

# # GPIO.setmode(GPIO.BOARD)
# # # GPIO.setmode(GPIO.BCM)
# # GPIO.setup(33,GPIO.OUT)
# # servo = GPIO.PWM(33,20)

# # servo.start(0)
# # print("waiting for 1 second")
# # time.sleep(1)


# # print("rotation at intervals 12 degrees")
# # # while duty <= 13:
# # duty = 2
# # while True:
# #     if duty < 13:
# #         duty += 0.2
# #         msg = int(input(f"typ 0: "))
# #         print(f"duty: {duty}")
# #         servo.ChangeDutyCycle(duty)
# #         time.sleep(1)
# #     else:
# #         print("hello")
# #         duty = 2

# # print("turning back to 0")
# # servo.ChangeDutyCycle(2)
# # time.sleep(1)
# # servo.ChangeDutyCycle(0)

# # servo.stop()
# # GPIO.cleanup()
# # print("cleanup")


#################################################################################################
# in servo motor,
# 1ms pulse for 0 degree (LEFT)
# 1.5ms pulse for 90 degree (MIDDLE)
# 2ms pulse for 180 degree (RIGHT)

# so for 50hz, one frequency is 20ms
# duty cycle for 0 degree = (1/20)*100 = 5%
# duty cycle for 90 degree = (1.5/20)*100 = 7.5%
# duty cycle for 180 degree = (2/20)*100 = 10%
import RPi.GPIO as GPIO
import time

# control = [5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10]
control = [2,3,4,5,6,7,8,9,10,11]
teller1 = 0
teller2 = 0
# servo1 = 33
# servo2 = 35
servo1 = 13
servo2 = 19
# GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo1,GPIO.OUT)
GPIO.setup(servo2,GPIO.OUT)
p1 = GPIO.PWM(servo1,50)# 50hz frequency
p2 = GPIO.PWM(servo2,50)# 50hz frequency
p1.start(2.5)# starting duty cycle ( it set the servo to 0 degree )
p2.start(2.5)# starting duty cycle ( it set the servo to 0 degree )
try:
    while True:
        msg = int(input(f"geef 0 of 1: "))
        if teller1 < 9 and teller2 < 9:
            if msg == 0:
                teller1 += 1
                # p1.ChangeDutyCycle(control[x])
                p1.ChangeDutyCycle(control[teller1])
                time.sleep(0.2)
                print(teller1)
            elif msg == 1:
                teller2 += 1
                p2.ChangeDutyCycle(control[teller2])
                time.sleep(0.2)
                print(teller2)
        
        elif teller1 >= 8:
            teller1 = 0
            teller2 = 0
            print("turning back to 0")
            p1.ChangeDutyCycle(2)
            p2.ChangeDutyCycle(2)
            time.sleep(1)
            p1.ChangeDutyCycle(0)
            p2.ChangeDutyCycle(0)
        
        elif teller2 >= 8:
            teller1 = 0
            teller2 = 0
            print("turning back to 0")
            p1.ChangeDutyCycle(2)
            p2.ChangeDutyCycle(2)
            time.sleep(1)
            p1.ChangeDutyCycle(0)
            p2.ChangeDutyCycle(0)
        
        else:
            print("nope")
            # for x in range(8,0,-1):
            #     p.ChangeDutyCycle(control[x])
            #     time.sleep(0.2)
            #     print(x)
           
except KeyboardInterrupt:
    GPIO.cleanup()

