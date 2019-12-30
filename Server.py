#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pymouse import PyMouse
from pykeyboard import PyKeyboard
import socket
import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pyscreenshot as ImageGrab
import sys
import select
import threading
from tkinter import *
from tkinter import filedialog


# In[ ]:


keyDict =  {
            8 : 22,
            9 : 23,
            12 : 0,
            13 : 36,
            19 : 127,
            27 : 9,
            32 : 65,
            33 : 10,
            34 : 48,
            35 : 12,
            36 : 13,
            38 : 16,
            39 : 48,
            40 : 187,
            41 : 188,
            42 : 17,
            43 : 21,
            44 : 59,
            45 : 20,
            46 : 60,
            47 : 61,
            48 : 19,
            49 : 10,
            50 : 11,
            51 : 12,
            52 : 13,
            53 : 14,
            54 : 15,
            55 : 16,
            56 : 17,
            57 : 18,
            58 : 47,
            59 : 47,
            60 : 94,
            61 : 21,
            62 : 60,
            63 : 61,
            64 : 11,
            91 : 34,
            92 : 51,
            93 : 35,
            94 : 15,
            95 : 20,
            96 : 49,
            97 : 38,
            98 : 56,
            99 : 54,
            100 : 40,
            101 : 26,
            102 : 41,
            103 : 42,
            104 : 43,
            105 : 31,
            106 : 44,
            107 : 45,
            108 : 46,
            109 : 58,
            110 : 57,
            111 : 32,
            112 : 33,
            113 : 24,
            114 : 27,
            115 : 39,
            116 : 28,
            117 : 30,
            118 : 55,
            119 : 25,
            120 : 53,
            121 : 29,
            122 : 52,
            127 : 119,
            256 : 19,
            257 : 10,
            258 : 11,
            259 : 12,
            260 : 13,
            261 : 14,
            262 : 15,
            263 : 16,
            264 : 17,
            265 : 18,
            266 : 60,
            267 : 61,
            268 : 17,
            269 : 20,
            270 : 21,
            271 : 36,
            272 : 21,
            273 : 111,
            274 : 116,
            275 : 114,
            276 : 113,
            277 : 118,
            278 : 110,
            279 : 115,
            280 : 112,
            281 : 117,
            282 : 67,
            283 : 68,
            284 : 69,
            285 : 70,
            286 : 71,
            287 : 72,
            288 : 73,
            289 : 74,
            290 : 75,
            291 : 76,
            292 : 95,
            293 : 96,
            300 : 77,
            301 : 66,
            302 : 78,
            303 : 62,
            304 : 50,
            305 : 105,
            306 : 37,
            307 : 108,
            308 : 64,
            311 : 133,
            312 : 134,
            313 : 92,
            315 : 146,
            316 : 107,
            317 : 107,
            318 : 127
           }


# In[ ]:


SELFIP = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] 
if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), 
s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, 
socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
IP = "192.168.1.110"
PORT = 12345
RES = (PyMouse().screen_size()[0] - 1, PyMouse().screen_size()[1] - 1, 0)
CRES = (1920, 1080, 0)
os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"
lastSS = 0
Broadcasters = []
LOC = 3
condition = [PyMouse().position, pygame.mouse.get_pos]
cI = [0,-1,0]


# In[ ]:


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


# In[ ]:


def broadcastListener():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(5)
    s.bind(('', PORT))
    s.setblocking(0)
    result = select.select([s],[],[],10)
    if result[0]:
        packet = result[0][0].recv(1024)
        s.close()
        return packet.decode()
    else:
        s.close()
        return None


# In[ ]:


while True:
    print("Waiting for new client...")
    newClient = broadcastListener()
    if newClient and newClient not in Broadcasters:
        Broadcasters.append(newClient)
    print('[0] Keep looking')
    for i in range(len(Broadcasters)):
        print('[' + str(i+1) + ']', Broadcasters[i])
    dest = int(input("Select Client: "))
    if dest ==  0:
        cls()
        continue
    else:
        cls()
        print(Broadcasters[dest-1].split("|")[1], "has been selected as client.")
        IP = Broadcasters[dest-1].split("|")[0]
        CRES = Broadcasters[dest-1].split("|")[2]
        CRES = (int(CRES.split(",")[0]), int(CRES.split(",")[1]), 0)
        break


# In[ ]:


prompt = """
               [1]UP
          ----------------
         |                |
         |     Server     |
 [2]LEFT |                | [3] RIGHT
         |     Screen     |
         |                |
          ----------------
               [4]DOWN
"""


# In[ ]:


while True:
    try:
        print(prompt)
        LOC = int(input("\nSelect the location of the client: "))
        if LOC not in [1,2,3,4]:
            cls()
            continue
        elif LOC == 1:
            cI = [-1,1,1]
            break
        elif LOC == 2:
            cI = [-1,0,0]
            break
        elif LOC == 3:
            cI = [0,-1,0]
            break
        elif LOC == 4:
            cI = [1,-1,1]
            break
    except ValueError:
        continue


# In[ ]:


def share():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpTuple = (IP, PORT)
        while True:
            # ON SELF
            while not condition[0]()[cI[2]] == RES[cI[0]]:
                continue
            posbeforetoggle = (abs(CRES[cI[1]] - 5), int(condition[0]()[1] / (RES[1]+1) * CRES[1])) if LOC in [2,3] else (int(condition[0]()[0] / (RES[0]+1) * CRES[0]) ,abs(CRES[cI[1]] - 5)) 
            pygame.init()
            os.system("import -window root screen.png")
            lastSS = time.time()
            screen = pygame.display.set_mode((RES[0]+1, RES[1]+1), pygame.NOFRAME)
            screen = pygame.display.set_mode((RES[0]+1, RES[1]+1), pygame.NOFRAME)
            background_image = pygame.image.load('screen.png').convert()
            screen.blit(background_image, (0,0))
            pygame.display.flip()
            pygame.mouse.set_pos(posbeforetoggle)
            pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
            pygame.event.set_grab(True)

            # ON CLIENT
    #         SS = threading.Thread(name='takeSS', target=takeSS)
    #         SS.start()
            while True:
                if condition[1]()[cI[2]] == RES[cI[1]]:
                    pygame.mouse.set_pos((abs(RES[cI[0]]-1), int(condition[1]()[1] / CRES[1] * (RES[1]+1)))) if LOC in [2,3] else pygame.mouse.set_pos((int(condition[1]()[0] / CRES[0] * (RES[0]+1)), abs(RES[cI[0]]-1)))
                    break
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEMOTION:
                        posbeforetoggle = pygame.mouse.get_pos()
                        s.sendto(("M," + str(posbeforetoggle[0]) + "," + str(posbeforetoggle[1])).encode(), udpTuple)
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button in [1,2,3]:
                        s.sendto(("P," + str(event.pos[0]) + "," + str(event.pos[1]) + "," + str(int(-3* (event.button**2)/2 + (13*event.button)/2 - 4))).encode(), udpTuple)
                    elif event.type == pygame.MOUSEBUTTONUP and event.button in [1,2,3]:
                        s.sendto(("R," + str(event.pos[0]) + "," + str(event.pos[1]) + "," + str(int(-3* (event.button**2)/2 + (13*event.button)/2 - 4))).encode(), udpTuple)
                    elif event.type == pygame.KEYDOWN:
                        s.sendto(("P," + str(keyDict[event.key])).encode(), udpTuple)
                    elif event.type == pygame.KEYUP:
                        s.sendto(("R," + str(keyDict[event.key])).encode(), udpTuple)

            pygame.quit()
    #         SS.do_run = False
    #         SS.join()
    except:
        print("Exited!")
        pygame.quit()


# In[ ]:


def receivefile(file):
    count = 1
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((SELFIP, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        f = open(file + str(count),'wb')
        while True:
            bytepart = conn.recv(1024)
            if not bytepart:
                break
            f.write(bytepart)
            f.flush()
        f.close()
        conn.close()
        count += 1
        print("\n A file has been received")
    s.close()


# In[ ]:


def sendfile(file, ClientIP):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ClientIP,PORT))
    f = open(file, "rb")
    part = f.read(1024)
    while part:
        s.sendall(part)
        part = f.read(1024)
    f.close()
    s.close()
    cls()
    print(file.split("/")[-1], "has been sent!")


# In[ ]:


def selectFile():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path


# In[ ]:


shareThread = threading.Thread(name='share', target=share)
shareThread.start()
recvFile = threading.Thread(name='receivefile', target=receivefile, args=("receivedFile",))
recvFile.start()


# In[ ]:


while True:
    input("Press Enter to Share File")
    path = selectFile()
    if not path == '':
        sendfile(path, IP)


# In[ ]:




