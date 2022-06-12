# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 27

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


while True:
    # Comment this line out if you have RGBW/GRBW NeoPixels
    # pixels.fill((255, 0, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((255, 0, 0, 0))
    pixels[0] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[0] = (0,0,0)
    pixels.show()
    time.sleep(0.2)
    
    pixels[1] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[1] = (0,0,0)
    pixels.show()
    time.sleep(0.2)
    
    pixels[2] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[2] = (0,0,0)
    pixels.show()
    time.sleep(0.2)
    
    pixels[3] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[3] = (0,0,0)
    pixels.show()
    time.sleep(0.2)
    
    pixels[4] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[4] = (0,0,0)
    pixels.show()
    time.sleep(0.2)
    
    pixels[5] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[5] = (0,0,0)
    pixels.show()
    time.sleep(0.2)
    
    pixels[6] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[6] = (0,0,0)
    pixels.show()
    time.sleep(0.2)
    
    pixels[7] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[7] = (0,0,0)
    pixels.show()
    time.sleep(0.2)
    
    pixels[8] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[8] = (0,0,0)
    pixels.show()
    time.sleep(0.2)
    
    pixels[9] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[9] = (0,0,0)
    pixels.show()
    time.sleep(0.2)
    
    pixels[10] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[10] = (0,0,0)
    pixels.show()
    time.sleep(0.2)

    pixels[11] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[11] = (0,0,0)
    pixels.show()
    time.sleep(0.2)

    pixels[12] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[12] = (0,0,0)
    pixels.show()
    time.sleep(0.2)

    pixels[13] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[13] = (0,0,0)
    pixels.show()
    time.sleep(0.2)

    pixels[14] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[14] = (0,0,0)
    pixels.show()
    time.sleep(0.2)

    pixels[15] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[15] = (0,0,0)
    pixels.show()
    time.sleep(0.2)

    pixels[16] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[16] = (0,0,0)
    pixels.show()
    time.sleep(0.2)

    pixels[17] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[17] = (0,0,0)
    pixels.show()
    time.sleep(0.2)

    pixels[18] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[18] = (0,0,0)
    pixels.show()
    time.sleep(0.2)

    pixels[19] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[19] = (0,0,0)
    pixels.show()
    time.sleep(0.2)

    pixels[20] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[20] = (0,0,0)
    pixels.show()
    time.sleep(0.2)

    pixels[21] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[21] = (0,0,0)
    pixels.show()
    time.sleep(0.2)

    pixels[22] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[22] = (0,0,0)
    pixels.show()
    time.sleep(0.2)

    pixels[23] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[23] = (0,0,0)
    pixels.show()
    time.sleep(0.2)

    pixels[24] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[24] = (0,0,0)
    pixels.show()
    time.sleep(0.2)

    pixels[25] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[25] = (0,0,0)
    pixels.show()
    time.sleep(0.2)

    pixels[26] = (255,0,0)
    pixels.show()
    time.sleep(0.2)
    pixels[26] = (0,0,0)
    pixels.show()
    time.sleep(0.2)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 255, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 255, 0, 0))

    # Comment this line out if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 0, 255))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 0, 255, 0))
    # pixels.show()
    # time.sleep(1)

    rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step
    pixels.show()
    time.sleep(1)