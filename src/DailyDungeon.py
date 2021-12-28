from .Utils import liveScreen, touch,swipe, extractText, extractTextFromResize
from .Utils import findImage
import cv2
import threading
import time
from .Utils import restart
from datetime import date, timedelta, datetime
import numpy as np
from .loginL2 import checkExist

DailyDungeonIsDone = 1
finished = 0
currentStep = 0  
inExecution = 0
lastStep = 0
# BUGS/IMPROVEMENTS
# 1. SO resta testar se da algum problema
# 2. verificar se tem scroll ao iniciar
# 3. melhorar teleport qndo for em outro territorio
# 4. Ainda da pra deixa mais rapido
# 5. Puxar a informacao de um txt evita qndo desligar e ligar o bot fazer tudo de novo


def loopDailyDungeon():
    # restart()
    threading.Timer(6.0, loopDailyDungeon).start()
    doDailyDungeon()


def doDailyDungeon():
    global finished
    global currentStep
    global inExecution
    global DailyDungeonIsDone
    from .loginL2 import logged
    from .loginL2 import text  # extracted text
    if logged == 0:
        return False
    
    if DailyDungeonIsDone == 1:
        return False
    
    # print(text)

    if inExecution == 0:
        print("Daily Quest")
        now = datetime.now()
        inExecution = 1
        checkStep()
        inExecution = 0

# change step 1-3 to close dialogs and step 4 is final quest


def checkStep():
    global currentStep
    print("Daily DUngeon : Checking Steps")  # verificar qual passo esta baseado em prints
    if currentStep == 0:  # Main screen
        print("Step 0")
        step00()
    elif currentStep == 1:  # Touch Dungeon
        print("Step 1")
        step01()
    elif currentStep == 2:  # Touch in Daily Dungeon ir swipe to start
        print("Step 2")
        step02()
    elif currentStep == 3:  # Check current screen is Daily Dungeon
        print("Step 3")
        step03()
    elif currentStep == 4:  # Check already completed
        print("Step 4")
        step04()
    elif currentStep == 5:  # Touch in enter
        print("Step 5")
        step05()


def step00():
    global currentStep
    touch(923, 30)  # touch(235, 400)
    from .loginL2 import text  # extracted text
    if text.find('Dungeon'):
        touch(300, 659) # touch in dungeon
        time.sleep(1)
        liveScreen()
        time.sleep(3)
        currentStep = 1


def step01():
    global currentStep
    from .loginL2 import text  # extracted text
    if text.find('Normal Dungeon'):
        currentStep = 2  # run to NPC
        touch(120, 515) # touch in Normal Dungeon
        time.sleep(3)
        liveScreen()
        time.sleep(4)
    elif text.find('Temporal Rift'):
        currentStep = 2  # run to NPC
        touch(120, 515) # touch in Normal Dungeon
        time.sleep(3)
        liveScreen()
        time.sleep(4)

def step02():
    global currentStep
    from .loginL2 import text  # extracted text
    
    if detectAreInStart():
        touch(171, 345)  # touch in Daily Dungeon  
        time.sleep(4)
        currentStep = 3  # ready to touch in Daily Dungeon
        return False
    else:
        print("Swiping to start")
        swipe(40, 420, 800, 420, 0.5)  # Swiping to start
        time.sleep(3)
        liveScreen()
        time.sleep(3)

def step03():
    global currentStep
    liveScreen()
    time.sleep(4)
    text = extractText()
    #from .loginL2 import text  # extracted text
    print("TEXT DAILY ")
    print(text)
    if text.find('Very Easy') > 0 :
        currentStep = 4
        return True
    elif text.find('Hell') > 0 :
        currentStep = 4
        return True
    elif text.find('Heroic') > 0 :
        currentStep = 4
        return True
    elif text.find('Legendary') > 0 :
        currentStep = 4
        return True
    elif text.find('Mythic') > 0 :
        currentStep = 4
        return True
    elif text.find('Elite Points') > 0 : # wrong screen
        touch(39,40) # back to prev screen
        currentStep = 2 # set current step like last step
        time.sleep(5)
        return True
    else:
        detectImMainScreen()
        return False
  

def step04():
    global currentStep, DailyDungeonIsDone
    from .loginL2 import text  # extracted text
    if text.find('Available Completions: 1/1') > 0 :
        currentStep = 5
        return True
    elif text.find('1/1') > 0 :
        currentStep = 5
        return True
    elif text.find('Available Completions: 0/1') > 0 :
        currentStep = 0
        DailyDungeonIsDone = 1
        touch(1243,39) # back to main screen
        time.sleep(15)
        return True
    elif text.find('0/1') > 0 :
        currentStep = 0
        DailyDungeonIsDone = 1
        touch(1243,39) # back to main screen
        time.sleep(15)
        return True
    else: # Already completed
        currentStep = 0
        DailyDungeonIsDone = 1
        touch(1243,39) # back to main screen
        time.sleep(15)
        return False
    
def step05():
    global currentStep, DailyDungeonIsDone
    from .loginL2 import text  # extracted text
    touch(1146,512) # touch Free Auto-Clear start 
    time.sleep(3)
    touch(1134,590) # touch in Free Auto-Clear
    time.sleep(5)
    touch(1134,590) # close prize reward
    time.sleep(3)
    touch(1243,39) # back to main screen
    time.sleep(3)
    currentStep = 0
    DailyDungeonIsDone = 1
  
def markLikeDone():
    global currentStep, DailyDungeonIsDone
    DailyDungeonIsDone = 1
    currentStep = 0
    touch(1025,668) # touch in OK
    time.sleep(25)
    touch(1243,39) # back to main screen
    time.sleep(5)

def detectAreInStart():
    from .loginL2 import now  # extracted text
    if now is None:
        time.sleep(7)  # skip to next thread execution
        return 0
    
    text = extractTextFromResize(165,40,257,420)
    print("TEXT FROM RESZIZE : ")
    print(text)
    if text.find("Daily Dungeon") > 0 :
        return True
    elif text.find("strengthening every day") > 0:
        return True
    else:
        return False
    
    
def detectImMainScreen():
    global currentStep
    if currentStep == 0:
        return False
    
    if currentStep == 5:
        return False
    
    from .loginL2 import now  # extracted text
    if now is None:
        time.sleep(7)  # skip to next thread execution
        return 0
    elif checkExist("Resources\pot.png"):
        currentStep = 0
        return False
    elif checkExist("Resources\pot2.png"):
        currentStep = 0
        return False
    elif checkExist('Resources\clock.png'):  # reward recess point
        currentStep = 0
        return False
    elif checkExist("Resources\pot3.png"):  # offline mode
        currentStep = 0
        return False
    elif checkExist("Resources\pot4.png"):  # offline mode
        currentStep = 0
        return False
    elif checkExist("Resources\pot5.png"):  # offline mode
        currentStep = 0
        return False
    elif checkExist("Resources\pot6.png"):  # offline mode
        currentStep = 0
        return False
    return True