#################### IMPORT #####################
from repositories.DataRepository import DataRepository
from flask_socketio import SocketIO, emit, send
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, jsonify, request
# from numpy import False_, broadcast
from subprocess import check_output
# from selenium import webdriver
# from logging import exception
from flask_cors import CORS
import adafruit_ssd1306
from PIL import Image
from RPi import GPIO
import threading
import digitalio
import datetime
import neopixel
import random
import board
import time

#################### MY IMPORT #####################
from hulpcode.joystick import Joy_klasse
# # from hulpcode.touch import Touch_klasse
from hulpcode.oled import Oled_klasse
from hulpcode.motor import Motor_klasse
from hulpcode.neopixel import Neos_klasse

motor_klasse_obj = Motor_klasse()
neo_klasse_obj =  Neos_klasse()
oled_klasse_obj = Oled_klasse()
joy_klasse_obj = Joy_klasse()


########## JOYSTICK ###########
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

speler = None

########### TOUCHSENSOR ###########
t1 = 27
t2 = 17

# teller aantal keer aangeraakt
teller7 = 0
teller8 = 0

########### MOTOR ###########
motor1 = 19
motor2 = 13

# teller
tellerm1 = 0
tellerm2 = 0


# ########### KNOP ###########
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
player = None

########### RGB ###########
r = 23
g = 24
b = 25

#################### NEOPIXEL #####################
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

########## SPELERS ###########
led_pos1 = [] # posities dat speler 1 had gekozen
led_pos2 = [] # posities dat speler 2 had gekozen
puntenR = 0
puntenB = 0

#################### FLASK #####################
# start app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'

socketio = SocketIO(app, cors_allowed_origins="*", 
    logger=False, engineio_logger=False, ping_timeout=1)

CORS(app)
print("program started")

#################### SETUP #####################
def setup():
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

    # knoppen
    GPIO.setup(up1, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(up1, GPIO.FALLING, callback_up1, bouncetime = 300)

    GPIO.setup(down1, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(down1, GPIO.FALLING, callback_down1, bouncetime = 300)

    GPIO.setup(up2, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(up2, GPIO.FALLING, callback_up2, bouncetime = 300)

    GPIO.setup(down2, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(down2, GPIO.FALLING, callback_down2, bouncetime = 300)

    # RGB led
    GPIO.setup(r, GPIO.OUT)
    GPIO.setup(g, GPIO.OUT)
    GPIO.setup(b, GPIO.OUT)
    
    # rgb led uitzetten, anders geeft het licht in het begin, terwijl die dat niet moet doen
    GPIO.output(r, GPIO.LOW)
    GPIO.output(g, GPIO.HIGH)
    GPIO.output(b, GPIO.LOW)


#################### CALLBACK #####################
def callback_sw1(pin):
    global teller16
    teller16 += 1
    socketio.emit('B2F_value_joy_1_sw', {'teller':teller16})
    joysw_id(pin)
    return teller16

def callback_sw2(pin):
    global teller19
    teller19 += 1
    socketio.emit('B2F_value_joy_2_sw', {'teller':teller19})
    joysw_id(pin)
    return teller19

def callback_up1(pin):
    global tellerKeuze, tellerStapZ, player
    tellerKeuze += 1
    if player == 0:
        socketio.emit('B2F_value_knopup1', {'teller':tellerStapZ})
        if tellerStapZ < 3:
            tellerStapZ += 1
            DataRepository.create_historiek(pin, "1 UP", tellerKeuze, 3)
            socketio.emit('B2F_historiek', {'deviceid':pin, 'actieid':3, 'waarde':"1 UP", "actiedatum":datetime.datetime.now()})
    return tellerKeuze, tellerStapZ

def callback_up2(pin):
    global tellerKeuze, tellerStapZ, player
    tellerKeuze += 1
    if player == 1:
        socketio.emit('B2F_value_knopup2', {'teller':tellerStapZ})
        if tellerStapZ < 3:
            tellerStapZ += 1
            DataRepository.create_historiek(pin, "1 UP", tellerKeuze, 3)
            socketio.emit('B2F_historiek', {'deviceid':pin, 'actieid':3, 'waarde':"1 UP", "actiedatum":datetime.datetime.now()})
    return tellerKeuze, tellerStapZ

def callback_down1(pin):
    global tellerKeuze, tellerStapZ, player
    tellerKeuze -= 1
    if player == 1:
        socketio.emit('B2F_value_knopdown1', {'teller':tellerStapZ})
        if tellerStapZ > 1:
            tellerStapZ -= 1
            DataRepository.create_historiek(pin, "1 DOWN", tellerStapZ, 3)
    return tellerKeuze, tellerStapZ

def callback_down2(pin):
    global tellerKeuze, tellerStapZ, player
    tellerKeuze -= 1
    if player == 2:
        socketio.emit('B2F_value_knopdown2', {'teller':tellerStapZ})
        if tellerStapZ > 1:
            tellerStapZ -= 1
            DataRepository.create_historiek(pin, "1 DOWN", tellerStapZ, 3)
    return tellerKeuze, tellerStapZ

# ##################### FUNCTIONS - JOYSTICK #####################
def joystick_id(deviceID):
    waarde = 0
    commentaar = ''
    if deviceID == 14:
        commentaar = "joystick 1 registreerde beweging op x-as"
        waarde = joy_klasse_obj.readChannel(x_as1)
        socketio.emit('B2F_value_joy_1_x', {'joy_1_x':waarde})

    elif deviceID == 15:
        commentaar = 'joystick 1 registreerde beweging op y-as'
        waarde = joy_klasse_obj.readChannel(y_as1)
        socketio.emit('B2F_value_joy_1_y', {'joy_1_y':waarde})

    elif deviceID == 17:
        commentaar = 'joystick 2 registreerde beweging op x-as'
        waarde = joy_klasse_obj.readChannel(x_as2)
        socketio.emit('B2F_value_joy_2_x', {'joy_2_x':waarde})

    elif deviceID == 18:
        commentaar = 'joystick 2 registreerde beweging op y-as'
        waarde = joy_klasse_obj.readChannel(y_as2)
        socketio.emit('B2F_value_joy_2_y', {'joy_2_y':waarde})
    return waarde, commentaar

def joysw_id(sw_id):
    global teller16, prev_teller16, teller19, prev_teller19
    waarde = 0 # als de callback gecalled is, dan 1, anders 0
    if sw_id == 5:
        commentaar = "joystick 1 is niet ingedrukt"
        if teller16 != prev_teller16:
            commentaar = 'joystick 1 ingedrukt'
            waarde = 1
            prev_teller16 = teller16
    elif sw_id == 6:
        commentaar = 'joystick 2 niet ingedrukt'
        if teller19 != prev_teller19:
            commentaar = "joystick 2 ingedrukt"
            waarde = 1
            prev_teller19 = teller19
    return waarde, commentaar

#################### ANDERE FUNCTIONS #####################
#### joystick uitlezen tijdens spel #####
def joystick_uitlezen(speler, max_punten):
    global choice_running, tellerStapX, tellerStapY, tellerStapZ, led_pos1, led_pos2, vorige_pos
    global player
    positie_lijst = []
    tellerStapX = 1
    tellerStapY = 1
    tellerStapZ = 1
    vorige_pos = 0
    puntenR = 0
    puntenB = 0
    winnaar = None
    oud_gekozen_pixelsR = []
    oud_gekozen_pixelsB = []
    while choice_running and True:
        player = speler # voor callbacks
        ########################################################
        oled_klasse_obj.oled_clear()
        oled_klasse_obj.xyz(tellerStapX, tellerStapY, tellerStapZ)
        # ROOD
        if speler == 1:
            socketio.emit('B2F_player', {'speler':'rood'})
            GPIO.output(b, GPIO.LOW)
            GPIO.output(r, GPIO.HIGH)
            for joy_id in [14, 15, 16]:
                # de x-as
                for joy_id in [14]:
                    waarde, commentaar = joystick_id(joy_id)
                    if waarde > 800 or waarde < 200:
                        DataRepository.create_historiek(joy_id, commentaar, waarde, 1)
                        if waarde > 800 and tellerStapX < 3:
                            tellerStapX += 1
                        elif waarde < 200 and tellerStapX > 1:
                            tellerStapX -= 1
                # de y-as
                for joy_id in [15]:
                    waarde, commentaar = joystick_id(joy_id)
                    if waarde > 800 or waarde < 200:
                        DataRepository.create_historiek(joy_id, commentaar, waarde, 1)
                        if waarde > 800 and tellerStapY < 3:
                            tellerStapY += 1
                        elif waarde < 200 and tellerStapY > 1:
                            tellerStapY -= 1
                
                gekozen_positie = int(positie(tellerStapX, tellerStapY, tellerStapZ, 0, vorige_pos))
                if vorige_pos != gekozen_positie and (vorige_pos not in led_pos2 and vorige_pos not in led_pos1):
                    neo_klasse_obj.show_pixels()
                    neo_klasse_obj.clear_pixel(vorige_pos)
                    vorige_pos = gekozen_positie

                # de coordinaten noteren op oled
                oled_klasse_obj.xyz(tellerStapX, tellerStapY, tellerStapZ)

                # bij het bevestigen
                if gekozen_positie in led_pos2 or gekozen_positie in led_pos1:
                    neo_klasse_obj.bezet(gekozen_positie)
                
                if GPIO.input(t1):
                    if gekozen_positie not in led_pos2 and gekozen_positie not in led_pos1:
                        positie_lijst.append(tellerStapX)
                        positie_lijst.append(tellerStapY)
                        positie_lijst.append(tellerStapZ)
                        led_pos1.append(gekozen_positie)
                        neo_klasse_obj.chosen_one(gekozen_positie, speler)
                        time.sleep(0.2) # anders dubbel positie in lijst
                        oled_klasse_obj.oled_clear()
                        positie_lijst = []
                        speler = 2
                    else:
                        neo_klasse_obj.bezet(gekozen_positie)
                        oled_klasse_obj.oled_clear()
                        oled_klasse_obj.bezet()
                vorige_pos = gekozen_positie
        ########################################################
        # als het speler 1 is, dan moet je alleen joy 1 uitlezen
        elif speler == 2:
            socketio.emit('B2F_player', {'speler':'blauw'})
            GPIO.output(r, GPIO.LOW)
            GPIO.output(b, GPIO.HIGH)
            for joy_id in [17, 18, 19]:
                # de x-as
                for joy_id in [17]:
                    waarde, commentaar = joystick_id(joy_id)
                    if waarde > 800 or waarde < 200:
                        DataRepository.create_historiek(joy_id, commentaar, waarde, 1)
                        if waarde > 800 and tellerStapX < 3:
                            tellerStapX += 1
                        elif waarde < 200 and tellerStapX > 1:
                            tellerStapX -= 1
                # de y-as
                for joy_id in [18]:
                    waarde, commentaar = joystick_id(joy_id)
                    if waarde > 800 or waarde < 200:
                        DataRepository.create_historiek(joy_id, commentaar, waarde, 1)
                        if waarde > 800 and tellerStapY < 3:
                            tellerStapY += 1
                        elif waarde < 200 and tellerStapY > 1:
                            tellerStapY -= 1
                
                gekozen_positie = int(positie(tellerStapX, tellerStapY, tellerStapZ, 1, vorige_pos))

                if vorige_pos != gekozen_positie and (vorige_pos not in led_pos2 and vorige_pos not in led_pos1):
                    neo_klasse_obj.show_pixels()
                    neo_klasse_obj.clear_pixel(vorige_pos)
                    vorige_pos = gekozen_positie
                oled_klasse_obj.xyz(tellerStapX, tellerStapY, tellerStapZ)

                # bij het bevestigen
                if gekozen_positie in led_pos2 or gekozen_positie in led_pos1:
                    neo_klasse_obj.bezet(gekozen_positie)

                if GPIO.input(t2):
                    if gekozen_positie not in led_pos1 and gekozen_positie not in led_pos2:
                        positie_lijst.append(tellerStapX)
                        positie_lijst.append(tellerStapY)
                        positie_lijst.append(tellerStapZ)
                        led_pos2.append(gekozen_positie)
                        neo_klasse_obj.chosen_one(gekozen_positie, speler)
                        time.sleep(0.2) # anders dubbel positie in lijst
                        oled_klasse_obj.oled_clear()
                        positie_lijst = []
                        speler = 1
                    else:
                        oled_klasse_obj.oled_clear()
                        oled_klasse_obj.bezet()
                        oled_klasse_obj.oled_clear()
                vorige_pos = gekozen_positie
        neo_klasse_obj.led_onthouden(0, led_pos1)
        neo_klasse_obj.led_onthouden(1, led_pos2)

        for key, value in win_combinaties.items():
            if (len(set(led_pos1) & set(value)) == 3) and (key not in oud_gekozen_pixelsR and key not in oud_gekozen_pixelsB):
                puntenR = motor_klasse_obj.puntentelling(0, puntenR)
                motor_klasse_obj.punt_bij(speler)
                oud_gekozen_pixelsR.append(key)

            elif len(set(led_pos2) & set(value)) == 3 and (key not in oud_gekozen_pixelsR and key not in oud_gekozen_pixelsB):
                puntenB = motor_klasse_obj.puntentelling(1, puntenB)
                motor_klasse_obj.punt_bij(speler)
                oud_gekozen_pixelsB.append(key)
        if max_punten == puntenR or max_punten == puntenB:
            print(f"stand van het spel: max: {max_punten}, R: {puntenR}, B:{puntenB}")
        if puntenR == max_punten:
            choice_running = False
            winnaar = "rood"
        elif puntenB == max_punten:
            choice_running = False
            winnaar = "blauw"
        time.sleep(0.02)
    if not choice_running:
        positie_lijst.clear()
        oud_gekozen_pixelsR.clear()
        oud_gekozen_pixelsB.clear()
        led_pos1.clear() 
        led_pos2.clear()
        neo_klasse_obj.eind_kleur(winnaar)
        if winnaar == "rood":
            DataRepository.create_game(puntenR, puntenB)
            socketio.emit('B2F_games', {'winnaar':"Rood"})
        elif winnaar == "blauw":
            DataRepository.create_game(puntenB, puntenR)
            socketio.emit('B2F_games', {'winnaar':"Blauw"})

        return winnaar, puntenR, puntenB

def positie(x, y, z, player, vorige_pos):
    neonummer = neo_klasse_obj.get_key(x, y, z, vorige_pos)
    if neonummer not in led_pos1 and neonummer not in led_pos2:
        neo_klasse_obj.player_color(player, neonummer)
    else:
        print("kies een andere led")
    time.sleep(0.3)
    return neonummer

def keuzelijst():
    global tellerKeuze, app_running, prev_teller19, teller19, prev_teller16, teller16
    while app_running and True:
        if tellerKeuze > 3:
                tellerKeuze = 3
        elif tellerKeuze < 0:
            tellerKeuze = 0

        if prev_teller19 == teller19 == prev_teller16 == teller16:
            oled_klasse_obj.lijst(tellerKeuze)
        else:
            ip = oled_klasse_obj.ip_adressen()
            prev_teller19 = teller19 = teller16 = prev_teller16
            socketio.emit('B2F_show_ip', {'ip_adres':ip[1]})
            time.sleep(1)

        socketio.emit('B2F_choice_oled', {'keuze':tellerKeuze})
        if GPIO.input(t1) or GPIO.input(t2):
            print(f"dit is de tellerKeuze: {tellerKeuze}")
            app_running = False
        else:
            time.sleep(0.02)
        time.sleep(0.5)
    if not app_running:
        return tellerKeuze

def spel_starten():
    global tellerKeuze, keuzeSpel, app_running, choice_running
    choice_running = True
    app_running = True
    tellerKeuze = 0
    keuzeSpel = keuzelijst() # => in oled ook 
    time.sleep(0.2)
    start_game()

def start_game():
    global kleur, player
    # alles uitzetten van de rgb
    GPIO.output(r, GPIO.LOW)
    GPIO.output(g, GPIO.LOW)
    GPIO.output(b, GPIO.LOW)
    randomPlayer = random.randint(1, 2)
    oled_klasse_obj.display_player(randomPlayer)
    if randomPlayer == 1:
        GPIO.output(r, GPIO.HIGH)
        kleur = "Rood"
    elif randomPlayer == 2:
        GPIO.output(b, GPIO.HIGH)
        kleur = 'Blauw'
    player = randomPlayer
    game(randomPlayer, tellerKeuze)

def game(beginner, tellerKeuze):
    global game_running, puntenR, puntenB
    puntenR = 0
    puntenB = 0
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
        time.sleep(1)
        neo_klasse_obj.start_kleur()
        winnaar, puntenR, puntenB = joystick_uitlezen(beginner, max_punten)
        print(f"dit is de winnaar: {winnaar}")
        game_running = False
    if not game_running:
        game_running = True
        tellerKeuze = 0
        spel_starten()

# #################### SOCKETIO #####################
@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e, "????")

@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    emit('B2F_connected', {'message': "hallo nieuwe user!"})

#################### ENDPOINTS #####################
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
        data = DataRepository.read_speler_by_id(playerID)
        if data is not None:
            return jsonify(speler = data), 200
        else:
            return jsonify(message = "error"), 404

# historiek/waarden
@app.route(endpoint + '/historiek/', methods = ['GET'])
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
        data = DataRepository.create_historiek(gegevens["deviceid"], gegevens["commentaar"], gegevens["waarde"], gegevens["actieid"])
        return jsonify(volgnummer = data), 201
    
#################### THREADS #####################
def start_thread():
    print("***** Starting THREAD *****")
    thread = threading.Thread(target = spel_starten, args = (), daemon = True)
    thread.start()

#################### SOCKETIO.RUN #####################

if __name__ == "__main__":
    try:
        time.sleep(1)
        setup()
        start_thread()
        print("**** Starting APP ****")
        socketio.run(app,debug = False, host = '0.0.0.0')
    except KeyboardInterrupt:
        print("kb")
    finally:
        oled_klasse_obj.oled_clear()
        time.sleep(1)
        print("cleanup pi")
        app_running = False
        joy_klasse_obj.closing()
        neo_klasse_obj.alles_uit()
        GPIO.cleanup()



