# import RPi.GPIO as GPIO
# import time

# P_SERVO = 17 # adapt to your wiring
# fPWM = 50  # Hz (not higher with software PWM)
# a = 10
# b = 2

# def setup():
#     global pwm
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(P_SERVO, GPIO.OUT)
#     pwm = GPIO.PWM(P_SERVO, fPWM)
#     pwm.start(0)

# def setDirection(direction):
#     duty = a / 180 * direction + b
#     pwm.ChangeDutyCycle(duty)
#     print("direction =", direction, "-> duty =", duty)
#     time.sleep(1) # allow to settle
   
# print("starting")
# setup()
# for direction in range(0, 181, 10):
#     setDirection(direction)
# direction = 0    
# setDirection(0)    
# GPIO.cleanup() 
# print("done")

#####################################################################################
from RPi import GPIO

# duty cycle, calibrate if needed
MIN_DUTY = 5
MAX_DUTY = 10

servo_signal_pin = 17

def deg_to_duty(deg):
    return (deg - 0) * (MAX_DUTY- MIN_DUTY) / 180 + MIN_DUTY

if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(servo_signal_pin, GPIO.OUT)
    # set pwm signal to 50Hz
    servo = GPIO.PWM(servo_signal_pin, 50)
    servo.start(0)

    # loop from 0 to 180
    for deg in range(181):
        duty_cycle = deg_to_duty(deg)    
        servo.ChangeDutyCycle(duty_cycle)

    # cleanup the gpio pins
    GPIO.cleanup()