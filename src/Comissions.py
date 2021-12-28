from .Utils import liveScreen, touch
from .Utils import findImage
import cv2
import threading
import time
from .Utils import restart
finished = 0
currentStep = 0

def checkExist(pic):
    now = cv2.imread("now.png", 0)
    find = cv2.imread(pic,0)
    found = findImage(now, find)
    if found == "FOUND":
        return True
    else:
        return False

# so falta verificar se tem alguma tarefa em execucao
def loopComissions():
    restart()
    time.sleep(3)
    threading.Timer(420.0, loopComissions).start()  # every 7 minutes
    doComissions()


def doComissions():
    global finished
    global currentStep
    touch(1015, 78)  # close clan donation
    time.sleep(1)
    touch(1015, 78)  # close clan donation
    time.sleep(1)
    touch(1015, 78)  # close clan donation
    time.sleep(1)
    touch(1155, 40)  # close clan donation
    time.sleep(2)
    touch(500, 70)  # click in Item
    time.sleep(2)
    touch(1309, 222)  # click in Main Professions
    time.sleep(2)
    touch(870, 150)  # click in Comissions Office
    time.sleep(2)
    touch(80, 570)  # click in Craft History
    time.sleep(2)
    touch(1444, 850)  # click in Claim All
    time.sleep(2)
    touch(80, 250)  # click in Comissions
    time.sleep(2)
    liveScreen()
    time.sleep(5)
    if checkExist("Resources\comissions_empty.png") == True :
        print("No Comissions")
        return False
    
    if checkExist("Resources\comissions_max.png") == True :
        print("Comissions Reached max limit")
        return False
    # esta faltando a foto com 5
    
    # improve checking if comission are avaiable
    for i in range(15):
        touch(1485, 400)  # click in Accept
        time.sleep(2)
        touch(800, 588)  # click in OK, avaiable or reached max limit
        time.sleep(2)
        
    time.sleep(1)
    touch(1560, 50)  # click in Back to main screen
# change step 1-3 to close dialogs and step 4 is final quest


def checkStep():
    global currentStep
    print("Verificando Passos")  # verificar qual passo esta baseado em prints
    if currentStep == 0:  # click to see quests
        print("Passo 0")
        step00()  # melhorar aqui
    elif currentStep > 0:  # run to NPC
        print("Passo 1")
        step01()


def step00():
    global currentStep
    print("Start Scroll Quests")
    # tap
    touch(235, 400)
    time.sleep(4)
    touch(1130, 800)  # select
    time.sleep(4)
    touch(950, 600)  # ok
    time.sleep(4)
    # start quest
    touch(950, 760)  # start
    time.sleep(4)
    # walk
    touch(620, 650)  # run
    currentStep = 1  # run to NPC
