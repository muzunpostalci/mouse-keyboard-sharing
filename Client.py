#!/usr/bin/env python
# coding: utf-8

# In[9]:


from pymouse import PyMouse
from pykeyboard import PyKeyboard
import socket
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import threading
from tkinter import *
from tkinter import filedialog


# In[ ]:


IP = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] 
if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), 
s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, 
socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
SERVERIP = ""


# In[ ]:


os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"
PORT = 12345
HOSTNAME = socket.gethostname()
RES = PyMouse().screen_size()


# In[ ]:


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


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


def receivefile(file):
    count = 1
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, PORT))
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
        print("\nA file has been received")
    s.close()


# In[ ]:


def selectFile():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path


# In[ ]:


def broadcast():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('',0))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto((IP + "|" + HOSTNAME + "|" + str(RES[0]) + "," + str(RES[1])).encode(), ('<broadcast>', PORT))
    sock.close()


# In[ ]:


while True:
    try:
        print("[0] Broadcast")
        print("[1] Start Listening")
        print("[2] Quit")
        sel = int(input("Make selection: "))
        if sel == 0:
            cls()
            broadcast()
        elif sel == 1:
            cls()
            break
        elif sel == 2:
            cls()
            sys.exit()
    except (ValueError, TypeError):
        cls()
        continue


# In[ ]:


def recvInput():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((IP, PORT))
        data, addr = s.recvfrom(20)
        global SERVERIP
        SERVERIP = addr[0]
        pygame.init()
        screen = pygame.display.set_mode((1920,1080), pygame.NOFRAME)
        screen = pygame.display.set_mode((1920,1080), pygame.NOFRAME)
        pygame.display.set_icon(pygame.image.load('assets/icon.png'))
        pygame.display.iconify()
        while True:
            data, addr = s.recvfrom(20)
            data = data.decode().split(",")
            if len(data) == 3:
                pygame.mouse.set_pos(int(data[1]),int(data[2]))
            elif len(data) == 4:
                if data[0] == "P":
                    PyMouse().press(int(data[1]), int(data[2]), int(data[3]))
                else:
                    PyMouse().release(int(data[1]), int(data[2]), int(data[3]))
            else:
                if data[0] == "P":
                    PyKeyboard().press_key(int(data[1]))
                else:
                    PyKeyboard().release_key(int(data[1]))
    except:
        s.close()
        pygame.quit()


# In[ ]:


recvThread = threading.Thread(name="recvInput", target=recvInput)
recvThread.start()
recvFile = threading.Thread(name="receivefile", target=receivefile,args=("receivedFile",))
recvFile.start()


# In[ ]:


while True:
    input("Press Enter to Share File")
    path = selectFile()
    if not path == '':
        sendfile(path, SERVERIP)

