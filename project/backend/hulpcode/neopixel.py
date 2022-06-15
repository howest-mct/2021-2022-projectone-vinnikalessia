import time
import board
import neopixel


pixel_pin = board.D18
num_pixels = 27
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

neopixel_dict = {
        0:[1, 1, 1], 1:[2, 1, 1], 2:[3, 1, 1], 
        3:[3, 2, 1], 4:[2, 2, 1], 5:[1, 2, 1],
        6:[1, 3, 1], 7:[2, 3, 1], 8:[3, 3, 1],

        9:[3, 3, 2], 10:[2, 3, 2], 11:[1, 3, 2], 
        12:[1, 2, 2], 13:[2, 2, 2], 14:[3, 2, 2],
        15:[3, 1, 2], 16:[2, 1, 2], 17:[1, 1, 2],

        18:[1, 1, 3], 19:[2, 1, 3], 20:[3, 1, 3], 
        21:[3, 2, 3], 22:[2, 2, 3], 23:[1, 2, 3],
        24:[1, 3, 3], 25:[2, 3, 3], 26:[3, 3, 3],
        }

class Neos_klasse():
    def clear_pixel(self, i): 
        pixels[i] = (0,0,0)
        pixels.show()
    
    def wheel(self, pos):
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


    def rainbow_cycle(self, wait):
        global num_pixels
        for j in range(255):
            for i in range(num_pixels):
                pixel_index = (i * 256 // num_pixels) + j
                pixels[i] = Neos_klasse.wheel(pixel_index & 255)
            pixels.show()
            time.sleep(wait)

    
    def chosen_one(self, getal, speler):
        print(f"dit is de player: {speler} {getal}")
        if speler == 0:
            # rood
            pixels[getal] = (255,0,0)
        else:
            # blauw
            pixels[getal] = (0,0,255)
        pixels.show()
        # time.sleep(0.2)


    ##### kijken of combinatie klopt #####
    # def get_key(val):
    def get_key(self, x, y, z):
        val = []
        val.append(x)
        val.append(y)
        val.append(z)
        for key, value in neopixel_dict.items():
            if val == value:
                print("key exists JIPPY")
                print(val)
                return key
        return "key doesn't exist"

    def start_kleur(self):
        pixels.fill((0, 255, 0))
        pixels.show()
        time.sleep(1)
        pixels.fill((0, 0, 0))
        pixels.show()
    
    def eind_kleur(self, winnaar):
        for i in range(3):
            if winnaar == "rood":
                pixels.fill((255, 0, 0))
                print("rood heeft gewonnen")
            elif winnaar == "blauw":
                pixels.fill((0, 0, 255))
                print("blauw heeft gewonnen")
            pixels.show()
            time.sleep(0.2)
            pixels.fill((0, 0, 0))
            pixels.show()
            time.sleep(0.2)

    def alles_uit(self):
        pixels.fill((0, 0, 0))
        pixels.show()

    def player_color(self, player, coordinaten):
        if player == 0:
            pixels[coordinaten] = (255,0,0)
        else:
            pixels[coordinaten] = (0,0,255)
        pixels.show()

    def bezet(self, pixel):
        pixels[pixel] = (255,255,0)
        # if player == 0:
        #     pixels[pixel] = (255,0,0)
        # else:
        #     pixels[pixel] = (0,0,255)
        pixels.show()
        time.sleep(0.2)

    def led_onthouden(self, player, ledpos):
        if player == 0:
            for i in ledpos:
                pixels[i] = (255,0,0)
                pixels.show()
        else:
            for i in ledpos:
                pixels[i] = (0,0,255)
                pixels.show()
    
    def vorige_positie(self, vorige_pos):
        pixels[vorige_pos] = (0,0,0)
    
    def show_pixels(self):
        pixels.show()
        