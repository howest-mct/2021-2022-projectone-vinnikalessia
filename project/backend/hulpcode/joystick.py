from RPi import GPIO
import spidev
import time


class Joy_klasse():
    def __init__(self) -> None:
        self.y_as1 = 0
        self.x_as1 = 1
        self.y_as2 = 3
        self.x_as2 = 4

        self.sw1 = 5
        self.sw2 = 6

        self.teller16 = 0
        self.last_val16 = 0
        self.prev_teller16 = 0

        self.teller19 = 0
        self.last_val19 = 0
        self.prev_teller19 = 0

        self.teller = 0
        # de spi-bus
        self.spi = spidev.SpiDev()
        self.spi.open(0,1)
        self.spi.max_speed_hz = 10 ** 5
          
    def readChannel(self, channel):
        val = self.spi.xfer2([1,(8|channel)<<4,0])
        data = (((val[1] & 3) << 8) | val[2])
        return data

