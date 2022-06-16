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


class Joy_klasse():    
    def readChannel(self, channel):
        val = spi.xfer2([1,(8|channel)<<4,0])
        data = (((val[1] & 3) << 8) | val[2])
        return data

