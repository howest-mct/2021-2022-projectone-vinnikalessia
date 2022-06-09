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
# x (horizontaal), y (verticaal), z (hoogte)
lijst = {
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



print(lijst)
msg = [1, 1, 1]

print(lijst[1])

if msg == lijst[1]:
	print("yes")
else:
	print("nope")

def get_key(val):
    for key, value in lijst.items():
         if val == value:
             return key
    return "key doesn't exist"
 
print(get_key(msg))

