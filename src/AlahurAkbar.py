from .Utils import liveScreen, touch
from .Utils import findImage
import cv2
import threading
import time
from .Utils import restart
finished = 0
currentStep = 0  # step 0 = no runinng scroll, 1 = Select Scroll, 2 = Confirm Scroll, 3 = Start Scroll, 4 = walk, 5 = Doing, 6 = Claim
inExecution = 0
# falta verificar se a imagem now esta com o tamanho >=1 evita erros
# verificar passo padrao atual
# verificar se ja acabou


def loopAlahurAkbar():
    # restart()
    threading.Timer(185.0, loopAlahurAkbar).start()
    doAlahurAkbar()


def doAlahurAkbar():
    global finished
    global currentStep
    global inExecution
    if inExecution == 0:
        liveScreen()
        inExecution = 1
        checkDie()
        checkStep()
        inExecution = 0

# change step 1-3 to close dialogs and step 4 is final quest


def checkStep():
    global currentStep
    print("Alahur Akbar !!")  # verificar qual passo esta baseado em prints
    touch(925, 32)  # go to Dungeon
    time.sleep(1)
    touch(300, 666)  # Click in Dungeon
    time.sleep(2)
    touch(123, 520)  # touch(235, 400)
    time.sleep(2)
    touch(690, 374)  # touch in elite
    time.sleep(2)
    touch(1108, 657)  # touch in enter
    time.sleep(10)
    touch(1181, 92)  # touch in map
    time.sleep(4)
    touch(456, 384)  # select spot to attack
    time.sleep(15)
    touch(869, 684)  # select auto attack this shit
    time.sleep(25)
    backToQuests()
  


def checkCompleted():
    global finished
    global currentStep
    now = cv2.imread("now.png")
    completed = cv2.imread("Resources\quest_completed.png")
    check = findImage(now, completed)
    if check == "FOUND":
        print("Quests Done")
        finished = 10
        currentStep = 0
    else:
        print("Quests not done yet")


def checkDie():
    image = cv2.imread("now.png")
    die = cv2.imread("Resources\die.png")
    status = findImage(image, die)
    if(status == "FOUND"):
        print("I Die")
        backToQuests()
    else:
        print("I Living")

def backToQuests():
    print("Back to position")
    touch(1140, 535)  # revive
    time.sleep(3)
    touch(1239, 250)  # close alert
    time.sleep(2)
    touch(860, 92)  # leave
    time.sleep(15)
    touch(1242, 41)  # leave to main screen


def step00():
    global currentStep
    print("Start Scroll Quests")
    touch(119, 394)  # touch(235, 400)
    time.sleep(2)
    currentStep = 1  # run to NPC


def detectCurrentStep():
    global currentStep
    global finished
    now = cv2.imread("now.png")
    closeDialog = cv2.imread("Resources\step1.png")
    print(closeDialog.shape)
    # (h, w, d) = image.shape
    #row = cv2.imread("Resources\row.png")
    #print(row.shape)
    #name2 = cv2.imread("Resources\row2.png")
    teleportPNG = cv2.imread("Resources\step_teleport.png")
    check = findImage(now, closeDialog)
    #checkName = findImage(now, row)
    #checkName2 = findImage(now, name2)
    checkTeleport = findImage(now, teleportPNG)
    claim = cv2.imread("Resources\claim.png")
    checkClaim = findImage(now, claim)
    start = cv2.imread("Resources\start.png")
    checkStart = findImage(now, start)
    okIMG = cv2.imread("Resources\ok.png")
    checkOK = findImage(now, okIMG)
    if check == "FOUND":
        print("Tap in Fulfill request")
        time.sleep(1)
        touch(930, 541)  # click in fulfill request 1280x720
        time.sleep(1)
        currentStep = 2
    #elif checkName == "FOUND" :
    #    currentStep = 5
    #elif checkName2 == "FOUND" :
    #    currentStep = 5
    elif checkTeleport == "FOUND" :
        print("Tap in run")
        touch(495, 522)  # tap in run 1280x720
        currentStep = 5  # doing
    elif checkClaim == "FOUND":
        print("Claim reward")
        touch(641, 612)  # tap claim reward 1280x720
        time.sleep(1)
        currentStep = 0  # finished
        finished += 1
    elif checkStart == "FOUND":
        touch(760, 612)  # Click in Start quest 1280x720
        currentStep = 4  # run quest
    elif checkOK == "FOUND":
        touch(758, 500)  # Click in OK to accept quest 1280x720
        time.sleep(2)
        currentStep = 3  # start quest

def step01():
    global currentStep
    print("Checking Step 2")
    now = cv2.imread("now.png")
    closeDialog = cv2.imread("Resources\step1.png")
    check = findImage(now, closeDialog)
    if check == "FOUND":
        print("Tap in Fulfill request")
        time.sleep(1)
        touch(930, 541)  # click in fulfill request 1280x720
        time.sleep(1)
        currentStep = 2
    else:
        teleportPNG = cv2.imread("Resources\step_teleport.png")
        checkTeleport = findImage(now, teleportPNG)
        if checkTeleport == "FOUND":
            print("Tap in run")
            touch(495, 522)  # tap in run 1280x720
            time.sleep(2)
            currentStep = 4
        else:
            print("Unknow Step, checking again")
            currentStep = 2


def incorrectStatus():
    now = cv2.imread("now.png")
    closeDialog = cv2.imread("Resources\summoningCircle.png")
    check = findImage(now, closeDialog)
    if check == "FOUND":
        touch(790, 600)


def step011():
    global currentStep
    global finished
    # try close all NPC dialogs printed
    # if checkCloseDialog():
    # close dialog and start quest
    #    touch(1490, 650)
    #    currentStep = 2
    # final quest
    now = cv2.imread("now.png")
    closeDialog = cv2.imread("Resources\claim.png")
    check = findImage(now, closeDialog)
    if check == "FOUND":
        # claim reward
        print("Claim")
        touch(641, 612)
        time.sleep(1)
        currentStep = 0
        finished += 1
    else:
        print("Not done yet")
        touch(1188, 509)  # click SKIP 1280x720
        time.sleep(1)
        touch(1490, 650)
        currentStep = 1


def step02():
    global currentStep
    now = cv2.imread("now.png")
    okIMG = cv2.imread("Resources\ok.png")
    checkOK = findImage(now, okIMG)
    if checkOK == "FOUND":
        touch(758, 500)  # Click in OK to accept quest 1280x720
        time.sleep(2)
        currentStep = 3  # start quest


def step03():
    global currentStep
    now = cv2.imread("now.png")
    start = cv2.imread("Resources\start.png")
    checkStart = findImage(now, start)
    if checkStart == "FOUND":
        touch(760, 612)  # Click in Start quest 1280x720
        time.sleep(2)
        currentStep = 4  # run quest


def step04():
    global currentStep
    now = cv2.imread("now.png")
    teleportPNG = cv2.imread("Resources\step_teleport.png")
    checkTeleport = findImage(now, teleportPNG)
    if checkTeleport == "FOUND":
        print("Tap in run")
        touch(495, 522)  # tap in run 1280x720
        time.sleep(2)
        currentStep = 5  # doing
    else:
        print("Unknow Step, checking again")
        currentStep = 4


def step05():
    global currentStep
    global finished
    now = cv2.imread("now.png")
    claim = cv2.imread("Resources\claim.png")
    checkClaim = findImage(now, claim)
    if checkClaim == "FOUND":
        print("Claim reward")
        touch(641, 612)  # tap claim reward 1280x720
        currentStep = 0  # finished
        finished += 1
    else:
        print("Not finish yet")
        touch(1195, 522)  # click SKIP 1280x720
        time.sleep(1)
        touch(1490, 650)
        currentStep = 5


def step045():
    global currentStep
    global finished
    now = cv2.imread("now.png")
    closeDialog = cv2.imread("Resources\claim.png")
    check = findImage(now, closeDialog)
    if check == "FOUND":
        # claim reward
        touch(790, 765)
        currentStep = 0
        finished += 1
