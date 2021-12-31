from .Utils import liveScreen, touch, extractText, extractTextFromResize, countPixelsInPosition
from .Utils import findImage

import cv2
import threading
import time
from .Utils import restart
from datetime import date, timedelta, datetime
import numpy as np
from .loginL2 import checkStopService, checkExist
positionsCrop = [[277,9,220,50],[382,9,130,20],[348,244,5,5 ]] 
positions = [[112,326],[119, 394],[110, 225]] # position to click in scroll quest, 0 is seconds position and 1 is third, 2 is first position
position = 2 # current position
scrollQuestIsDone = 1
finished = 0
currentStep = 0  # step 0 = no runinng scroll, 1 = Select Scroll, 2 = Confirm Scroll, 3 = Start Scroll, 4 = walk, 5 = Doing, 6 = Claim
inExecution = 0
lastStep = 0
thread = False
# BUGS/IMPROVEMENTS
# 0. Verificar a posicao do click em scroll quest
# 1. SO resta testar se da algum problema
# 2. verificar se tem scroll ao iniciar
# 3. melhorar teleport qndo for em outro territorio
# 4. Ainda da pra deixa mais rapido
# 5. Puxar a informacao de um txt evita qndo desligar e ligar o bot fazer tudo de novo


def loopScrollQuest():
    # restart()
    global thread
    # maybe this can get a great performace
    if thread != False and thread.isAlive():
        thread.cancel()
        thread = False # clear RAM cache
        
    thread = threading.Timer(6.0, loopScrollQuest)
    thread.start()
    doScrollQuest()


def doScrollQuest():
    global finished, currentStep, inExecution, scrollQuestIsDone, thread
    from .loginL2 import logged
    from .loginL2 import text  # extracted text
    from .DailyDungeon import DailyDungeonIsDone
    from .TempleGuardian import finishedTempleGuardian
    from .TowerOfInsolence import TowerOfInsolenceIsDone
    from .EliteQuest import EliteQuestIsDone
    
    if logged == 0 or EliteQuestIsDone == 0 or TowerOfInsolenceIsDone == 0 or DailyDungeonIsDone == 0 or finishedTempleGuardian == 0 or scrollQuestIsDone == 1:
        return False
    
    if inExecution == 0:
        print("Daily Quest")
        # liveScreen()
        now = datetime.now()
        print(str(now.strftime("%H:%M:%S")))
        inExecution = 1
        checkMainTab()
        checkMapisOpened()
        checkStopService()
        checkDie()
        checkStep()
        inExecution = 0
    else:
        print("In Execution")   
        time.sleep(4) 

def checkMapisOpened():
    if checkExist("Resources\openmap.png") :
        touch(1244,40)
        return True
    return False

def checkMainTab():
    if countPixelsInPosition(164,69,50,2,[75, 154, 255], 50, 60):
        print("swith to main tab")
        touch(30,180)
        return True
    return False

def checkStep():
    global currentStep
    global lastStep
    lastStep = currentStep
    print("Cheking Steps")  # verificar qual passo esta baseado em prints
    checkCompleted()
    detectCurrentStep()


def checkCompleted():
    global finished, scrollQuestIsDone, currentStep
    from .loginL2 import text  # extracted text
    if text.find('Complete Count 10/10') > 0:
        finished = 10
        currentStep = 1
        scrollQuestIsDone = 1
        touch(1014, 173)
        return True
    elif text.find('Count 10/10') > 0:
        finished = 10
        currentStep = 1
        scrollQuestIsDone = 1
        touch(1014, 173)
        return True
    elif text.find('Count Recharge') > 0:
        finished = 10
        currentStep = 1
        scrollQuestIsDone = 1
        return True
    # crop Recharge button and check color
    elif countPixelsInPosition(505,423,205,60,[40,133,193], 30, 100) :
        return setLikeDone()
    elif countPixelsInPosition(505,423,205,60,[41, 90, 131], 150, 200) :
        return setLikeDone()
    elif countPixelsInPosition(505,423,205,60,[31, 87, 133], 35, 80) :
        return setLikeDone()
    elif countPixelsInPosition(297,226,35,30,[189,121,88], 4, 20) :
        return setLikeDone(False)
    # crop Recharge button and check color
    elif countPixelsInPosition(505,423,205,60,[29,40,57], 700, 1000) :
        step01()
        return True
    #elif text.find('Recharge') > 0 and currentStep == 1:
    #    print("Sub-Quest Done..")
    #    finished = 10
    #    currentStep = 1
    #    scrollQuestIsDone = 1
    #    touch(1014, 173)
    #    return True


def setLikeDone(close=True):
    global finished, currentStep, scrollQuestIsDone
    print("Scroll quests is done")
    if close :
        touch(1014, 172)  # touch in close
    time.sleep(2)
    finished = 10
    currentStep = 1
    scrollQuestIsDone = 1
    return True

def checkDie():
    from .loginL2 import now  # extracted text
    if now is None:
        time.sleep(5)  # skip to next thread execution
        return False
    die = cv2.imread("Resources\die.png")
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
    global currentStep, positions, position, finished,positionsCrop
    from .loginL2 import now, text  # extracted text
    if now is None:
        time.sleep(5)  # skip to next thread execution
        return False

    closeDialog = cv2.imread("Resources\step1.png")
    check = findImage(now, closeDialog)
    claim = cv2.imread("Resources\claim.png")
    checkClaim = findImage(now, claim)
    start = cv2.imread("Resources\start.png")
    checkStart = findImage(now, start)
    okIMG = cv2.imread("Resources\ok.png")
    monsterCard = cv2.imread("Resources\Screenshot_20211219-125109.png")
    checkOK = findImage(now, okIMG)
    from .loginL2 import text  # extracted text
    textFromSubQuest = extractTextFromResize(361, 2, 250, 80)
    #print("textFromSubQuest")
    #print(textFromSubQuest)
    """if text.find('Bonus Points') > 0 or text.find('Points Start') > 0:
        print("Leave from elite")
        touch(859, 86)  # Leave from elite
        time.sleep(4)
        touch(1239, 44)  # Back to main screen
        return False
    elif text.find('Elite Points') > 0:
        print("Leave from elite")
        touch(859, 86)  # Leave from elite
        time.sleep(4)
        touch(1239, 44)  # Back to main screen
        return False
    el"""
    if countPixelsInPosition(450,645,240,60,[49,77,107], 450, 600) :
        print("Touch in OK 0")
        touch(764, 483)  # Click in OK to accept quest 1280x720
        time.sleep(5)
        currentStep = 3  # start quest
        return True  
    elif findImage(now, monsterCard) :
        print("Close Dialog and start Quest")
        touch(788, 488)  # Tap in close moster card dialog
        time.sleep(1)
        touch(670, 610)  # Tap in Start Quest
        time.sleep(4)
        touch(492, 518)  # Tap in walk
        time.sleep(4)
        currentStep = 3  # start quest
        return True  
    elif text.find('Grade S :') > 0:
        return startQuest()
    elif text.find('Grade A :') > 0:
        return startQuest()
    elif text.find('Clear Reward') > 0:
        return startQuest()
    elif text.find('already fulfilled') > 0:
        touch(764, 483)  # Click in OK to accept quest 1280x720
        time.sleep(2)
        currentStep = 3  # start quest
        return True
    elif text.find('Proceed with the quest') > 0:
        touch(764, 483)  # Click in OK to accept quest 1280x720
        time.sleep(2)
        currentStep = 3  # start quest
        return True
    elif text.find('cannot be') > 0:
        touch(764, 483)  # Click in OK to accept quest 1280x720
        time.sleep(2)
        currentStep = 3  # start quest
        return True
    elif text.find('You need a Scroll') > 0:
        return runOrTeleport()
    elif text.find('order to teleport') > 0:
        return runOrTeleport()
    elif countPixelsInPosition(581,379,500,60,[49,77,107], 850, 1500):
        print("Claim reward 0")
        touch(641, 612)  # tap claim reward 1280x720
        currentStep = 0  # finished
        finished += 1
        time.sleep(5)
        return True
    elif text.find('Cearance') > 0:
        print("Claim reward !")
        touch(641, 612)  # tap claim reward 1280x720
        time.sleep(1)
        currentStep = 0  # finished
        finished += 1
        return True
    elif checkOK:
        touch(674, 609)  # Click in OK to accept quest 1280x720
        time.sleep(2)
        currentStep = 3  # start quest
        return True
    elif check:
        print("Tap in Fulfill request.")
        time.sleep(1)
        touch(930, 541)  # click in fulfill request 1280x720
        time.sleep(5)
        currentStep = 2
    elif countPixelsInPosition(494,814,50,46,[101, 249, 249], 1, 2) :   
        print("Auto detect run")
        return runOrTeleport()
    elif checkClaim:
        print("Claim reward")
        touch(641, 612)  # tap claim reward 1280x720
        time.sleep(1)
        currentStep = 0  # finished
        finished += 1
    elif checkStart:
        touch(760, 612)  # Click in Start quest 1280x720
        currentStep = 4  # run quest
    elif checkOK:
        touch(758, 500)  # Click in OK to accept quest 1280x720
        time.sleep(2)
        currentStep = 3  # start quest
    elif text.find('Incorrect status') > 0:
        print("Closing Incorrect status")
        touch(640, 470)  # touch in OK
        currentStep = 5  # waiting quest
    elif textFromSubQuest.find('Available [Sub-quest]') > 0:
        print("Tap in sub quest.")
        touch(119, 394)  # just touch in Start scroll quest
        time.sleep(5)
        return False
    elif textFromSubQuest.find('[Sub-quest]') > 0 or textFromSubQuest.find('[Sub]') > 0 or textFromSubQuest.find('[Sub') > 0:
        print("Tap in sub quest")
        touch(positions[position][0], positions[position][1])
        time.sleep(5)
        return False
    elif textFromSubQuest.find('Go to Harkeiah’s Grave?') > 0 or textFromSubQuest.find('Go to Harkeiah') > 0:
        print("Tap in OK Harkeiah's Grave")
        touch(764, 472)  # just touch in Start scroll quest
        currentStep = 5  # waiting quest
        time.sleep(5)
        return False
    elif walkScreen() == True:
         print("Tap in walk to start the quest")
         touch(371, 515)  # just touch in Start scroll quest
         time.sleep(3)  # wait to next screen
    elif detectIsDoing() == False: # Detect is running
        print("Autodetect is not running")
        touch(positions[position][0], positions[position][1])  # just touch in Start scroll quest
        time.sleep(1)  # wait to next screen
        liveScreen() # observar se da erro
        time.sleep(3)
        newText = extractText()
        if newText.find('You need a Scroll') > 0:
            return runOrTeleport()
        elif newText.find('order to teleport') > 0:
            return runOrTeleport()
        else:
            return False
    elif countPixelsInPosition(550,0,1280,170,[0,0,0], 20000, 200000):
        skipDialog()
        currentStep = 5  # waiting quest
        return False


def walkScreen():
    if countPixelsInPosition(495,825,10,10,[233, 201, 131], 1, 10, True): # Screen to walk or teleport
        return True;
    
    return False;

def detectIsDoing():
    if countPixelsInPosition(348,244,5,5,[87, 208, 255], 1, 10, True) and walkScreen() == False and countPixelsInPosition(550,0,1280,170,[0,0,0], 20000, 200000) == False: # Detect is running
        return False;
    
    if countPixelsInPosition(318,244,5,5,[87, 208, 255], 1, 10,True) and walkScreen() == False and countPixelsInPosition(550,0,1280,170,[0,0,0], 20000, 200000) == False: # Detect is running
        return False;
    
    return True;


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
    global finished, currentStep
    from .loginL2 import now  # extracted text
    if now is None:
        time.sleep(5)  # skip to next thread execution
        return False
    okIMG = cv2.imread("Resources\ok.png")
    from .loginL2 import text  # extracted text
    if countPixelsInPosition(450,645,240,60,[49,77,107], 450, 600) :
        print("Touch in OK 0")
        touch(764, 483)  # Click in OK to accept quest 1280x720
        time.sleep(6)
        currentStep = 3  # start quest
        return True
    elif text.find('already fulfilled') > 0:
        print("Touch in OK 1")
        touch(764, 483)  # Click in OK to accept quest 1280x720
        time.sleep(6)
        currentStep = 3  # start quest
    elif text.find('with the quest?') > 0:
        print("Touch in OK 2")
        touch(764, 483)  # Click in OK to accept quest 1280x720
        time.sleep(6)
        currentStep = 3  # start quest
        return True
    elif text.find('cannot be') > 0:
        print("Touch in OK 3")
        touch(764, 483)  # Click in OK to accept quest 1280x720
        time.sleep(6)
        currentStep = 3  # start quest
        return True
    elif findImage(now, okIMG):
        print("Touch in OK 4")
        touch(674, 609)  # Click in OK to accept quest 1280x720
        time.sleep(6)
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

    #teleportPNG = cv2.imread("Resources\step_teleport.png")
    #checkTeleport = findImage(now, teleportPNG)
    if countPixelsInPosition(494,814,50,46,[101, 249, 249], 1, 2) : #checkTeleport:
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
    if countPixelsInPosition(581,379,500,60,[49,77,107], 850, 1500, True):
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
    elif countPixelsInPosition(550,0,1280,170,[0,0,0], 20000, 200000):
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
