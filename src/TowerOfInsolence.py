from .Utils import liveScreen, touch,swipe, extractText, extractTextFromResize
from .Utils import findImage
import cv2
import threading
import time
from .Utils import restart
from datetime import date, timedelta, datetime
import numpy as np
from .loginL2 import checkExist

TowerOfInsolenceIsDone = 1
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


def loopTowerOfInsolence():
    # restart()
    threading.Timer(6.0, loopTowerOfInsolence).start()
    doTowerOfInsolence()


def doTowerOfInsolence():
    global finished, currentStep, inExecution, TowerOfInsolenceIsDone
    from .loginL2 import logged
    from .loginL2 import text  # extracted text
    from .DailyDungeon import DailyDungeonIsDone
    
    if logged == 0:
        return False
    
    if DailyDungeonIsDone == 0:
        return False
    
    if TowerOfInsolenceIsDone == 1:
        return False
    
    if inExecution == 0:
        print("Tower Of Insolence")
        inExecution = 1
        checkStep()
        inExecution = 0

# change step 1-3 to close dialogs and step 4 is final quest


def checkStep():
    global currentStep
    print("Tower Of Insolence : Checking Steps")  # verificar qual passo esta baseado em prints
    if currentStep == 0:  # Main screen
        print("Step 0")
        step00()
    elif currentStep == 1:  # Touch Dungeon
        print("Step 1")
        step01()
    elif currentStep == 2:  # Touch in Tower Of Insolence or swipe to start
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
    detectImMainScreen()
        
def step02():
    global currentStep
    from .loginL2 import text  # extracted text
    
    if detectAreInStart():
        touch(436, 335)  # touch in Tower Of Insolence
        currentStep = 3  # ready to touch in Daily Dungeon
        return False
    elif text.find('Elite Points') > 0 : # wrong screen
        touch(39,40) # back to prev screen
        currentStep = 2 # set current step like last step
        time.sleep(5)
        return True
    elif text.find('Required Level') > 0:
        touch(39,40) # back to prev screen
        currentStep = 2 # set current step like last step
        time.sleep(5)
        return True
    else:
        print("Swiping to start")
        swipe(40, 420, 800, 420, 0.5)  # Swiping to start
        time.sleep(2)
        liveScreen()
        time.sleep(2)
        detectImMainScreen()

def step03():
    global currentStep,now
    liveScreen()
    time.sleep(4)
    text = extractText(now)
    #from .loginL2 import text  # extracted text
    print("TEXT Tower Of Insolence ")
    print(text)
    if text.find('Tower of Insolence') > 0 :
        currentStep = 4
        return True
    elif text.find('Immeasurable') > 0 :
        currentStep = 4
        return True
    elif text.find('Floors') > 0 :
        currentStep = 4
        return True
    elif text.find('Auto-Clear is only valid for one day for rewards for all cleared') > 0 :
        currentStep = 4
        return True
    elif text.find('Elite Points') > 0 : # wrong screen
        touch(39,40) # back to prev screen
        currentStep = 2 # set current step like last step
        time.sleep(5)
        return True
    elif text.find('Required Level') > 0:
        touch(39,40) # back to prev screen
        currentStep = 2 # set current step like last step
        time.sleep(5)
        return True
    else:
        detectImMainScreen()
        return False
  

def step04():
    global currentStep, TowerOfInsolenceIsDone
    from .loginL2 import text  # extracted text
    textResize = extractTextFromResize(642,650,300,80)
    print("CURRENT TEXT")
    print(text)
    if text.find('You have claimed today’s Auto-Clear reward.') > 0:
        currentStep = 0
        TowerOfInsolenceIsDone = 1
        touch(1243,39) # back to main screen
        time.sleep(15)
        return False
    elif text.find('You have claimed today') > 0:
        currentStep = 0
        TowerOfInsolenceIsDone = 1
        touch(1243,39) # back to main screen
        time.sleep(15)
        return False
    elif textResize.find('Auto-Clear') > 0 :
        currentStep = 5
        return True
    elif textResize.find('Clear') > 0 :
        currentStep = 5
        return True
    elif textResize.find('Reward') > 0 :
        currentStep = 0
        TowerOfInsolenceIsDone = 1
        touch(1243,39) # back to main screen
        time.sleep(15)
        return True
    else: # Already completed
        currentStep = 0
        TowerOfInsolenceIsDone = 1
        touch(1243,39) # back to main screen
        time.sleep(15)
        return False
    
def step05():
    global currentStep, TowerOfInsolenceIsDone
    from .loginL2 import text  # extracted text
    touch(800,675) # touch Free Auto-Clear start 
    time.sleep(7)
    touch(944,660) # touch Free Auto-Clear start 
    time.sleep(2)
    touch(1243,39) # back to main screen
    time.sleep(3)
    currentStep = 0
    TowerOfInsolenceIsDone = 1
  
def markLikeDone():
    global currentStep, TowerOfInsolenceIsDone
    TowerOfInsolenceIsDone = 1
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