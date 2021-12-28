from .Utils import liveScreen, touch
from .Utils import findImage
from .Utils import find_matches
from .Utils import restart
import subprocess
import threading
import cv2
import numpy as np
import os
import time
doneHallOfGreed = 0
stepHallOfGreed = 0
working = False
import random
def loopHallOfGreed():
    #time.sleep(5)
    threading.Timer(32.0, loopHallOfGreed).start()
    doHallOfGreed()


def doHallOfGreed():
    global doneHallOfGreed
    global stepHallOfGreed
    liveScreen()
    time.sleep(2)
    if doneHallOfGreed == 1:
        print("Já terminou ganância")
        return True
    checkSteps()


def checkSteps():
    global stepHallOfGreed
    global doneHallOfGreed
    global working
    if working == True:
        print("Já está trabalhando em outro macro")
        return False
    else:
        restart()
        time.sleep(2)
        
    print("Passo  : " + str(stepHallOfGreed))
    #inprogress = chekingInProgress()
    # I'm Hall of Greed
    if ImField() == True:
        print("Hall of Greed")
        stepHallOfGreed = 1
    else: # se tiver alguma doacao tenta de novo dps de 10s
        backHallOfGreed()
        
    # aqui embaixo da problema no código
    if stepHallOfGreed == 1:
        # if checkIfIInHallOfGreed():
        # print("I not Hall of Greed")
        # backHallOfGreed()
        # el
        if doneHallOfGreed == True:
            print("Hall of Greed")
            #stepHallOfGreed = 1
        elif checkExist("Resources\hall.png") :
            print("Hall of Greed progress points")
        elif doneHallOfGreed == False and chekingIsDone() and ImField() == True:
            stepHallOfGreed = 1
            touch(1160, 114)
            time.sleep(3) # talvez nem precise mais de sleep
            touch(940, 600)
            time.sleep(3) # talvez nem precise mais de sleep
            print("Hall of Greed, Finished")

def ImField():
    global working
    working = True
    image = cv2.imread("now.png")
    hsv = image# cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    crop_img = hsv[93:138, 1143:1181]  # SS
    cv2.imwrite("canleave.png", crop_img)
    BLUE_MIN = np.array([0,0,180], np.uint8)
    BLUE_MAX = np.array([255,255,255], np.uint8)
    dst = cv2.inRange(crop_img, BLUE_MIN, BLUE_MAX)
    no_blue = cv2.countNonZero(dst)
    print('white pixels is: ' + str(no_blue)+" is field ?")
    working = False
    if no_blue >= 400:
        return True
    else:
        return False


def backHallOfGreed():
    global stepHallOfGreed
    global working
    working = True
    print("Backing to hall of greed")
    touch(800, 604)  # click ok Message
    time.sleep(2)
    touch(1155, 36)
    time.sleep(2)
    touch(590, 815)
    time.sleep(3)
    touch(375, 653)
    time.sleep(3)
    touch(1156, 665)
    time.sleep(3)
    touch(1350, 805)  # enter hall of greed
    time.sleep(10)
    goTOSpot()
    working = False
    stepHallOfGreed = 1
    

def goTOSpot():
    working = True
    touch(1480, 110)  # click map
    time.sleep(5)
    if random.randint(0,100) < 50:
        touch(572, 644)  # select spot
    else:
        touch(517, 642)  # select spot
   
    time.sleep(30)
    touch(1090, 850)  # auto
    time.sleep(2)
    touch(1500, 345)  # start if avaiable
    time.sleep(2)
    touch(203, 330)  # auto
    time.sleep(2)
    touch(800, 604)  # click ok Message
    
    
def chekingInProgress():
    image = cv2.imread("now.png")
    crop_img = image[279:297, 1440:1531]  # SS
    hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
    BLUE_MIN = np.array([22, 93, 0], np.uint8)
    BLUE_MAX = np.array([45, 255, 255], np.uint8)
    dst = cv2.inRange(hsv, BLUE_MIN, BLUE_MAX)
    no_blue = cv2.countNonZero(dst)
    print('The number of yellow pixels is: ' + str(no_blue))
    if no_blue >= 700:
        return True
    else:
        return False


def chekingIsDone():
    image = cv2.imread("now.png")
    crop_img = image[279:297, 1440:1531]  # SS
    #BLUE_MIN = np.array([23, 0, 0], np.uint8)
    #BLUE_MAX = np.array([255, 255, 255], np.uint8)
    BLUE_MIN = np.array([0,0,180], np.uint8)
    BLUE_MAX = np.array([255,255,255], np.uint8)
    dst = cv2.inRange(crop_img, BLUE_MIN, BLUE_MAX)
    no_blue = cv2.countNonZero(dst)
    print('The number of white pixels is: ' + str(no_blue))
    if no_blue >= 500:
        return True
    else:
        return False


def checkisLogged():
    global logged
    global loggedStep
    if checkExist("Resources\pot.png"):
        print("Character Logged")
        loggedStep = 0
        logged = 1
    elif checkExist("Resources\pot2.png"):
        print("Character Logged")
        loggedStep = 0
        logged = 1
    elif checkExist("Resources\buttom.png"):
        print("Character Logged")
        loggedStep = 0
        logged = 1


def findMyChar():
    global loggedStep
    if checkExist("Resources\loaded.png"):
        loggedStep = 3  # step waiting for login
        touch(1415, 768)
    elif checkExist("Resources\loaded2.png"):
        loggedStep = 3  # step waiting for login
        touch(1415, 768)
    elif checkExist("Resources\loaded3.png"):
        loggedStep = 3  # step waiting for login
        touch(1415, 768)
    else:
        print("Ainda não carregou")


def checkIfIInHallOfGreed():
    now = cv2.imread("now.png", 0)
    #find = cv2.imread("Resources\castle.png")
    crop_img = now[172:223, 1537:1590]  # SS
    BLUE_MIN = np.array([23, 0, 0], np.uint8)
    BLUE_MAX = np.array([255, 255, 255], np.uint8)
    dst = cv2.inRange(crop_img, BLUE_MIN, BLUE_MAX)
    no_blue = cv2.countNonZero(dst)
    print('The number of white pixels is: ' + str(no_blue) + ' on castle icon')
    if no_blue >= 1500:
        return True
    else:
        return False


def checkExist(pic):
    now = cv2.imread("now.png", 0)
    find = cv2.imread(pic,0)
    found = findImage(now, find)
    if found :
        return True
    else:
        return False


def checkL2isOpen():
    global loggedStep
    now = cv2.imread("now.png")
    lauch = cv2.imread("Resources\lauch.png")
    positions = find_matches(now, lauch)
    print("Verificando se Emulador está pronto")
    print(positions)
    if len(positions) > 0:
        x = positions[0][0]
        y = positions[0][1]
        print("Abrindo ....")
        touch(x, y)
        loggedStep = 2  # step waiting for login
    else:
        restart()
        print("Emulador não está pronto ainda")


def openL2():
    os.startfile("C:\LDPlayer\LDPlayer64\dnplayer.exe")


def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())
