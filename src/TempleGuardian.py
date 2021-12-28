from .Utils import extractText, extractTextFromResize, liveScreen, touch, countPixelsInPosition
from .Utils import swipe
from .Utils import findImage
from .loginL2 import checkExist
import cv2
import threading
import time
import pytesseract
# working
finishedTempleGuardian = 1
currentStepTempleGuardian = 0 # done this
inExecution = 0
thread = False

def loopTempleGuardian():
    global thread
    # olha isso douglas
    if thread != False and thread.isAlive():
        thread.cancel()
        
    thread = threading.Timer(8.0, loopTempleGuardian)
    thread.start()
    doTempleGuardian()


def doTempleGuardian():
    global inExecution, currentStepTempleGuardian, finishedTempleGuardian
    from .DailyDungeon import DailyDungeonIsDone
    from .TowerOfInsolence import TowerOfInsolenceIsDone
    from .SummoningCircle import finishedSummoningCircle
    
    from .loginL2 import logged
    if logged == 0:
        return False

    if finishedTempleGuardian == 1:
        return False

    if DailyDungeonIsDone == 0:
        return False

    if TowerOfInsolenceIsDone == 0:
        return False
    
    if finishedSummoningCircle == 0:
        return False
    
    elif inExecution == 0:
        inExecution = 1
        checkStep()
        inExecution = 0


def checkStep():
    global currentStepTempleGuardian
    # verificar qual passo esta baseado em prints
    print("Temple Guardian : Checking Steps")
    if currentStepTempleGuardian == 0:  # Main screen
        print("Step 0")
        step00()
    elif currentStepTempleGuardian == 1:  # Touch Dungeon
        print("Step 1")
        step01()
    elif currentStepTempleGuardian == 2:  # Touch in Normal Dungeon
        print("Step 2")
        step02()
    elif currentStepTempleGuardian == 3:  # Check current screen is temple guardian
        print("Step 3")
        step03()
    elif currentStepTempleGuardian == 4:  # Check already completed
        print("Step 4")
        step04()
    elif currentStepTempleGuardian == 5:  # Touch in enter
        print("Step 5")
        step05()
    elif currentStepTempleGuardian == 6:  # Wait to done
        print("Step 6")
        step06()


def step00():
    global currentStepTempleGuardian
    touch(923, 30)  # touch(235, 400)
    from .loginL2 import text  # extracted text
    if text.find('Dungeon'):
        touch(300, 659)  # touch in dungeon
        time.sleep(1)
        liveScreen()
        time.sleep(2)
        currentStepTempleGuardian = 1  # run to NPC


def step01():
    global currentStepTempleGuardian
    from .loginL2 import text  # extracted text
    if text.find('Normal Dungeon'):
        currentStepTempleGuardian = 2  # run to NPC
        touch(120, 515)  # touch in Normal Dungeon
        time.sleep(1)
        liveScreen()
        time.sleep(2)
    elif text.find('Temporal Rift'):
        currentStepTempleGuardian = 2  # run to NPC
        touch(120, 515)  # touch in Normal Dungeon
        time.sleep(1)
        liveScreen()
        time.sleep(2)


def step02():
    global currentStepTempleGuardian
    from .loginL2 import text  # extracted text

    if detectAreInStart():
        touch(1200, 377)  # touch in dungeon
        currentStepTempleGuardian = 3  # ready to touch in Temple Guardian
        # time.sleep(2)
        # liveScreen()
        # time.sleep(2)
        return False
    # elif text.find("Dungeon Quest"):
       # print("WRONG STEP")
        # touch(38,38) # touch in back
        # time.sleep(3)
    #    return False
    # elif text.find("Elite Points"):
    #    print("WRONG STEP")
    #    touch(38,38) # touch in back
    #    time.sleep(3)
    #    return False
    else:
        print("Swiping to start")
        swipe(40, 420, 800, 420, 0.5)  # swipe a little bit to down
        time.sleep(2)
        liveScreen()
        time.sleep(2)


def step03():
    global currentStepTempleGuardian
    liveScreen()
    time.sleep(4)
    text = extractText()
    # from .loginL2 import text  # extracted text
    if text.find('Temple Guardian') > 0:
        currentStepTempleGuardian = 4
        return True
    elif text.find('Very Easy') > 0:
        currentStepTempleGuardian = 4
        return True
    elif text.find('Required Level') > 0:
        currentStepTempleGuardian = 4
        return True
    elif text.find('Legendary') > 0:
        currentStepTempleGuardian = 4
        return True
    elif text.find('Mythic') > 0:
        currentStepTempleGuardian = 4
        return True
    else:
        return False


def step04():
    global currentStepTempleGuardian, finishedTempleGuardian
    from .loginL2 import text  # extracted text

    if countPixelsInPosition(609, 922, 320, 70, [49, 101, 70], 200, 1000):
        currentStepTempleGuardian = 5
        return True
    elif text.find('Available Entry Counts: 1/1') > 0:
        currentStepTempleGuardian = 5
        return True
    elif text.find('1/1') > 0:
        currentStepTempleGuardian = 5
        return True
    elif text.find('0/1') > 0:
        currentStepTempleGuardian = 0
        finishedTempleGuardian = 1
        touch(1243, 39)  # back to main screen
        time.sleep(15)
        return True
    else:  # Already completed
        currentStepTempleGuardian = 0
        finishedTempleGuardian = 1
        touch(1243, 39)  # back to main screen
        time.sleep(15)
        return False


def step06():
    global currentStepTempleGuardian, finishedTempleGuardian
    from .loginL2 import text  # extracted text
    if text.find('Dungeon Cleared') > 0:
        markLikeDone()
        return True
    elif(text.find('Temple Guardian Reward Box') > 0):
        markLikeDone()
        return True
    elif(text.find('Acquired Items') > 0):
        markLikeDone()
        return True
    elif(text.find('See Details') > 0):
        markLikeDone()
        return True
    else:
        return False


def step05():
    global currentStepTempleGuardian, finishedTempleGuardian
    from .loginL2 import text  # extracted text
    touch(320, 430)  # select Mythic
    time.sleep(2)
    touch(1082, 643)  # touch in start
    time.sleep(5)
    touch(767, 483)  # touch in auto-join
    time.sleep(3)
    touch(1102, 84)  # touch in close auto-join status
    time.sleep(3)
    touch(1243, 39)  # back to main screen
    currentStepTempleGuardian = 6


def markLikeDone():
    global currentStepTempleGuardian, finishedTempleGuardian
    finishedTempleGuardian = 1
    currentStepTempleGuardian = 0
    touch(1025, 668)  # touch in OK
    time.sleep(25)
    touch(1243, 39)  # back to main screen
    time.sleep(5)


def detectAreInStart():
    from .loginL2 import now  # extracted text
    if now is None:
        time.sleep(7)  # skip to next thread execution
        return 0

    text = extractTextFromResize(165, 40, 257, 420)
    print("TEXT FROM RESZIZE : ")
    print(text)
    if text.find("Daily Dungeon") > 0:
        return True
    elif text.find("strengthening every day") > 0:
        return True
    else:
        return False


def detectImMainScreen():
    global currentStepTempleGuardian
    if currentStepTempleGuardian == 0:
        return False

    if currentStepTempleGuardian == 5:
        return False

    from .loginL2 import now  # extracted text
    if now is None:
        time.sleep(7)  # skip to next thread execution
        return 0
    elif checkExist("Resources\pot.png"):
        currentStepTempleGuardian = 0
        return False
    elif checkExist("Resources\pot2.png"):
        currentStepTempleGuardian = 0
        return False
    elif checkExist('Resources\clock.png'):  # reward recess point
        currentStepTempleGuardian = 0
        return False
    elif checkExist("Resources\pot3.png"):  # offline mode
        currentStepTempleGuardian = 0
        return False
    elif checkExist("Resources\pot4.png"):  # offline mode
        currentStepTempleGuardian = 0
        return False
    elif checkExist("Resources\pot5.png"):  # offline mode
        currentStepTempleGuardian = 0
        return False
    elif checkExist("Resources\pot6.png"):  # offline mode
        currentStepTempleGuardian = 0
        return False
    return True
