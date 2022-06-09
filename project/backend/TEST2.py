# from RPi import GPIO
# from SimpleMRFC522 import SimpleMFRC522
# import multiprocessing
# import time
# import sys

# reader = SimpleMFRC522()
# # kaartje ID: 703057495658
# # badge ID: 602271926984
# # mijn studentenkaart ID: 1007357894346


# def rfid():
#     while True:
#         id_rfid, text = reader.read_no_block()  # uitlezen van de id_rfid en text
#         if (id_rfid is None):  # als er niets wordt uitgelezen
#             print("onbekend")
#         else:
#             print(id_rfid, text)
#         time.sleep(2)

# def multiproces_rfid():
#     p1 = multiprocessing.Process(target = rfid,)
#     p1.start()

# try:
#     multiproces_rfid()
# except:
#     print("d")
# finally:
#     GPIO.cleanup()

# try:
#         # # print("Hold a tag near the reader")
#         # # id, text = rf.read()
#         # # print("ID: %s\nText: %s" % (id,text))
#         # # print("YAAAAAAAY!!!\n")
#         # id_rfid, text = rf.read_no_block()  # uitlezen van de id_rfid en text constant
#         # # if (id_rfid is None):  # als er niets wordt uitgelezen
#         # #     print("onbekend")
#         # # else:
#         # print(id_rfid, text)
#         # time.sleep(1)
#     while True:
#             id_rfid, text = reader.read_no_block()  # uitlezen van de id_rfid en text
#             print(id_rfid, text)
#             if (id_rfid is None):  # als er niets wordt uitgelezen
#                 print("onbekend")
#             else:
#                 print('RFID-tag', id_rfid)
#                 time.sleep(2)

# except KeyboardInterrupt:
#     GPIO.cleanup()
# finally:
#     print("cleanup")
#     GPIO.cleanup()

# def multiprocess_display_ip():
#     p1 = multiprocessing.Process(target=display_id, args=(rfid_data,))
#     p1.start()
#     print(" Starting DISPLAY ")
#     p1 = threading.Thread(target=check_process_data,
#                           args=(), daemon=True)
#     p1.start()
#########################################################################
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import time
from RPi import GPIO
import threading
import multiprocessing

from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify, request

from flask_cors import CORS


##################### FLASK #####################
# start app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'

socketio = SocketIO(app, cors_allowed_origins="*", 
    logger=False, engineio_logger=False, ping_timeout=1)


CORS(app)
print("program started")


##################### SOCKETIO #####################
@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)

@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # emit('B2F_connected', {'message': "hallo nieuwe user!"})


##################### ENDPOINTS #####################
endpoint = '/api/v3'

@app.route('/')
def info():
    return jsonify(info = 'Please go to the endpoint ' + endpoint)





##################### SETUP #####################
def setup():
    print("setup")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # joystick 1
    GPIO.setup(sw1, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(x_as1, GPIO.IN)
    GPIO.setup(y_as1, GPIO.IN)
    GPIO.add_event_detect(sw1, GPIO.FALLING, callback_sw1, bouncetime = 1000)
    
    # joystick 2
    GPIO.setup(sw2, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(x_as2, GPIO.IN)
    GPIO.setup(y_as2, GPIO.IN)
    GPIO.add_event_detect(sw2, GPIO.FALLING, callback_sw2, bouncetime = 1000)

    # touchsensoren
    GPIO.setup(t1, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(t2, GPIO.IN, GPIO.PUD_UP)

    # # motoren
    # global pwm_motor1, pwm_motor2
    # GPIO.setup(motor1, GPIO.OUT)
    # GPIO.setup(motor2, GPIO.OUT)
    # pwm_motor1 = GPIO.PWM(motor1, 1000)
    # pwm_motor2 = GPIO.PWM(motor2, 1000)
    # pwm_motor1.start(0)
    # pwm_motor2.start(0)

    # # knoppen
    # GPIO.setup(up1, GPIO.IN, GPIO.PUD_UP)
    # GPIO.add_event_detect(up1, GPIO.FALLING, callback_up1, bouncetime = 1000)

    # GPIO.setup(down1, GPIO.IN, GPIO.PUD_UP)
    # GPIO.add_event_detect(down1, GPIO.FALLING, callback_down1, bouncetime = 1000)

    # GPIO.setup(up2, GPIO.IN, GPIO.PUD_UP)
    # GPIO.add_event_detect(up2, GPIO.FALLING, callback_up2, bouncetime = 1000)

    # GPIO.setup(down2, GPIO.IN, GPIO.PUD_UP)
    # GPIO.add_event_detect(down2, GPIO.FALLING, callback_down2, bouncetime = 1000)

    # # RGB led
    # GPIO.setup(r, GPIO.OUT)
    # GPIO.setup(g, GPIO.OUT)
    # GPIO.setup(b, GPIO.OUT)
    
    # # rgb led uitzetten, anders geeft het licht in het begin, terwijl die dat niet moet doen
    # GPIO.output(r, GPIO.LOW)
    # GPIO.output(g, GPIO.HIGH) # mag eig wel aan om te laten tonen dat opgestart is
    # GPIO.output(b, GPIO.LOW)
    while True:
        time.sleep(1)

##################### CALLBACK #####################
def callback_sw1(pin):
    global teller16, teller19
    teller16 += 1
    print("Knop joystick 1 is {} keer ingedrukt\n".format(teller16))
    return teller16

def callback_sw2(pin):
    global teller19
    teller19 += 1
    print("Knop joystick 2 is {} keer ingedrukt\n".format(teller19))
    return teller19

def callback_up1(pin):
    global tellerup1
    tellerup1 += 1
    print("1 UP")
    return tellerup1

def callback_down1(pin):
    global tellerdown1
    tellerdown1 -= 1
    print("1 DOWN")
    return tellerdown1

def callback_up2(pin):
    global tellerup2
    tellerup2 += 1
    print("2 UP")
    return tellerup2

def callback_down2(pin):
    global tellerdown2
    tellerdown2 -= 1
    print("2 DOWN")
    return tellerdown2

##################### FUNCTIONS - JOYSTICK #####################
def joysw_id(sw_id):
    global teller16, prev_teller16, teller19, prev_teller19
    # 1 teller voor 2 sw's
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


oled_reset = digitalio.DigitalInOut(board.D4)

WIDTH = 128
HEIGHT = 64  # Change to 64 if needed
BORDER = 1

i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

tellerKeuze = 0
app_running = True
keuze = None

image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

t1 = 13
t2 = 19

GPIO.setup(t1, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(t2, GPIO.IN, GPIO.PUD_UP)



def keuzelijst():

    global tellerKeuze, app_running, keuze
    while app_running and True:
        print("Kies tot hoeveel er gespeeld wordt")
        if tellerKeuze > 3:
                tellerKeuze = 3
        elif tellerKeuze < 0:
            tellerKeuze = 0
        print(tellerKeuze)
        draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
        draw.rectangle(
            (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
            outline=0,
            fill=0,
        )
        if tellerKeuze == 0:
            print("keuze 1")
            draw.text((5, 2), "__ tot 1 spelen __", font=font, fill=255)# gekozen
            draw.text((5, 17), "   tot 3 spelen", font=font, fill=255) 
            draw.text((5, 32), "   tot 5 spelen", font=font, fill=255)
            draw.text((5, 47), "   tot 9 spelen", font=font, fill=255)
        elif tellerKeuze == 1:
            print("keuze 2")
            draw.text((5, 2), "   tot 1 spelen", font=font, fill=255)# gekozen
            draw.text((5, 17), "__  tot 3 spelen __", font=font, fill=255) 
            draw.text((5, 32), "   tot 5 spelen", font=font, fill=255)
            draw.text((5, 47), "   tot 9 spelen", font=font, fill=255)

        elif tellerKeuze == 2:
            print("keuze 3")
            draw.text((5, 2), "   tot 1 spelen", font=font, fill=255)# gekozen
            draw.text((5, 17), "   tot 3 spelen", font=font, fill=255) 
            draw.text((5, 32), "__ tot 5 spelen __", font=font, fill=255)
            draw.text((5, 47), "   tot 9 spelen", font=font, fill=255)

        elif tellerKeuze == 3:
            print("keuze 4")
            draw.text((5, 2), "   tot 1 spelen", font=font, fill=255)# gekozen
            draw.text((5, 17), "   tot 3 spelen", font=font, fill=255) 
            draw.text((5, 32), "   tot 5 spelen", font=font, fill=255)
            draw.text((5, 47), "__ tot 9 spelen __", font=font, fill=255)
        else:
            print("KAN NIET")
        # als touchsensor aanraking ziet, dan start spel
        oled.image(image)
        oled.show()
        if GPIO.input(t1) or GPIO.input(t2):
            # dus als er input is van t1/t2
            print('touchsensor aangeraakt => confirm de keuze')
            print(f"dit is de tellerKeuze: {tellerKeuze}")
            keuze = tellerKeuze
            app_running = False
        else:
            time.sleep(0.2)
    if not app_running:
        print("done")


def spel_starten():
    global tellerKeuze
    keuzelijst()
    print("keuzelijst overlopen en gekozen")
    # global app_running
    # while app_running and True:
    # print("Kies tot hoeveel er gespeeld wordt")
    # if tellerKeuze > 3:
    #         tellerKeuze = 3
    # elif tellerKeuze < 0:
    #     tellerKeuze = 0
    # print(tellerKeuze)
    # draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
    # draw.rectangle(
    #     (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
    #     outline=0,
    #     fill=0,
    # )
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
    # print("we wachten even")
    # time.sleep(3)

    time.sleep(0.2)
    print(f"dit is wat er gekozen werd: {keuze}")
    time.sleep(0.2)
    print("LET'S START THE GAME!")
    print("START GAME")









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

########### TOUCHSENSOR ###########
t1 = 13
t2 = 19

# teller aantal keer getouched
teller7 = 0 # t1
teller8 = 0 # t2






# ALS JE DE ENE LEEST, KAN JE DE ANDER NIET UITLEZEN!!
def start_thread():
    print("***** Starting THREAD *****")

    
    # # thread2 = threading.Thread(target = setup, args = (), daemon = True)
    # thread2 = multiprocessing.Process(target = setup, args = (), daemon = True)

    # # thread1 = multiprocessing.Process(target = spel_starten, args = (), daemon = True)
    # # thread2 = threading.Thread(target = touch_uitlezen, args = (), daemon = True)
    # thread2.start()
    
    thread1 = threading.Thread(target = spel_starten, args = (), daemon = True)
    # thread1 = multiprocessing.Process(target = spel_starten, args = (), daemon = True)
    # thread2 = threading.Thread(target = touch_uitlezen, args = (), daemon = True)
    thread1.start()

    # thread2.start()
    # threading.Timer(1, joystick_uitlezen).start() # niet nodig want anders start je het 2 keer




try:
    #setup()
    start_thread()
    socketio.run(app,debug = False, host = '0.0.0.0')

    # while app_running and True:
    #     print("Kies tot hoeveel er gespeeld wordt")
    #     if tellerKeuze > 3:
    #             tellerKeuze = 3
    #     elif tellerKeuze < 0:
    #         tellerKeuze = 0
    #     print(tellerKeuze)
    #     draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
    #     draw.rectangle(
    #         (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
    #         outline=0,
    #         fill=0,
    #     )        
    #     if tellerKeuze == 0:
    #         print("keuze 1")
    #         draw.text((5, 2), "__ tot 1 spelen __", font=font, fill=255)# gekozen
    #         draw.text((5, 17), "   tot 3 spelen", font=font, fill=255) 
    #         draw.text((5, 32), "   tot 5 spelen", font=font, fill=255)
    #         draw.text((5, 47), "   tot 9 spelen", font=font, fill=255)
    #     elif tellerKeuze == 1:
    #         print("keuze 2")
    #         draw.text((5, 2), "   tot 1 spelen", font=font, fill=255)# gekozen
    #         draw.text((5, 17), "__  tot 3 spelen __", font=font, fill=255) 
    #         draw.text((5, 32), "   tot 5 spelen", font=font, fill=255)
    #         draw.text((5, 47), "   tot 9 spelen", font=font, fill=255)

    #     elif tellerKeuze == 2:
    #         print("keuze 3")
    #         draw.text((5, 2), "   tot 1 spelen", font=font, fill=255)# gekozen
    #         draw.text((5, 17), "   tot 3 spelen", font=font, fill=255) 
    #         draw.text((5, 32), "__ tot 5 spelen __", font=font, fill=255)
    #         draw.text((5, 47), "   tot 9 spelen", font=font, fill=255)

    #     elif tellerKeuze == 3:
    #         print("keuze 4")
    #         draw.text((5, 2), "   tot 1 spelen", font=font, fill=255)# gekozen
    #         draw.text((5, 17), "   tot 3 spelen", font=font, fill=255) 
    #         draw.text((5, 32), "   tot 5 spelen", font=font, fill=255)
    #         draw.text((5, 47), "__ tot 9 spelen __", font=font, fill=255)
    #     else:
    #         print("KAN NIET")
    #     # als touchsensor aanraking ziet, dan start spel
    #     oled.image(image)
    #     oled.show()
    #     if GPIO.input(t1) or GPIO.input(t2):
    #         # dus als er input is van t1/t2
    #         print('touchsensor aangeraakt => confirm de keuze')
    #         print(f"dit is de tellerKeuze: {tellerKeuze}")
    #     else:
    #         time.sleep(0.2)
    #     if not app_running:
    #         print("done")
        

except KeyboardInterrupt as k:
    print(k)
finally:
    print("cleanup pi")
    GPIO.cleanup()
    oled.fill(0)
    oled.show()

