from asyncio.windows_events import NULL
from tkinter.messagebox import NO
from .Utils import countPixelsInPosition_NOW, checkExist_NOW, restartL2, liveScreen, touch, extractText, extractTextFromResize, countPixelsInPosition
from .Utils import findImage
import cv2
import threading
import time
from .Utils import restart
from datetime import date, timedelta, datetime
import numpy as np
import os
from .loginL2 import checkStopService, checkExist

positionsCropIconDoing = [[348, 244, 5, 5], [390, 244, 5, 5]]
positionsTexAvaiableQuest = [[348, 244, 5, 5], [302, 10, 25, 10]]
positionsText1IconDoing = [[348, 244, 5, 5], [222, 11, 10, 10]]
positionsCrop = [[348, 244, 5, 5], [275, 9, 220, 50]]
# position to click in scroll quest, 0 is seconds position and 1 is third, 2 is first position
positions = [[110, 225], [110, 341]]
position = None  # None # se current position of "Avaiable Sub-quests"
scrollQuestIsDone = 1
finished = 0
currentStep = 0  # step 0 = no runinng scroll, 1 = Select Scroll, 2 = Confirm Scroll, 3 = Start Scroll, 4 = walk, 5 = Doing, 6 = Claim
inExecution = 0
lastStep = 0
thread = False
now = None
Try = 0
scrollA = cv2.imread("Resources\Screenshot_20220129-192543.png")
scrollCraft = cv2.imread("Resources\Screenshot_20220209-214356.png")
die = cv2.imread("Resources\die.png")
# BUGS/IMPROVEMENTS
# 1. Deixar mais rápido
# 2. Verificar se está em campo aberto


def loopScrollQuest():
    global thread
    if thread != False and thread.isAlive():
        thread.join()
    thread = threading.Timer(6.0, doScrollQuest)
    thread.daemon = True  # stop if the program exits
    thread.start()


def doScrollQuest():
    global finished, now, Try, position, currentStep, inExecution, scrollQuestIsDone, thread
    from .loginL2 import logged
    from .loginL2 import text  # extracted text
    from .DailyDungeon import DailyDungeonIsDone
    from .TempleGuardian import finishedTempleGuardian
    from .TowerOfInsolence import TowerOfInsolenceIsDone
    from .EliteQuest import EliteQuestIsDone

    if not logged or not EliteQuestIsDone or not TowerOfInsolenceIsDone or not DailyDungeonIsDone or finishedTempleGuardian == 0 or scrollQuestIsDone == 1:
        return False

    print("======== Daily Quest =========== ")
    liveScreen()
    if os.path.isfile('./now.png') == True:
        now = cv2.imread("now.png")
        if now is None:
            Try += 1
            print("Current Screen not found #"+str(Try))
            time.sleep(3)  # skip to next thread execution
            if Try >= 15:
                Try = 0
                logged = 0
                restartL2()
            return False
        size = os.path.getsize("./now.png")
        if size < 200:
            print("problem with current screen : " + str(size))

        assert not isinstance(now, type(None)), 'image not found'
        Try = 0
        if position == None:
            detectDefaultPosition()

        checkMainTab()
        checkMapisOpened()
        checkStopService()
        checkDie()
        checkStep()
    print("======== Done Daily Quest =========== ")


def checkMapisOpened():
    if checkExist("Resources\openmap.png"):
        touch(1244, 40)
        return True
    return False


def checkMainTab():
    if countPixelsInPosition(164, 69, 50, 2, [75, 154, 255], 50, 60):
        print("swith to main tab")
        touch(30, 180)
        return True
    return False


def checkStep():
    global currentStep
    global lastStep
    lastStep = currentStep
    print("Cheking Steps")  # verificar qual passo esta baseado em prints
    if position is not None:
        checkCompleted()
        detectCurrentStep()


def checkCompleted():
    global finished, scrollQuestIsDone, currentStep, now, scrollA, scrollCraft
    from .loginL2 import text  # extracted text
    if (findImage(now, scrollA) or findImage(now, scrollCraft)) and not countPixelsInPosition_NOW(504, 630, 200, 80, [52, 104, 72], 30, 300, now):
        print("Scroll quest finished")
        return setLikeDone()


def detectDefaultPosition():
    # find Main Quest ( Yellow tons )
    global now, position, positionsText1IconDoing
    if not detectMainScreen():
        return False

    if countPixelsInPosition_NOW(214, 283, 30, 30, [255, 247, 78], 1, 50, now):
        position = 1
        print("Main quest detected")
        return False
    elif countPixelsInPosition_NOW(222, 10, 25, 10, [255,174,0], 1, 100, now): # detect yellow tons
        position = 1
        print("Main quest detected")
        return False
    else:
        position = 0
        return False


def setLikeDone(close=True):
    global finished, currentStep, scrollQuestIsDone, thread
    print("Scroll quests is done")
    if close:
        touch(1014, 172)  # touch in close
    time.sleep(2)
    finished = 10
    currentStep = 0
    scrollQuestIsDone = 1
    thread.cancel()
    return True


def checkDie():
    global now, die
    if now is None:
        time.sleep(5)  # skip to next thread execution
        return False
    status = findImage(now, die)
    if status:
        print("I Die")
        backToQuests()


def backToQuests():
    print("Back to Quest")
    touch(637, 480)  # click in OK
    time.sleep(1)
    touch(637, 480)  # click in OK
    time.sleep(2)
    touch(1140, 535)  # revive
    time.sleep(6)
    touch(1239, 250)  # close alert
    time.sleep(2)
    touch(positions[position][0], positions[position][1])  # touch(235, 400)


def step00():
    global currentStep
    print("Start Scroll Quests")
    touch(positions[position][0], positions[position][1])  # touch(235, 400)
    time.sleep(5)
    currentStep = 1  # run to NPC


def detectCurrentStep():
    global currentStep, now, positions, position, finished, positionsCrop,scrollQuestIsDone
    from .loginL2 import text  # extracted text
    if now is None:
        time.sleep(5)  # skip to next thread execution
        return False
    if scrollQuestIsDone == 1:
        return False
    closeDialog = cv2.imread("Resources\step1.png")
    claim = cv2.imread("Resources\claim.png")
    start = cv2.imread("Resources\start.png")
    okIMG = cv2.imread("Resources\ok.png")
    monsterCard = cv2.imread("Resources\Screenshot_20211219-125109.png")
    if countPixelsInPosition(450, 645, 240, 60, [49, 77, 107], 450, 600):
        print("Touch in OK 0")
        touch(764, 483)  # Click in OK to accept quest 1280x720
        time.sleep(5)
        currentStep = 3  # start quest
        return True
    elif findImage(now, monsterCard):
        print("Close Dialog and start Quest")
        touch(788, 488)  # Tap in close moster card dialog
        time.sleep(1)
        touch(670, 610)  # Tap in Start Quest
        time.sleep(4)
        touch(492, 518)  # Tap in walk
        time.sleep(4)
        currentStep = 3  # start quest
        return True
    elif countPixelsInPosition_NOW(581, 379, 500, 60, [49, 77, 107], 850, 1500,now):
        print("Claim reward 0")
        touch(641, 612)  # tap claim reward 1280x720
        currentStep = 0  # finished
        finished += 1
        time.sleep(3)
        refreshLive()
        return True
    elif findImage(now, okIMG):
        touch(674, 609)  # Click in OK to accept quest 1280x720
        time.sleep(2)
        currentStep = 3  # start quest
        refreshLive()
        return True
    elif findImage(now, closeDialog):
        print("Tap in Fulfill request.")
        time.sleep(1)
        touch(930, 541)  # click in fulfill request 1280x720
        time.sleep(3)
        currentStep = 2
        refreshLive()
    elif countPixelsInPosition_NOW(494, 814, 50, 46, [101, 249, 249], 1, 2, now):
        print("Auto detect run")
        return runOrTeleport()
    elif findImage(now, claim):
        print("Claim reward")
        touch(641, 612)  # tap claim reward 1280x720
        time.sleep(1)
        currentStep = 0  # finished
        finished += 1
        refreshLive()
    elif findImage(now, start):
        touch(760, 612)  # Click in Start quest 1280x720
        currentStep = 4  # run quest
    elif walkScreen() == True:
        print("Tap in walk to start the quest")
        touch(371, 515)  # just touch in Start scroll quest
        time.sleep(2)  # wait to next screen
        refreshLive()
    elif detectIsDoing():  # Detect is running
        print("Autodetect is not running")
        # just touch in Start scroll quest
        touch(positions[position][0], positions[position][1])
        time.sleep(1)  # wait to next screen
        liveScreen()  # observar se da erro
        time.sleep(3)
    elif countPixelsInPosition_NOW(550, 0, 1280, 170, [0, 0, 0], 20000, 200000,now):
        skipDialog()
        currentStep = 5  # waiting quest
        return False


def walkScreen():
    # Screen to walk or teleport
    if countPixelsInPosition(495, 825, 10, 10, [233, 201, 131], 1, 10, True):
        return True

    return False


def detectIsDoing():
    global positionsCropIconDoing, position, positionsTexAvaiableQuest, now
    
    print("Position " + str(position))
    if countPixelsInPosition_NOW(550, 0, 1280, 170, [0, 0, 0], 20000, 200000,now):
        return False
    
    print("x : " + str(positionsTexAvaiableQuest[position][0]) + " Y : "+ str(positionsTexAvaiableQuest[position][1]))
    # avaiable sub quest 
    asq = countPixelsInPosition_NOW(positionsTexAvaiableQuest[position][0], positionsTexAvaiableQuest[position][1], 25, 10, [75,208,247], 1, 100, now, True)  # blue toon from text
    if asq and not walkScreen():
        return True
    
    #return False
   
    detectConquestIcon = countPixelsInPosition(positionsCropIconDoing[position][0], positionsCropIconDoing[position][1],
                                               positionsCropIconDoing[position][2], positionsCropIconDoing[position][3], [87, 208, 255], 1, 10)  # blue toon
    """detectConquestText = countPixelsInPosition(positionsTextIconDoing[position][0], positionsTextIconDoing[position][1],
                                               positionsTextIconDoing[position][2], positionsTextIconDoing[position][3], [141,176,255], 1, 100)  # blue toon from text
   """
    detectConquestText2= countPixelsInPosition(positionsText1IconDoing[position][0], positionsText1IconDoing[position][1],
                                               positionsText1IconDoing[position][2], positionsText1IconDoing[position][3], [255,174,0], 1, 100)  # blue toon from text
    if not countPixelsInPosition(550, 0, 1280, 170, [0, 0, 0], 20000, 200000):
        return True
    
    # Detect is running
    """if detectConquestText and not walkScreen():
        return False"""
    
    # Detect is running
    if detectConquestText2 and not walkScreen():
        return False
    # Detect is running
    if detectConquestIcon and not walkScreen():
        return False

    return True


def step01():
    global currentStep
    print("Checking Step 1")
    now = cv2.imread("now.png")
    if now is None:
        print("Eita poHa")
        time.sleep(15)  # skip to next thread execution
        return False

   # Recharge Auto=Progress Fulfill Request
    crop_img = now[431:461, 436:451]
    closeDialog = cv2.imread("Resources\step1.png")
    check = findImage(now, closeDialog)
    from .loginL2 import text  # extracted text
    if text.find('Recharge') > 0:
        print("STEP01 : Recharge[")
        tapFulfillRequest()
        print("]")
        currentStep = 2
        return True
    elif text.find('Auto=Progress') > 0:
        print("STEP01 : Auto=Progress[")
        tapFulfillRequest()
        print("]")
        currentStep = 2
        return True
    elif text.find("Fulfill Request") > 0:
        print("STEP01 : Fulfill Request[")
        tapFulfillRequest()
        print("]")
        currentStep = 2
        return True
    elif check:
        print("STEP01 : FOUND[")
        tapFulfillRequest()
        print("]")
        currentStep = 2
        return True
    elif text.find('ready fulfilled') > 0:
        touch(764, 483)  # Click in OK to accept quest 1280x720
        time.sleep(7)
        currentStep = 3  # start quest
        return True
    elif text.find('cannot be') > 0:
        touch(764, 483)  # Click in OK to accept quest 1280x720
        time.sleep(7)
        currentStep = 3  # start quest
        return True
    elif text.find('the quest?') > 0:
        touch(764, 483)  # Click in OK to accept quest 1280x720
        time.sleep(7)
        currentStep = 3  # start quest
        return True
    else:
        teleportPNG = cv2.imread("Resources\step_teleport.png")
        checkTeleport = findImage(now, teleportPNG)
        if checkTeleport:
            print("Tap in run")
            touch(495, 522)  # tap in run 1280x720
            time.sleep(2)
            currentStep = 4
        else:
            print("Unknow Step, checking again")
            currentStep = 2


def detectMainScreen():
    global now
    if checkExist_NOW(now, "Resources\pot.png"):  # todo check pot 100
        return True
    elif checkExist_NOW(now, "Resources\pot2.png"):  # todo check pot 100
        return True
    elif checkExist_NOW(now, "Resources\pot3.png"):  # offline mode
        return True
    elif checkExist_NOW(now, "Resources\pot4.png"):  # offline mode
        return True
    elif checkExist_NOW(now, "Resources\pot5.png"):  # offline mode
        return True
    elif checkExist_NOW(now, "Resources\pot6.png"):  # offline mode
        return True


def tapFulfillRequest():
    global currentStep, lastStep
    print("Tap in Fulfill request")
    time.sleep(1)
    touch(930, 541)  # click in fulfill request 1280x720
    time.sleep(3)
    if lastStep != 5:
        currentStep = 2


def skipDialog():
    global currentStep
    print("Skip dialog")
    touch(640, 470)    # touch in OK
    time.sleep(1)
    touch(1195, 522)  # click in skip 1280x720
    time.sleep(1)
    touch(1195, 522)  # click in skip 1280x720
    time.sleep(4)
    refreshLive()
    # currentStep = 5  # waiting quest
    return True


def runOrTeleport():
    global currentStep
    from .loginL2 import text  # extracted text
    if text.find('recommend using a Portal') > 0:
        print("Tap in teleport")
        touch(663, 530)  # tap in teleport 1280x720
    elif text.find('another territory') > 0:
        print("Tap in teleport")
        touch(663, 530)  # tap in teleport 1280x720
    elif text.find('distance away') > 0:
        print("Tap in teleport")
        touch(663, 530)  # tap in teleport 1280x720
    else:
        print("Tap in run")
        touch(495, 522)  # tap in run 1280x720

    time.sleep(2)
    currentStep = 5  # doing


def step02():
    global finished, currentStep, now
    if now is None:
        time.sleep(5)  # skip to next thread execution
        return False
    okIMG = cv2.imread("Resources\ok.png")
    if countPixelsInPosition_NOW(450, 645, 240, 60, [49, 77, 107], 450, 600,now):
        print("Touch in OK 0")
        touch(764, 483)  # Click in OK to accept quest 1280x720
        time.sleep(4)
        refreshLive()
        currentStep = 3  # start quest
        return True
    elif findImage(now, okIMG):
        print("Touch in OK 4")
        touch(674, 609)  # Click in OK to accept quest 1280x720
        time.sleep(4)
        refreshLive()
        currentStep = 3  # start quest
        return True


def step03():
    global currentStep
    now = cv2.imread("now.png")
    if now is None:
        print("Eita poHa step2")
        time.sleep(15)  # skip to next thread execution
        return False
    start = cv2.imread("Resources\start.png")
    checkStart = findImage(now, start)
    from .loginL2 import text  # extracted text
    if text.find('Grade S :') > 0:
        return startQuest()
    elif text.find('Grade A :') > 0:
        return startQuest()
    elif checkStart:
        return startQuest()


def startQuest():
    global currentStep
    touch(760, 612)  # Click in Start quest 1280x720
    time.sleep(7)
    currentStep = 4  # run quest
    return True


def step04():
    global currentStep
    from .loginL2 import now  # extracted text
    if now is None:
        time.sleep(5)  # skip to next thread execution
        return False

    # checkTeleport:
    if countPixelsInPosition(494, 814, 50, 46, [101, 249, 249], 1, 2):
        print("Tap in run")
        touch(495, 522)  # tap in run 1280x720
        time.sleep(2)
        currentStep = 5  # doing
    else:
        print("Unknow Step, checking again")
        currentStep = 4


def step05():
    global currentStep, finished
    from .loginL2 import now  # extracted text
    from .loginL2 import text  # extracted text
    if now is None:
        print("Eita poHa step2")
        time.sleep(10)  # skip to next thread execution
        return False
    claim = cv2.imread("Resources\claim.png")
    if countPixelsInPosition(581, 379, 500, 60, [49, 77, 107], 850, 1500, True):
        print("Claim reward 0.")
        touch(641, 612)  # tap claim reward 1280x720
        currentStep = 0  # finished
        finished += 1
        time.sleep(5)
        return True
    elif findImage(now, claim):
        print("Claim reward")
        touch(641, 612)  # tap claim reward 1280x720
        currentStep = 0  # finished
        finished += 1
    elif text.find('Cearance') > 0:
        print("Claim reward")
        touch(641, 612)  # tap claim reward 1280x720
        currentStep = 0  # finished
        finished += 1
    elif countPixelsInPosition(550, 0, 1280, 170, [0, 0, 0], 20000, 200000):
        skipDialog()
        currentStep = 5  # waiting quest
        return False


def detectImClanHall():
    from .loginL2 import now  # extracted text
    if now is None:
        time.sleep(5)  # skip to next thread execution
        return False

    from .loginL2 import text  # extracted text
    if text.find('Clan Hall') > 0:
        touch(930, 88)
        time.sleep(10)  # leave from clan hall
        return True
    elif text.find('clan Hall') > 0:
        touch(930, 88)
        time.sleep(10)  # leave from clan hall
        return True
    elif text.find('hall') > 0:
        touch(930, 88)
        time.sleep(10)  # leave from clan hall
        return True

    return False


def refreshLive():
    global now, Try
    liveScreen()
    if os.path.isfile('./now.png') == True:
        now = cv2.imread("now.png")
        if now is None:
            Try += 1
            print("Current Screen not found #"+str(Try))
            time.sleep(3)  # skip to next thread execution
            if Try >= 15:
                Try = 0
                logged = 0
                restartL2()
            return False
        size = os.path.getsize("./now.png")
        if size < 200:
            print("problem with current screen : " + str(size))

        assert not isinstance(now, type(None)), 'image not found'
        return True
    return False