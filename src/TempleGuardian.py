from .Utils import extractText, countPixelsInPosition_NOW, findImageByPosition, extractTextFromResize, liveScreen, touch
from .Utils import swipe, restartL2
from .Utils import findImage
import cv2
import threading
import time
import pytesseract
import os
import numpy as np
Try = 0
alreadyDone = cv2.imread("Resources\Screenshot_20220101-172942.png")
die = cv2.imread("Resources\die.png")
limitBreak = cv2.imread("Resources\Screenshot_20220101-161653.png")
dungeon1 = cv2.imread("Resources\Screenshot_20220101-155243.png")
closeDialog = cv2.imread("Resources\Screenshot_20220101-183441.png")
summoningCircle2 = cv2.imread("Resources\summoningCircleText.png")
templeGuardianResource = cv2.imread("Resources\TempleGuardianResource1.png")
dungeon = cv2.imread("Resources\Screenshot_20220101-143001.png")
dungeon2 = cv2.imread("Resources\Screenshot_20220101-150154.png")
invalid1Resource = cv2.imread("Resources\Screenshot_20220307-135104.png")
invalid2Resource = cv2.imread("Resources\Screenshot_20220306-142327.png")
# working
finishedTempleGuardian = 0
currentStepTempleGuardian = 0 # done this
inExecution = 0
thread = False
jumps = 1
jumpsC = 0
now = False

def loopTempleGuardian():
    global thread, jumpsC, jumps
    # olha isso douglas
    if thread != False and thread.isAlive():
        thread.join()   
        
    thread = threading.Timer(8.0, doTempleGuardian)
    thread.daemon = True # stop if the program exits
    thread.setName("Temple Guardian Thread")
    thread.start()


def doTempleGuardian():
    global inExecution, Try, now, currentStepTempleGuardian, finishedTempleGuardian
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
    
    liveScreen()
    if os.path.isfile('now.png') == True:
        now = cv2.imread("now.png")
        if now is None:
            Try+= 1
            print("Current Screen not found #"+str(Try))
            time.sleep(3) # skip to next thread execution
            if Try >= 15 : 
                Try = 0
                logged = 0
                restartL2()
            return False
        size = os.path.getsize("now.png")
        print("Size : " + str(size))
        if size < 200:
            print("problem with current screen : " + str(size))
            
        assert not isinstance(now, type(None)), 'image not found'
        Try = 0
        checkStep()


def checkStep():
    invalidStep()
    detectCurrentStep()
    global currentStepTempleGuardian
    # verificar qual passo esta baseado em prints
    print("Temple Guardian : Checking Steps " + str(currentStepTempleGuardian))
    if currentStepTempleGuardian == 0: # Tap in Menu
        print("Step 0")
        step00()
    elif currentStepTempleGuardian == 1: # Tap in Dungeon
        print("Step 1")
        step01()
    elif currentStepTempleGuardian == 2:  # Tap in Normal Dungeon
        print("Step 2")
        step02()
    elif currentStepTempleGuardian == 3:  # Swipe to Summoning Circle (END)
        print("Step 3")
        step03()
    elif currentStepTempleGuardian == 4:   # Enter in Temple Guardian
        print("Step 4")
        step04()
    elif currentStepTempleGuardian == 5:  # wait to done
        print("Step 5")
        step05() 
    elif currentStepTempleGuardian == '?':  # wait to done
        print("Invalid Step")


def step00():
    if detectInvalidStep():
        touch(923, 30)  # touch(235, 400)

def step01():
    global now
    if detectMenuIsOpened() :
        touch(300, 659)  # touch in dungeon
        time.sleep(2)
        liveScreen()
        time.sleep(2)
        if os.path.isfile('now.png') == True:
            now = cv2.imread("now.png")

def step02():
    global now
    if detectDungeonMenuIsOpened():
        touch(275, 526)  # touch in Normal Dungeon
        time.sleep(2)
        liveScreen()
        time.sleep(2)
        if os.path.isfile('now.png') == True:
            now = cv2.imread("now.png")

def step03():
    global currentStepTempleGuardian
    touch(485, 434) # touch in Temple Guardian
    currentStepTempleGuardian = 4  # ready to touch in Temple Guardian
    return True

def step04():
    global currentStepTempleGuardian, alreadyDone, now, finishedTempleGuardian
    if findImage(now, alreadyDone) or countPixelsInPosition_NOW(622,1086,80,60,[246,109,181],1,100,now):
        print("Already FInished")
        currentStepTempleGuardian = 0  # reset steps
        finishedTempleGuardian = 1  # run to NPC
        touch(1246, 41)  # Back to main screen
    else:
        print("Waiting to Finish")
        touch(1073, 644) # Touch in Enter
        time.sleep(1)
        touch(755, 503) # Auto Join
        time.sleep(1)
        touch(1103, 83) # Close AUto Join
        time.sleep(1)
        touch(1244, 39) # Back to main screen
        currentStepTempleGuardian = 5

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
    global closeDialog, now
    from .loginL2 import text  # extracted text
    # final quest
    if findImage(now, closeDialog):
        markLikeDone()
    elif text.find('Dungeon Cleared') > 0:
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


def markLikeDone():
    global currentStepTempleGuardian, finishedTempleGuardian
    print("Temple Guardian Done Exiting...")
    touch(1000, 673)  # Tap in OK
    currentStepTempleGuardian = 0
    finishedTempleGuardian = 1
    time.sleep(15)
    touch(1243, 39)  # back to main screen
    time.sleep(10)


def detectAreInEnd():
    global currentStepTempleGuardian,now, summoningCircle2
    if findImage(now, summoningCircle2)  or findImage(now, currentStepTempleGuardian) :
        print("Opening Temple Guardian ....")
        return True
  
    return False

def detectInvalidStep():
    global currentStepTempleGuardian
    if checkExist("Resources\pot.png"): # todo check pot 100
        print("Invalid Step")
        return True
    elif checkExist("Resources\pot2.png"): # todo check pot 100
        print("Invalid Step")
        return True
    elif checkExist("Resources\pot3.png"):  # offline mode
        print("Invalid Step")
        return True
    elif checkExist("Resources\pot4.png"):  # offline mode
        print("Invalid Step")
        return True
    elif checkExist("Resources\pot5.png"):  # offline mode
        print("Invalid Step")
        return True
    elif checkExist("Resources\pot6.png"):  # offline mode
        print("Invalid Step")
        return True
    else:
        return False
    

def countPixelsInPosition(top, right, width, height, color, min, max, Print = False):
    global now  # now
    if now is None:
        time.sleep(3)  # skip to next thread execution
        return False

    crop_img = now[top: (top + height), right: (right + width)]
    imm = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
    result = np.count_nonzero(np.all(imm == color, axis=2))
    if Print :
        print("Pixels : " + str(result))
        
    if result >= min and result <= max:
        return True
    else:
        return False


def invalidStep():
    global invalid1Resource, invalid2Resource, currentStepTempleGuardian
    if findImage(now, invalid1Resource) : # I'm Normal Dungeon ?
        currentStepTempleGuardian = 0
        touch(1247,40)
        return True
    if findImage(now, invalid2Resource) : # I'm Normal Dungeon ?
        currentStepTempleGuardian = 3
        touch(40,38)
        return True
    
    return False


def detectCurrentStep():
    from .loginL2 import text  # extracted text
    global dungeon1,limitBreak, now, currentStepTempleGuardian, templeGuardianResource, summoningCircle2, dungeon, dungeon2
    if detectDungeonMenuIsOpened() and  currentStepTempleGuardian < 3:
        currentStepTempleGuardian = 2
        return True
    elif findImage(now, dungeon1) : # I'm Normal Dungeon ?
        currentStepTempleGuardian = 3
        return True
    elif findImage(now, limitBreak) : # I'm Normal Dungeon
        touch(39,37)
        currentStepTempleGuardian = 3  
        return True
    elif findImage(now,summoningCircle2) or findImage(now,templeGuardianResource) : # I'm Normal Dungeon
        print("set Dungeons")
        currentStepSummoningCircle = 3     
        return True
    elif findImage(now, dungeon) : # I'm Dungeon Screen
        currentStepTempleGuardian = 2    
        return True
    elif findImage(now, dungeon2) : # I'm Main Menu
        currentStepTempleGuardian = 1    
        return True
    elif detectMenuIsOpened() and currentStepTempleGuardian != 2:
        print("Auto detect menu")
        return True
    elif countPixelsInPosition(500, 103, 45, 20, [210, 210, 210], 1, 30,True) and countPixelsInPosition(500, 277, 45, 45, [210, 210, 210], 1, 30,True):
        currentStepTempleGuardian = 2  
        return True
    elif countPixelsInPosition(500, 103, 45, 20, [209, 209, 210], 1, 30,True) and countPixelsInPosition(500, 277, 45, 45, [209, 209, 210], 1, 30,True):
        currentStepTempleGuardian = 2  
        return True
    elif countPixelsInPosition(635, 451, 40, 50, [210, 210, 210], 1, 30,True) and countPixelsInPosition(655, 277, 45, 20, [210, 210, 210], 1, 30,True):
        currentStepTempleGuardian = 1    
        return True
    elif countPixelsInPosition(635, 451, 40, 50, [209, 209, 210], 1, 30,True) and countPixelsInPosition(655, 277, 45, 20, [209, 209, 210], 1, 30,True):
        currentStepTempleGuardian = 1    
        return True
    elif currentStepTempleGuardian != 0 and currentStepTempleGuardian != 5 and detectInvalidStep():
        currentStepTempleGuardian = 0  
        return True
    else:
        return False

def checkExist(pic):
    #from .loginL2 import now  # extracted text
    global now
    if now is None:
        print("Erro to get now in checking l2 crasher")
        time.sleep(7) # skip to next thread execution
        return False
    find = cv2.imread(pic)
    if find is None:
        print("Erro ao ver se existe : " + pic)
        time.sleep(7) # skip to next thread execution
        return False
    
    assert not isinstance(find,type(None)), 'image not found'
    try:
        find.shape
        found = findImage(now, find)
        del find
        if found:
            return True
        else:
            return False
    except AttributeError:
        print("shape not found")  
        return False
    

def detectDungeonMenuIsOpened():
    global now, currentStepTempleGuardian
    print("Detecting dungeon menu is opened")
    # Normal Dungeon Alert red circle
    if countPixelsInPosition_NOW(500,330,10,10,[186, 16, 37], 1, 50, now, True):
        currentStepTempleGuardian = 2
        print("Dungeon Alert")
        return True
    
    # World Raid icon
    if countPixelsInPosition_NOW(510,990,10,20,[195,196,197], 1, 100, now) or countPixelsInPosition_NOW(510,990,10,20,[225,224,222], 1, 100, now):
        currentStepTempleGuardian = 2
        print("World Raid Icon")
        return True
    
    # normal dungeon icon
    if countPixelsInPosition_NOW(510,264,30,20,[195,196,197], 1, 100, now, True):
        currentStepTempleGuardian = 2
        print("Normal Dungeon Icon")
        return True
    
    # Temporal Rift icon
    if countPixelsInPosition_NOW(513,412,30,20,[195,196,197], 1, 100, now, True):
        currentStepTempleGuardian = 2
        print("Temporal Rift Icon")
        return True
    
    if countPixelsInPosition_NOW(510,990,10,20,[187,187,187], 1, 100, now, True):
        currentStepTempleGuardian = 2
        print("World Raid Icon2")
        return True
    
    # normal dungeon icon
    if countPixelsInPosition_NOW(510,264,30,20,[187,187,187], 1, 100, now, True):
        currentStepTempleGuardian = 2
        print("Normal Dungeon Icon2")
        return True
    
    # Temporal Rift icon
    if countPixelsInPosition_NOW(513,412,30,20,[187,187,187], 1, 100, now, True):
        currentStepTempleGuardian = 2
        print("Temporal Rift Icon2")
        return True
    
    
    return False

def detectMenuIsOpened():
    global now, currentStepTempleGuardian
    # Rankig icon
    print("Detecting menu is opened")
    # Dungeon icon red ball alert
    if countPixelsInPosition_NOW(622,405,10,10,[186, 16, 37], 10, 50, now):
        currentStepTempleGuardian = 1
        print("Dungeon Alert Circle")
        return True
    
    # Dungeon icon red ball alert
    if countPixelsInPosition_NOW(620,550,10,10,[186, 16, 37], 10, 50, now):
        currentStepTempleGuardian = 1
        print("Batlefield Alert Circle")
        return True
    
    # Batlefield icon red ball alert
    if countPixelsInPosition_NOW(620,550,10,10,[186, 16, 37], 10, 50, now):
        currentStepTempleGuardian = 1
        print("Batlefield Alert Circle")
        return True
    
    # clan icon red ball alert
    if countPixelsInPosition_NOW(620,694,10,10,[186, 16, 37], 10, 50, now):
        currentStepTempleGuardian = 1
        print("social Alert Circle")
        return True
    
    # clan icon red ball alert
    if countPixelsInPosition_NOW(620,840,10,10,[186, 16, 37], 10, 50, now):
        currentStepTempleGuardian = 1
        print("social Alert Circle")
        return True
    
    if countPixelsInPosition_NOW(645,1053,30,20,[187,187,187], 1, 50, now, True):
        currentStepTempleGuardian = 1
        print("Rankig Icon")
        return True
    
    # Trading Post icon
    if countPixelsInPosition_NOW(650,928,45,35,[187,187,187], 1, 50, now, True):
        currentStepTempleGuardian = 1
        print("Trading Post Icon")
        return True
    
    # Friends icon
    if countPixelsInPosition_NOW(630,774,40,35,[187,187,187], 1, 50, now, True):
        currentStepTempleGuardian = 1
        print("Friends Icon")
        return True
    
    return False