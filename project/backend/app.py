##################### IMPORT #####################
from repositories.DataRepository import DataRepository
from flask_socketio import SocketIO, emit, send
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, jsonify, request
from numpy import False_, broadcast
from subprocess import check_output
from selenium import webdriver
from logging import exception
from flask_cors import CORS
import adafruit_ssd1306
from PIL import Image
from RPi import GPIO
import threading
import digitalio
import neopixel
import random
import spidev
import board
import time

##################### MY IMPORT #####################
from hulpcode.joystick import Joy_klasse
from hulpcode.touch import Touch_klasse
from hulpcode.oled import Oled_klasse
from hulpcode.motor import Motor_klasse
from hulpcode.neopixel import Neos_klasse

motor_klasse_obj = Motor_klasse()
neo_klasse_obj =  Neos_klasse()

########### JOYSTICK ###########
# deze hangen aan de mcp
y_as1 = 0
x_as1 = 1
y_as2 = 2
x_as2 = 3

# de sw van de joystick aan de rpi
sw1 = 5
sw2 = 6

# teller aantal keer sw ingedrukt
teller16 = 0
last_val16 = 0
prev_teller16 = 0

teller19 = 0
last_val19 = 0
prev_teller19 = 0

tellerStapX = 0
tellerStapY = 0
tellerStapZ = 0

########### TOUCHSENSOR ###########
t1 = 13
t2 = 19

# teller aantal keer aangeraakt
teller7 = 0 # t1
teller8 = 0 # t2

########### MOTOR ###########
motor1 = 17
motor2 = 22
hoek1 = 5
hoek2 = 5

# teller
tellerm1 = 0
tellerm2 = 0


########### OLED ###########
tellerOled = 0
oled_reset = digitalio.DigitalInOut(board.D4)
WIDTH = 128
HEIGHT = 64
BORDER = 1
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)
oled.fill(0)
oled.show()
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
draw.rectangle(
    (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
    outline=0,
    fill=0,
)

########### KNOP ###########
up1 = 12
down1 = 16
up2 = 20
down2 = 21

# aan/uit knop pi
onoff = 26

# teller => keuze tot hoeveel er gespeeld wordt
tellerKeuze = 0


# is de teller voordat het spel begint. Hiermee wordt er gekozen tot hoeveel er wordt gespeeld
app_running = True
keuzeSpel = None
game_running = True
choice_running = True

########### RGB ###########
r = 23
g = 24
b = 25

##################### NEOPIXEL #####################
pixel_pin = board.D18 # pin 18
num_pixels = 27 # ik heb 27 neopixels
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

vorige_pix = 0

# lednummer:[x-as, y-as, z-as] 
neopixel_dict = {
        1:[1, 1, 1], 2:[2, 1, 1], 3:[3, 1, 1], 
        4:[3, 2, 1], 5:[2, 2, 1], 6:[1, 2, 1],
        7:[1, 3, 1], 8:[2, 3, 1], 9:[3, 3, 1],

        10:[3, 3, 2], 11:[2, 3, 2], 12:[1, 3, 2], 
        13:[1, 2, 2], 14:[2, 2, 2], 15:[3, 2, 2],
        16:[3, 1, 2], 17:[2, 1, 2], 18:[1, 1, 2],

        19:[1, 1, 3], 20:[2, 1, 3], 21:[3, 1, 3], 
        22:[3, 2, 3], 23:[2, 2, 3], 24:[1, 2, 3],
        25:[1, 3, 3], 26:[2, 3, 3], 27:[3, 3, 3],
        }

# nummer_winnende_combinatie:[lednummer1, lednummer2, lednummer3] => klein naar groot
win_combinaties = {
    1:[0,1,2], 2:[3,4,5], 3:[6,7,8], 4:[0,5,6], 5:[1,4,7], 6:[2,3,8], 
    7:[0,4,8], 8:[2,4,6], 9:[15,16,17], 10:[12,13,14], 11:[9,10,11], 
    12:[11,12,17], 13:[10,13,16], 14:[9,14,15], 15:[9,13,17], 16:[11,13,15],
    17:[18,19,20], 18:[21,22,23], 19:[24,25,26], 20:[18,23,24], 21:[19,22,25], 
    22:[20,21,26], 23:[18,22,26], 24:[20,22,24], 25:[0,17,18], 26:[1,16,19], 
    27:[2,15,20], 28:[0,16,20], 29:[2,16,18], 30:[1,13,25], 31:[5,12,23], 
    32:[6,11,24], 33:[0,12,24], 34:[6,12,18], 35:[7,13,19], 36:[3,14,21], 
    37:[8,9,26], 38:[2,14,26], 39:[8,14,20], 40:[3,13,23], 41:[7,10,25], 
    42:[5,13,21], 43:[6,10,26], 44:[8,10,24], 45:[4,13,22], 46:[0,6,8], 
    47:[6,13,20], 48:[2,13,24], 49:[0,13,26], 50:[8,12,18]}

########### SPELERS ###########
# player1 = True # zo?
# player2 = True # zo?
# posities dat de tegenspeler koos mogen niet meer gekozen worden
led_pos1 = [] # posities dat speler 1 had gekozen
led_pos2 = [] # posities dat speler 2 had gekozen


##################### BUSSEN #####################
# de spi-bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.open(0,1)
spi.max_speed_hz = 10 ** 5

##################### FLASK #####################
# start app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'

socketio = SocketIO(app, cors_allowed_origins="*", 
    logger=False, engineio_logger=False, ping_timeout=1)


CORS(app)
print("program started")


##################### SETUP #####################
def setup():
    global pwm_motor1, pwm_motor2
    print("setup")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # joystick 1
    GPIO.setup(sw1, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(sw1, GPIO.FALLING, callback_sw1, bouncetime = 1000)
    
    # joystick 2
    GPIO.setup(sw2, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(sw2, GPIO.FALLING, callback_sw2, bouncetime = 1000)

    # touchsensoren
    GPIO.setup(t1, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(t2, GPIO.IN, GPIO.PUD_UP)

    # motoren
    GPIO.setup(motor1, GPIO.OUT)
    GPIO.setup(motor2, GPIO.OUT)
    pwm_motor1 = GPIO.PWM(motor1, 1000)
    pwm_motor2 = GPIO.PWM(motor2, 1000)
    pwm_motor1.start(0)
    pwm_motor2.start(0)

    # knoppen
    GPIO.setup(up1, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(up1, GPIO.FALLING, callback_up, bouncetime = 300)

    GPIO.setup(down1, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(down1, GPIO.FALLING, callback_down, bouncetime = 300)

    GPIO.setup(up2, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(up2, GPIO.FALLING, callback_up, bouncetime = 300)

    GPIO.setup(down2, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(down2, GPIO.FALLING, callback_down, bouncetime = 300)

    # RGB led
    GPIO.setup(r, GPIO.OUT)
    GPIO.setup(g, GPIO.OUT)
    GPIO.setup(b, GPIO.OUT)
    
    # rgb led uitzetten, anders geeft het licht in het begin, terwijl die dat niet moet doen
    GPIO.output(r, GPIO.LOW)
    GPIO.output(g, GPIO.HIGH)
    GPIO.output(b, GPIO.LOW)


##################### CALLBACK #####################
def callback_sw1(pin):
    global teller16, teller19
    teller16 += 1
    print("Knop joystick 1 is {} keer ingedrukt\n".format(teller16))
    # socketio.emit('B2F_value_joy_1_sw', {'teller':teller16}) # niet nodig?
    # joystick_id(pin)
    return teller16

def callback_sw2(pin):
    global teller19
    teller19 += 1
    print("Knop joystick 1 is {} keer ingedrukt\n".format(teller19))
    return teller19

def callback_up(pin):
    global tellerKeuze, tellerStapZ
    tellerKeuze += 1
    if tellerStapZ < 3:
        tellerStapZ += 1
    print("1 UP")
    return tellerKeuze, tellerStapZ

def callback_down(pin):
    global tellerKeuze, tellerStapZ
    tellerKeuze -= 1
    if tellerStapZ > 1:
        tellerStapZ -= 1
    print("1 DOWN")
    return tellerKeuze, tellerStapZ

##################### FUNCTIONS - JOYSTICK #####################
def joysw_id(sw_id):
    global teller16, prev_teller16, teller19, prev_teller19
    waarde = 0 # als de callback gecalled is, dan 1, anders 0
    if sw_id == 16:
        commentaar = "joystick 1 is niet ingedrukt"
        if teller16 != prev_teller16:
            commentaar = 'joystick 1 ingedrukt'
            waarde = 1
            prev_teller16 = teller16
        socketio.emit('B2F_value_joy_1_sw', {'teller':teller16})

    elif sw_id == 19:
        commentaar = 'joystick 2 niet ingedrukt'
        if teller19 != prev_teller19:
            commentaar = "joystick 2 ingedrukt"
            waarde = 1
            prev_teller19 = teller19
        socketio.emit('B2F_value_joy_2_sw', {'teller':teller19})
    return waarde, commentaar

def joystick_id(deviceID):
    if deviceID == 14:
        commentaar = "joystick 1 registreerde beweging op x-as"
        waarde = Joy_klasse.readChannel(x_as1)
        socketio.emit('B2F_value_joy_1_x', {'joy_1_x':waarde})
        print(f"dit is x van joystick 1: {waarde}")

    elif deviceID == 15:
        commentaar = 'joystick 1 registreerde beweging op y-as'
        waarde = Joy_klasse.readChannel(y_as1)
        socketio.emit('B2F_value_joy_1_y', {'joy_1_y':waarde})
        print(f"dit is y van joystick 1: {waarde}")
        print(commentaar)

    elif deviceID == 17:
        commentaar = 'joystick 2 registreerde beweging op x-as'
        waarde = Joy_klasse.readChannel(x_as2)
        socketio.emit('B2F_value_joy_2_x', {'joy_2_x':waarde})
        print(f"dit is x van joystick 2: {waarde}")

    elif deviceID == 18:
        commentaar = 'joystick 2 registreerde beweging op y-as'
        waarde = Joy_klasse.readChannel(y_as2)
        socketio.emit('B2F_value_joy_2_y', {'joy_2_y':waarde})
        print(f"dit is y van joystick 2: {waarde}\n")
    return waarde, commentaar

##################### FUNCTIONS - TOUCHSENSOR #####################
def touch1():
    global teller7, hoek1, pwm_motor1
    teller7 += 1
    print("AHA! aangeraakt!")
    print(f"\t je hebt {teller7} keer t1 aangeraakt!")
    hoek1 += 9
    pwm = motor_klasse_obj.hoek_tot_duty(hoek1)
    pwm_motor1.changeDutyCycle(pwm)
    print("een punt bij?")
    return teller7

def touch2():
    global teller8, hoek2
    teller8 += 1
    print("AHA! aangeraakt!")
    print(f"\t je hebt {teller8} keer t2 aangeraakt!")
    hoek2 += 9
    pwm = motor_klasse_obj.hoek_tot_duty(hoek2)
    pwm_motor2.changeDutyCycle(pwm)
    print("een punt bij?")
    return teller8

##################### FUNCTIONS - MOTOR #####################
# def hoek_tot_duty(getal):
#     print(f"Dit is de hoek: {getal}")
#     pwm = int(getal * 0.555555)
#     print(f"Dit is de hoek in pwm: {pwm}")
#     return pwm

##################### ANDERE FUNCTIONS #####################
# ##### kijken of combinatie klopt #####
# def get_key(val):
#     for key, value in neopixel_dict.items():
#          if val == value:
#              print("key exists")
#              return key
#     return "key doesn't exist"
def oled_clear():
    draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
    draw.rectangle(
        (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
        outline=0,
        fill=0,
    )
    draw.rectangle( [(0,0), (oled.width, oled.height)], fill=0)
    oled.image(image)


##### joystick uitlezen tijdens spel #####
def joystick_uitlezen(speler, max_punten):
    global choice_running, tellerStapX, tellerStapY, tellerStapZ, led_pos1, led_pos2, vorige_pos
    neo_klasse_obj.start_kleur()
    positie_lijst = []
    tellerStapX = 1
    tellerStapY = 1
    tellerStapZ = 1
    vorige_pos = 0
    puntenR = 0
    puntenB = 0
    winnaar = None
    while choice_running and True:
        ########################################################
        oled_clear()
        draw.text((5, 17), str(tellerStapX), font=font, fill=255) 
        draw.text((5, 32), str(tellerStapY), font=font, fill=255)
        draw.text((5, 47), str(tellerStapZ), font=font, fill=255)
        oled.show()
        # ROOD
        if speler == 0:
            GPIO.output(b, GPIO.LOW)
            GPIO.output(r, GPIO.HIGH)
            for joy_id in [14, 15, 16]:
                # de x-as
                for joy_id in [14]:
                    waarde, commentaar = joystick_id(joy_id)
                    if waarde > 800 or waarde < 200:
                        print(waarde)
                        DataRepository.create_historiek(joy_id, commentaar, waarde)
                        if waarde > 800 and tellerStapX < 3:
                            print(f"TELLER X {tellerStapX}")
                            tellerStapX += 1
                        elif waarde < 200 and tellerStapX > 1:
                            print(f"TELLER X {tellerStapX}")
                            tellerStapX -= 1
                # de y-as
                for joy_id in [15]:
                    waarde, commentaar = joystick_id(joy_id)
                    if waarde > 800 or waarde < 200:
                        print(waarde)
                        DataRepository.create_historiek(joy_id, commentaar, waarde)
                        if waarde > 800 and tellerStapY < 3:
                            print(f"TELLER X {tellerStapY}")
                            tellerStapY += 1
                        elif waarde < 200 and tellerStapY > 1:
                            print(f"TELLER X {tellerStapY}")
                            tellerStapY -= 1
                
                gekozen_positie = int(positie(tellerStapX, tellerStapY, tellerStapZ, 0, vorige_pos))
                
                if vorige_pos != gekozen_positie and (vorige_pos not in led_pos2 and vorige_pos not in led_pos1):
                    # dan moet vorige led uit en volgende aan
                    print(vorige_pos)
                    print(gekozen_positie)
                    print("😮")
                    pixels.show()

                    neo_klasse_obj.clear_pixel(vorige_pos)
                    vorige_pos = gekozen_positie
                    print(vorige_pos)
                else:
                    print("😡")
                # # de sw
                # for joy_id in [16]:
                #     waarde, commentaar = joysw_id(joy_id)
                #     if waarde == 1:
                #         DataRepository.create_historiek(joy_id, commentaar, waarde)
                # if up1 and tellerStapZ < 3:
                #     # DataRepository.create_historiek(joy_id, commentaar, waarde) # ?
                #     print(f"TELLER Z: {tellerStapZ}")
                #     tellerStapZ += 1
                # elif down1 and tellerStapZ > 1:
                #     print(f"TELLER Z: {tellerStapZ}")
                #     # DataRepository.create_historiek(joy_id, commentaar, waarde) # ?
                #     tellerStapZ -= 1
                
                # de coordinaten noteren op oled
                draw.text((5, 17), str(tellerStapX), font=font, fill=255) 
                draw.text((5, 32), str(tellerStapY), font=font, fill=255)
                draw.text((5, 47), str(tellerStapZ), font=font, fill=255)
                oled.image(image)
                oled.show()

                # bij het bevestigen
                if gekozen_positie in led_pos2 or gekozen_positie in led_pos1:
                    neo_klasse_obj.bezet(speler, gekozen_positie)
                
                if GPIO.input(t1):
                    print("🐑")
                    if gekozen_positie not in led_pos2 and gekozen_positie not in led_pos1:
                        positie_lijst.append(tellerStapX)
                        positie_lijst.append(tellerStapY)
                        positie_lijst.append(tellerStapZ)
                        led_pos1.append(gekozen_positie)
                        neo_klasse_obj.chosen_one(gekozen_positie, speler)
                        print(f"gekozen_positie: {gekozen_positie}")
                        print("opgeslaan!")
                        print(f"dit is de gekozen positie{positie_lijst}")
                        # choice_running = False
                        # positie(positie_lijst, 0)
                        time.sleep(0.2) # anders dubbel positie in lijst
                        # nu is het aan de ander
                        draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
                        draw.rectangle(
                            (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
                            outline=0,
                            fill=0,
                        )
                        draw.rectangle( [(0,0), (oled.width, oled.height)], fill=0)
                        oled.image(image)
                        oled.show()
                        print(led_pos1)
                        positie_lijst = []
                        speler = 1
                    else:
                        print("OZODNCOSAPOPOD   ALQSK?C%    Z")
                        neo_klasse_obj.bezet(speler, gekozen_positie)
                        draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
                        draw.rectangle(
                            (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
                            outline=0,
                            fill=0,
                        )
                        draw.rectangle( [(0,0), (oled.width, oled.height)], fill=0)
                        oled.image(image)
                        oled.show()
                        draw.text((5, 2), "Deze led kan je niet kiezen!\nkies een andere led", font=font, fill=255)# gekozen
                        oled.show()
                        time.sleep(0.2)
                vorige_pos = gekozen_positie
        ########################################################
        # als het speler 1 is, dan moet je alleen joy 1 uitlezen
        elif speler == 1:
            GPIO.output(r, GPIO.LOW)
            GPIO.output(b, GPIO.HIGH)
            for joy_id in [17, 18, 19]:
                # de x-as
                for joy_id in [17]:
                    waarde, commentaar = joystick_id(joy_id)
                    if waarde > 800 or waarde < 200:
                        DataRepository.create_historiek(joy_id, commentaar, waarde)
                        if waarde > 800 and tellerStapX < 3:
                            tellerStapX += 1
                            print(f"TELLER X {tellerStapX}")
                        elif waarde < 200 and tellerStapX > 1:
                            print(f"TELLER X {tellerStapX}")
                            tellerStapX -= 1
                # de y-as
                for joy_id in [18]:
                    waarde, commentaar = joystick_id(joy_id)
                    if waarde > 800 or waarde < 200:
                        DataRepository.create_historiek(joy_id, commentaar, waarde)
                        if waarde > 800 and tellerStapY < 3:
                            print(f"TELLER X {tellerStapY}")
                            tellerStapY += 1
                        elif waarde < 200 and tellerStapY > 1:
                            print(f"TELLER X {tellerStapY}")
                            tellerStapY -= 1
                
                gekozen_positie = int(positie(tellerStapX, tellerStapY, tellerStapZ, 1, vorige_pos))

                if vorige_pos != gekozen_positie and (vorige_pos not in led_pos2 and vorige_pos not in led_pos1):
                    # dan moet vorige led uit en volgende aan
                    print("🤢")
                    print(vorige_pos)
                    print(gekozen_positie)
                    pixels.show()
                    
                    neo_klasse_obj.clear_pixel(vorige_pos)
                    vorige_pos = gekozen_positie
                    print(vorige_pos)
                else:
                    print("😆")
                # de sw
                # for joy_id in [19]:
                #     waarde, commentaar = joysw_id(joy_id)
                #     if waarde == 1:
                #         DataRepository.create_historiek(joy_id, commentaar, waarde)
                # if up1 and tellerStapZ < 3:
                #     print(f"TELLER Z: {tellerStapZ}")
                #     tellerStapZ += 1
                # elif down1 and tellerStapZ > 1:
                #     print(f"TELLER Z: {tellerStapZ}")
                #     tellerStapZ -= 1
                
                draw.text((5, 17), str(tellerStapX), font=font, fill=255) 
                draw.text((5, 32), str(tellerStapY), font=font, fill=255)
                draw.text((5, 47), str(tellerStapZ), font=font, fill=255)
                oled.image(image)
                oled.show()

                # bij het bevestigen
                if gekozen_positie in led_pos2 or gekozen_positie in led_pos1:
                    neo_klasse_obj.bezet(speler, gekozen_positie)

                if GPIO.input(t2):
                    print("🐑")
                    if gekozen_positie not in led_pos1 and gekozen_positie not in led_pos2:
                        positie_lijst.append(tellerStapX)
                        positie_lijst.append(tellerStapY)
                        positie_lijst.append(tellerStapZ)
                        led_pos2.append(gekozen_positie)
                        neo_klasse_obj.chosen_one(gekozen_positie, speler)
                        print("opgeslaan!")
                        print(positie_lijst)
                        # choice_running = False
                        time.sleep(0.2) # anders dubbel positie in lijst
                        # lijst leeg maken voor de volgende keer
                        # nu is het aan de ander
                        draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
                        draw.rectangle(
                            (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
                            outline=0,
                            fill=0,
                        )
                        draw.rectangle( [(0,0), (oled.width, oled.height)], fill=0)
                        oled.image(image)
                        oled.show()
                        print(led_pos2)
                        positie_lijst = []
                        speler = 0
                    else:
                        print("OZODNCOSAPOPOD   ALQSK?C%    Z")
                        draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
                        draw.rectangle(
                            (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
                            outline=0,
                            fill=0,
                        )
                        draw.rectangle( [(0,0), (oled.width, oled.height)], fill=0)
                        oled.image(image)
                        oled.show()
                        time.sleep(0.2)
                        draw.text((5, 2), "Deze led kan je niet kiezen!\nkies een andere led", font=font, fill=255)# gekozen
                        oled.show()
                vorige_pos = gekozen_positie
        neo_klasse_obj.led_onthouden(0, led_pos1)
        neo_klasse_obj.led_onthouden(1, led_pos2)
        time.sleep(0.2)
        print(led_pos1)
        print(led_pos2)
        # for key, value in win_combinaties.items():
        #     if len(set(led_pos1) & set(value)) == 3:
        #         print(key)
        #         print("yess")
        #     elif len(set(led_pos2) & set(value)) == 3:
        #         print(key)
        #         print("yess")
        for key, value in win_combinaties.items():
            print("🐾")
            if len(set(led_pos1) & set(value)) == 3:
                print(key)
                print("punt voor rood")
                puntenR = motor_klasse_obj.puntentelling(0, puntenR)
                print(puntenR)
            elif len(set(led_pos2) & set(value)) == 3:
                print(key)
                print("punt voor blauw")
                puntenB = motor_klasse_obj.puntentelling(1, puntenB)
                print(puntenB)
                print(max_punten, puntenR, puntenB)
        print("🦑")
        if puntenR >= max_punten:
            print(f"rood heeft gewonnen met {puntenR}")
            choice_running = False
            winnaar = "rood"
        elif puntenB >= max_punten:
            print(f"blauw heeft gewonnen met {puntenB}")
            choice_running = False
            winnaar = "blauw"
    if not choice_running:
        print("done😺😺😺😺😺😺")
        print("DOOOONNNNNEEEE")
        neo_klasse_obj.eind_kleur("rood")


def positie(x, y, z, player, vorige_pos):
    neonummer = neo_klasse_obj.get_key(x, y, z)
    print(neonummer)
    pixels[vorige_pos] = (0,0,0)

    print(f"dit zijn de coordinaten {neonummer}")
    print(led_pos1, led_pos2)

    if neonummer not in led_pos1 and neonummer not in led_pos2:
        neo_klasse_obj.player_color(player, neonummer)
        print("deze led mag je gebruiken")
        if player == 0:
            print(led_pos1)
        else:
            print("98687576")
            print(led_pos2)
    else:
        print("kies een andere led")
    print(f"DIT IS VORIGE PIXEL: {vorige_pos}")
    print(f"DIT IS NEONUMMER: {neonummer}")
    time.sleep(0.3)
    return neonummer


def keuzelijst():
    global tellerKeuze, app_running
    print("Kies tot hoeveel er gespeeld wordt")
    while app_running and True:
        if tellerKeuze > 3:
                tellerKeuze = 3
        elif tellerKeuze < 0:
            tellerKeuze = 0
        Oled_klasse.lijst(tellerKeuze)

        if GPIO.input(t1) or GPIO.input(t2):
            # dus als er input is van t1/t2
            print('touchsensor aangeraakt => confirm de keuze')
            print(f"dit is de tellerKeuze: {tellerKeuze}")
            app_running = False
        else:
            time.sleep(0.2)
    if not app_running:
        print("done :P")
        return tellerKeuze

def spel_starten():
    global tellerKeuze, keuzeSpel
    print(tellerKeuze)
    keuzeSpel = keuzelijst() # => in oled ook 
    print("keuzelijst overlopen en gekozen")
    print(tellerKeuze)
    print(f"dit is wat er gekozen werd: ")
    time.sleep(0.2)
    print("LET'S START THE GAME!")
    start_game()

def start_game():
    print(f"DIT IS TELLERKEUZE: {tellerKeuze}")
    print('we starten het spel ☺ ')
    # alles uitzetten van de rgb
    GPIO.output(r, GPIO.LOW)
    GPIO.output(g, GPIO.LOW)
    GPIO.output(b, GPIO.LOW)
    randomPlayer = random.randint(0, 1)
    print(f"DIT IS RANDOM: {randomPlayer}")
    print("EN WIE MAG ER BEGINNEN?......")
    Oled_klasse.display_player(randomPlayer)
    if randomPlayer == 0:
        print("Player 1 begint")
        GPIO.output(r, GPIO.HIGH)
    elif randomPlayer == 1:
        print("Player 2 begint")
        GPIO.output(b, GPIO.HIGH)
    game(randomPlayer, tellerKeuze)

def game(beginner, tellerKeuze):
    # het spel mag alleen joysticks uitlezen van de beginner nu, dan pas van de ander
    # als beginner 0 is, dan alleen x_as1, y_as1, sw1, knop1, knop2
    # als beginner 1 is, dan alleen x_as2, y_as2, sw2, knop3, knop4
    if tellerKeuze == 0:
        # dan wordt er gespeeld tot 1
        max_punten = 1
    elif tellerKeuze == 1:
        # dan wordt er gespeeld tot 3
        max_punten = 3
    elif tellerKeuze == 2:
        # dan wordt er gespeeld tot 5
        max_punten = 5
    elif tellerKeuze == 3:
        # dan wordt er gespeeld tot 9
        max_punten = 9
    while game_running and True:
        time.sleep(2)
        joystick_uitlezen(beginner, max_punten)
    if not game_running:
        print("THE END OF THE GAME")
        # return????

##################### SOCKETIO #####################
@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)

@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    emit('B2F_connected', {'message': "hallo nieuwe user!"})

@socketio.on('F2B_joystick')
def joystick(data):
    # data = json.loads(dictdata) # hoeft niet als je postman op JSON zet en niet op TEXT -_-
    # while True:
    joy_id = data["deviceid"]
    if joy_id in [14, 15, 17, 18]:
        # waarde, commentaar = joystick_id(joy_id)
        waarde, commentaar = joystick_id(joy_id)

    elif joy_id in [16, 19]:
        waarde, commentaar = joysw_id(joy_id)

    DataRepository.create_historiek(joy_id, commentaar, waarde)

@socketio.on('F2B_touch')
def touch(data):
    touch_id = data['deviceid']
    if touch_id == 7:
        print(f"sensor 1: {touch_id}")
        teller7, commentaar, waarde = Touch_klasse.touch1()
        print(teller7)

    elif touch_id == 8:
        print(f"sensor 2: {touch_id}")
        teller8, commentaar, waarde = Touch_klasse.touch2()
        print(teller8)

    else:
        print('IDK')
    DataRepository.create_historiek(touch_id, commentaar, waarde)


##################### ENDPOINTS #####################
endpoint = '/api/v1'

@app.route('/')
def info():
    return jsonify(info = 'Please go to the endpoint ' + endpoint)

# devices
@app.route(endpoint + '/devices/', methods = ['GET'])
def get_devices():
    if request.method == 'GET':
        data = DataRepository.read_devices()
        if data is not None:
            return jsonify(devices = data), 200
        else:
            return jsonify(message = "error"), 404

@app.route(endpoint + '/devices/<deviceID>/', methods = ['GET'])
def get_device(deviceID):
    if request.method == "GET":
        print(deviceID)
        data = DataRepository.read_device_by_id(deviceID)
        if data is not None:
            return jsonify(device = data), 200
        else:
            return jsonify(message = "error"), 404

# spelers
@app.route(endpoint + '/players/', methods = ['GET'])
def get_players():
    if request.method == "GET":
        data = DataRepository.read_alle_spelers()
        if data is not None:
            return jsonify(spelers = data), 200
        else:
            return jsonify(message = "error"), 404

@app.route(endpoint + '/players/<playerID>/', methods = ['GET'])
def get_player(playerID):
    if request.method == "GET":
        print(playerID)
        data = DataRepository.read_speler_by_id(playerID)
        if data is not None:
            return jsonify(speler = data), 200
        else:
            return jsonify(message = "error"), 404

# historiek/waarden
@app.route(endpoint + '/waarden/', methods = ['GET'])
def get_waarden_joy():
    if request.method == "GET":
        data = DataRepository.read_alle_waarden()
        if data is not None:
            return jsonify(historiek = data), 200
        else:
            print("error")
            return jsonify(message = "error"), 404
    elif request.method == 'POST':
        gegevens = DataRepository.json_or_formdata(request)
        print(gegevens)
        data = DataRepository.create_historiek(gegevens["deviceid"], gegevens["commentaar"], gegevens["waarde"], gegevens["actieid"])
        return jsonify(volgnummer = data), 201
    
##################### THREADS #####################
# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket. 


# def start_thread_teller():
#     print("***** Starting THREAD teller *****")
#     thread2 = threading.Thread(target = teller_doorsturen, args = (), daemon = True)
#     thread2.start()
#     #threading.Timer(10, joystick_uitlezen).start()    

# # # om de joystick uit te lezen ===> ToDo!!!!
# def teller_doorsturen():
#     global teller, socketio, last_val
#     while True:
#         if teller != last_val:
#             print("sending teller")
#             # het aantal keren gedrukt op de joystick
#             socketio.emit('B2F_value_joy_1_sw', {'teller':teller})
#             last_val = teller
#         time.sleep(.5)

# ALS JE DE ENE LEEST, KAN JE DE ANDER NIET UITLEZEN!!
def start_thread():
    print("***** Starting THREAD *****")
    thread1 = threading.Thread(target = spel_starten, args = (), daemon = True)
    # thread2 = threading.Thread(target = touch_uitlezen, args = (), daemon = True)
    thread1.start()
    # thread2.start()
    # threading.Timer(1, joystick_uitlezen).start() # niet nodig want anders start je het 2 keer


# def joystick_uitlezen():
#     while True:
#         print("\n***Joysticks uitlezen***")
#         for joy_id in [14, 15, 17, 18]:
#             waarde, commentaar = joystick_id(joy_id)
#             if waarde > 800 or waarde < 200:
#                 DataRepository.create_historiek(joy_id, commentaar, waarde)
#         for joy_id in [16, 19]:
#             waarde, commentaar = joysw_id(joy_id)
#             if waarde == 1:
#                 DataRepository.create_historiek(joy_id, commentaar, waarde)

#         time.sleep(0.7)

# def touch_uitlezen():
#     while True:
#         print("\n***Touchs uitlezen***")
#         if GPIO.input(t1):
#             waarde, commentaar = Touch_klasse.touch1()
#             print(waarde, commentaar, "😁")
#         elif GPIO.input(t2):
#             waarde, commentaar = Touch_klasse.touch2()
#             print(waarde, commentaar, "😎")
#         else:
#             print("Geen touch")
#         time.sleep(0.7)

##################### SOCKETIO.RUN #####################

if __name__ == "__main__":
    try:
        # global app_running
        # debug NIET op True zetten
        draw.text((5, 2), "__ tot 1 spelen __", font=font,     fill=255)# gekozen
        draw.text((5, 17), "   tot 3 spelen", font=font,     fill=255) 
        draw.text((5, 32), "   tot 5 spelen", font=font,     fill=255)
        draw.text((5, 47), "   tot 9 spelen", font=font,     fill=255)
        
        oled.image(image)
        oled.show()
        time.sleep(1)
        setup()
        start_thread()
        # start_chrome_thread()
        # start_thread_teller()
        print("**** Starting APP ****")
        socketio.run(app,debug = False, host = '0.0.0.0')
    except KeyboardInterrupt as e:
        print(e)
    finally:
        oled_clear()
        time.sleep(1)
        print("cleanup pi")
        app_running = False
        pwm_motor1.stop()
        pwm_motor2.stop()
        spi.close()
        neo_klasse_obj.alles_uit()
        time.sleep(0.2)
        GPIO.cleanup()



