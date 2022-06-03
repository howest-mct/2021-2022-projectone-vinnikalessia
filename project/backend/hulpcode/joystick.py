from RPi import GPIO
import spidev
import time

########### JOYSTICK ###########
# deze hangen aan de mcp
y_as1 = 0
x_as1 = 1
y_as2 = 3
x_as2 = 4

# de sw van de joystick aan de rpi
sw1 = 5
sw2 = 6

teller16 = 0
last_val16 = 0
prev_teller16 = 0

teller19 = 0
last_val19 = 0
prev_teller19 = 0

# teller aantal keer sw ingedrukt
teller = 0
# de spi-bus
spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz = 10 ** 5


class Joy_klasse:    
    def callback_sw1(pin):
        global teller16
        teller16 += 1
        print("Knop joystick 1 is {} keer ingedrukt\n".format(teller16))
        return teller16

    def callback_sw2(pin):
        global teller19
        teller19 += 1
        print("Knop joystick 1 is {} keer ingedrukt\n".format(teller19))
        return teller19

    def readChannel(channel):
        val = spi.xfer2([1,(8|channel)<<4,0])
        data = (((val[1] & 3) << 8) | val[2])
        return data

    def joystick_id(deviceID):
        if deviceID == 14:
            commentaar = "joystick 1 registreerde beweging op x-as"
            waarde = Joy_klasse.readChannel(x_as1)
            print(f"dit is x van joystick 1: {waarde}")

        elif deviceID == 15:
            commentaar = 'joystick 1 registreerde beweging op y-as'
            waarde = Joy_klasse.readChannel(y_as1)
            print(f"dit is y van joystick 1: {waarde}")

        elif deviceID == 17:
            commentaar = 'joystick 2 registreerde beweging op x-as'
            waarde = Joy_klasse.readChannel(x_as2)
            print(f"dit is x van joystick 2: {waarde}")

        elif deviceID == 18:
            commentaar = 'joystick 2 registreerde beweging op y-as'
            waarde = Joy_klasse.readChannel(y_as2)
            print(f"dit is y van joystick 2: {waarde}\n")
        return waarde, commentaar
    
    def joysw_id(sw_id):
        global teller16, prev_teller16, teller19, prev_teller19
        waarde = 0 # als de callback gecalled is, dan 1, anders 0
        if sw_id == 16:
            commentaar = "joystick 1 is niet ingedrukt"
            if teller16 != prev_teller16:
                commentaar = 'joystick 1 ingedrukt'
                waarde = 1
                prev_teller16 = teller16

        elif sw_id == 19:
            commentaar = "joystick 2 is niet ingedrukt"
            if teller19 != prev_teller19:
                commentaar = 'joystick 2 ingedrukt'
                waarde = 1
                prev_teller19 = teller19
        return waarde, commentaar
