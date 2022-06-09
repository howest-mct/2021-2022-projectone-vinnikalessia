
# import board
# import digitalio
# from PIL import Image, ImageDraw, ImageFont
# import adafruit_ssd1306
import time
from subprocess import check_output

# # Define the Reset Pin
# oled_reset = digitalio.DigitalInOut(board.D4)

# # Change these
# # to the right size for your display!
# WIDTH = 128
# HEIGHT = 64  # Change to 64 if needed
# BORDER = 1

# # Use for I2C.
# i2c = board.I2C()
# oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# # Use for SPI
# # spi = board.SPI()
# # oled_cs = digitalio.DigitalInOut(board.D5)
# # oled_dc = digitalio.DigitalInOut(board.D6)
# # oled = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, oled_dc, oled_reset, oled_cs)

# # Clear display.
# oled.fill(0)
# oled.show()

# # Create blank image for drawing.
# # Make sure to create image with mode '1' for 1-bit color.
# image = Image.new("1", (oled.width, oled.height))

# # Get drawing object to draw on image.
# draw = ImageDraw.Draw(image)

# # Draw a white background
# draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

# # Draw a smaller inner rectangle
# draw.rectangle(
#     (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
#     outline=0,
#     fill=0,
# )

# # Load default font.
# font = ImageFont.load_default()

# # Draw Some Text
# # text = "Hello World2!"
# # (font_width, font_height) = font.getsize(text)


# # draw.text(
# #     (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
# #     text,
# #     font=font,
# #     fill=255,
# # )


# #  draw.rectangle(device.bounding_box, outline="white", fill="black")
# draw.text((5, 2), "__ tot 1 spelen __", font=font,     fill=255)# gekozen
# draw.text((5, 17), "   tot 3 spelen", font=font,     fill=255) 
# draw.text((5, 32), "   tot 5 spelen", font=font,     fill=255)
# draw.text((5, 47), "   tot 9 spelen", font=font,     fill=255)

# # Display image
# oled.image(image)
# oled.show()

# time.sleep(1.5)

# print("clear scherm")
# oled.fill(0)
# oled.show()
# print("WACHTEN")
# time.sleep(2)
# draw.text((5, 32), "__ HELLO WORLD! :) __", font=font, fill=255)# gekozen


# # Display image
# oled.image(image)
# oled.show()

##############################################################################################################
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This demo will fill the screen with white, draw a black box on top
and then print Hello World! in the center of the display

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!
"""

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Change these
# to the right size for your display!
WIDTH = 128
HEIGHT = 64  # Change to 64 if needed
BORDER = 1

# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Use for SPI
# spi = board.SPI()
# oled_cs = digitalio.DigitalInOut(board.D5)
# oled_dc = digitalio.DigitalInOut(board.D6)
# oled = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, oled_dc, oled_reset, oled_cs)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

# Draw a smaller inner rectangle
draw.rectangle(
    (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
    outline=0,
    fill=0,
)

# Load default font.
font = ImageFont.load_default()

# Draw Some Text
text = "Hello World!"
(font_width, font_height) = font.getsize(text)
draw.text(
    (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
    text,
    font=font,
    fill=255,
)

# Display image

oled.image(image)
oled.show()
time.sleep(1)

draw.rectangle( [(0,0), (oled.width, oled.height)], fill=0)
oled.image(image)
oled.show()
time.sleep(1)

# text = "HALLOOOO"
# (font_width, font_height) = font.getsize(text)
# draw.text(
#     (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
#     text,
#     font=font,
#     fill=255,
# )
# oled.image(image)
# oled.show()
# time.sleep(1)

draw.rectangle( [(0,0), (oled.width, oled.height)], fill=0)
oled.image(image)
oled.show()
time.sleep(1)

######
ips = check_output(['hostname', '--all-ip-addresses'])
ip = ips.decode(encoding='utf-8').strip()
ip_adresses = ip.split()
print(ip_adresses)
print(ip_adresses[1])
print(ip_adresses[0])
######

text = (f"{ip_adresses[1]}")
(font_width, font_height) = font.getsize(text)
draw.text(
    (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
    text,
    font=font,
    fill=255,
)
text = (f"\n{ip_adresses[0]}")
(font_width, font_height) = font.getsize(text)
draw.text(
    (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
    text,
    font=font,
    fill=255,
)
oled.image(image)
oled.show()