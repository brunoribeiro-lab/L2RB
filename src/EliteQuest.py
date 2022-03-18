from .loginL2 import checkExist
from .Utils import checkExist_NOW, extractTextFromResize,countPixelsInPosition_NOW, restartL2, liveScreen, swipe, touch, extractText, countPixelsInPosition, findImageByPosition
from .Utils import findImage
import cv2
import threading
import time
from .Utils import restart
from datetime import date, timedelta, datetime
import numpy as np
import pytesseract
import os
EliteQuestIsDone = 1
finished = 1  # 1-5 max
currentStep = 0  # step 0 = no runinng scroll, 1 = Select Dungeon, 2 = Enter Doungeon, 3 = Start, 4 = Done
inExecution = 0
DungeonDialogPosition = [[205, 0, 230, 90], [289, 0, 230, 90]]
DungeonDialogPositionToTouch = [[108, 249], [108, 335]]
defaultPosition = 0
thread = False
Try = 0 # obsolete
# TODO/IMPROVEMENT
# 1.) Na quinta masmorra o cha fica parado pq tem um mob na frente (Fazer mais testes)
# 2.) Auto-clear all nao funcionando
# 3.) Detectar em qual tela esta em todas as telas
mapOpened = cv2.imread("Resources\Screenshot_20220111-020752.png")
eliteResource = cv2.imread("Resources\Screenshot_20220228-184657.png")
elite2Resource = cv2.imread("Resources\Screenshot_20220228-190211.png")
elite3Resource = cv2.imread("Resources\Screenshot_20220228-190930.png")
elite4Resource = cv2.imread("Resources\Screenshot_20220228-203657.png")
store = cv2.imread("Resources\Screenshot_20220111-002625.png")
shopOpened = cv2.imread("Resources\Screenshot_20220111-002625.png")
shopOpened2 = cv2.imread("Resources\Screenshot_20220111-021906.png")
invalid1Resource = cv2.imread("Resources\Screenshot_20220307-135104.png")
invalid2Resource = cv2.imread("Resources\Screenshot_20220306-142327.png")
required16 = cv2.imread("Resources\elvenRuins1.png")
required16_2 = cv2.imread("Resources\elvenRuins2.png")
die = cv2.imread("Resources\die.png")
def loopEliteQuest():
    global thread
    if thread != False and thread.isAlive():
        thread.join()    
             
    thread = threading.Timer(8.0, doEliteQuests)
    thread.daemon = True # stop if the program exits
    thread.setName("Elite Quests Thread")
    thread.start()

def doEliteQuests():
    global finished, Try, now, currentStep, inExecution, EliteQuestIsDone 
    from .loginL2 import logged
    from .SummoningCircle import finishedSummoningCircle
    from .DailyDungeon import DailyDungeonIsDone
    from .TempleGuardian import finishedTempleGuardian
    from .TowerOfInsolence import TowerOfInsolenceIsDone
    if not logged or not TowerOfInsolenceIsDone or not DailyDungeonIsDone or not finishedTempleGuardian or EliteQuestIsDone:
        print("*****")
        return False
    
    print("======== Elite Quest Thread =========== ")
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
        size = os.path.getsize("./now.png")
        if size < 200:
            print("problem with current screen : " + str(size))
                
        assert not isinstance(now, type(None)), 'image not found'
        Try = 0
        if finished > 5 and getAutoClearAll():
            claimAll()
            touch(1243, 39)  # back to main screen
            return True

        print("Current Dungeon : " + str(finished))
        # now = datetime.now()
       #print(str(now.strftime("%H:%M:%S")))
        inExecution = 1
        checkDie()
        checkStep()
        inExecution = 0
    print("======== End Elite Quest Thread =========== ")

# change step 1-3 to close dialogs and step 4 is final quest


def checkStep():
    detectInvalidScreen()
    # verificar qual passo esta baseado em prints
    detectCurrentStep()
    global currentStep
    print("Elite Quests : Cheking Steps : " + str(currentStep))
   
    # checkCompleted()
    if currentStep == 0:  # Main screen
        print("Step 0")
        step00()
    elif currentStep == 1:  # Touch Dungeon
        print("Step 1")
        step01()
    elif currentStep == 2:  # Touch in Normal Dungeon
        print("Step 2")
        step02()
    elif currentStep == 3:  # Looking for elite
        print("Step 3")
        step03()
    elif currentStep == 4:  # swipe to top
        print("Step 4")
        step04()
    elif currentStep == 5:  # choice the dungeon
        print("Step 5")
        step05()
    elif currentStep == 6:  # start quest
        print("Step 6")
        step06()
    elif currentStep == 7:  # start quest
        print("Step 7")
        step07()

def checkDie():
    global currentStep, now, die
    if(findImage(now, die)):
        print("I Die")
        currentStep = 5
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
    touch(930, 88)  # leave from elite dungeon
    time.sleep(5)


def step00():
    global currentStep, now
    if detectMainScreen():
        print("Touch in Menu")
        touch(923, 30)  # Touch in menu
        time.sleep(2)
        liveScreen()
        time.sleep(2)
        if os.path.isfile('now.png') == True:
            now = cv2.imread("now.png")


def step01():
    global currentStep, now
    if detectMenuIsOpened():
        print("Touch in Dungeon")
        touch(300, 659)  # touch in dungeon
        time.sleep(2)
        liveScreen()
        time.sleep(2)
        if os.path.isfile('now.png') == True:
            now = cv2.imread("now.png")


def step02():
    global currentStep, now
    touch(120, 517)  # touch in Normal Dungeon
    currentStep = 3
    time.sleep(3)
    liveScreen()
    time.sleep(2)
    if os.path.isfile('now.png') == True:
        now = cv2.imread("now.png")


def step03():
    global currentStep, now
    if findImageByPosition(167,543,320,515,now, eliteResource):
        print("Tap in Elite Dungeon")
        touch(710,420)
        currentStep = 4  # just choice the spot
        time.sleep(4)
        liveScreen()
        time.sleep(2)
        if os.path.isfile('now.png') == True:
            now = cv2.imread("now.png")
    else:
        print("Swipe to start")
        swipe(40, 420, 800, 420, 0.5)  # swipe a little bit to down
        time.sleep(4)
        liveScreen()
        time.sleep(2)
        if os.path.isfile('now.png') == True:
            now = cv2.imread("now.png")

def step04():
    global currentStep, now, finished, required16, required16_2
    if findImageByPosition(100, 27, 250, 150, now, required16) or findImageByPosition(100, 27, 250, 150, now, required16_2):
        print('First Dungeon')
        #touch(325, 179)
        currentStep = 5  # select the dungeon
        return False
    elif getAutoClearAll():
        return claimAll()
    else:
        currentStep = 4  # swipe again
        swipe(320, 129, 320, 655, 0.5)  # swipe to top
        time.sleep(3)
        liveScreen()
        time.sleep(2)
        if os.path.isfile('now.png') == True:
            now = cv2.imread("now.png")


def step05():
    global currentStep, finished
    #autoDetectDone()
    if finished == 1:
        touch(325, 179)
        time.sleep(2)
        liveScreen()
        time.sleep(2)
        if os.path.isfile('now.png') == True:
            now = cv2.imread("now.png")
    elif finished == 2:
        touch(336, 323)
        time.sleep(2)
        liveScreen()
        time.sleep(2)
        if os.path.isfile('now.png') == True:
            now = cv2.imread("now.png")
    elif finished == 3:
        touch(325, 457)
        time.sleep(2)
        liveScreen()
        time.sleep(2)
        if os.path.isfile('now.png') == True:
            now = cv2.imread("now.png")
    elif finished == 4:
        touch(334, 583)
        time.sleep(2)
        liveScreen()
        time.sleep(2)
        if os.path.isfile('now.png') == True:
            now = cv2.imread("now.png")
    elif finished == 5:
        if getAutoClearAll():
            return claimAll()
        else:
            swipe(320, 129, 320, 655, 0.5)  # swipe to top
            time.sleep(2)
            swipe(320, 129, 320, 655, 0.5)  # swipe to top
            time.sleep(2)
            swipe(320, 129, 320, 655, 0.5)  # swipe to top
            time.sleep(2)
            swipe(320, 655, 320, 455, 0.5)  # swipe a little bit to down
            time.sleep(2)
            touch(319, 376)

    getSelected = getSelectedDungeon()
    print("Selected : " + str(getSelected))
    print("Finished : " + str(finished))
    if getSelected == finished:
        if checkDOungeonCompleted():
            print("This dungeon is completed, step to next")
            finished = getSelected + 1
            currentStep = 4
            return True
        else:
            currentStep = 6
            time.sleep(4)
            return True
    else:
        currentStep = 4 # back to previous step, and select first dungeon
        return False

# check is complete if not enter dungeon
def autoDetectDone():
    global now  # extracted text
    global finished
    required16Done = cv2.imread("Resources\Screenshot_20211217-225542.png")
    
    if(findImageByPosition(127, 453, 593-453, 238-127, now, required16Done)):
        print("Selected Elven Ruins 1 Done")
        finished = 1
        return True
    
    if(findImageByPosition(260, 453, 593-453, 584-260, now, required16Done)):
        print("Selected Elven Ruins 2 Done")
        finished = 2
        return True
    
    return finished

def step06():
    global currentStep
    global finished
    if getAutoClearAll():
        return claimAll()
    
    touch(1113, 656)  # enter in dungeon
    time.sleep(5)
    currentStep = 7

def step07():
    global currentStep, defaultPosition, DungeonDialogPositionToTouch
    global finished
    from .loginL2 import text  # extracted text
    # Detect is not running
    if countPixelsInPosition(332, 244, 10, 5, [87, 208, 255], 1, 10):
        # detect is Done alert
        if countPixelsInPosition(236, 218, 5, 10, [234, 240, 251], 1, 10):
            print("Done")
            time.sleep(2)
            successClaim()
            return True
        else:
            touch(DungeonDialogPositionToTouch[defaultPosition][0],
                  DungeonDialogPositionToTouch[defaultPosition][1])  # touch in start
            time.sleep(2)
            liveScreen()
            time.sleep(2)
            return True
    # detect is Done alert
    elif countPixelsInPosition(236, 218, 5, 10, [234, 240, 251], 1, 10):
        print("Done")
        time.sleep(2)
        successClaim()
        return True
    else:
        print("waiting elite quest progress")
        return False

def successClaim():
    global finished
    global currentStep
    finished += 1
    currentStep = 4
    print("Claim and Leave")
    touch(244, 243)  # click in done
    time.sleep(3)
    touch(503, 617)  # touch in claim reward
    time.sleep(2)
    touch(861, 88)  # touch in leave
    time.sleep(3)


def checkDOungeonCompleted():
    global now
    # auto complete color
    if countPixelsInPosition_NOW(526,944,300,60,[222,198,140],1,100, now):
        return False
    
    if countPixelsInPosition_NOW(526,944,300,60,[26,32,43],17000,20000, now):
        return True
    
    # white color from text button
    """if countPixelsInPosition_NOW(526,944,300,60,[255,255,255],100,500, now):
        return False"""
    # pink color from red diamond
    if countPixelsInPosition_NOW(526,944,300,60,[246,109,181],1,100, now):
        return False
     # light pink color from red diamond
    if countPixelsInPosition_NOW(526,944,300,60,[254,191,224],1,100, now):
        return False
    # green color from button, is all completed
    if countPixelsInPosition_NOW(526,944,300,60,[51,105,72],1,500, now):
         claimAll()
         touch(1243, 39)  # back to main screen
    
    return True


def getSelectedDungeon():
    global now, required16_2  # extracted text
    if countPixelsInPosition_NOW(113,38,300,10,[99,150,217],1, 500, now, True) :
        print("Selected Elven Ruins 1")
        return 1
    
    if countPixelsInPosition_NOW(250,38,300,10,[99,150,217],1,500,now,True) :
        print("Selected Elven Ruins 2")
        return 2

    if countPixelsInPosition_NOW(385,38,300,10,[99,150,217],1,500,now,True) :
        print("Selected Ant Nest 1")
        return 3

    if countPixelsInPosition_NOW(522,38,300,10,[99,150,217],1,500,now,True) :
        print("Selected Ant Nest 2")
        return 4

    if countPixelsInPosition_NOW(658,38,300,10,[99,150,217],1,500,now,True) :
        print("Selected Cruma Tower 2F")
        return 5

    print("Elite not found")
    return 0

def getDoingStatus():
    global DungeonDialogPosition, defaultPosition, now

    top = 290  # DungeonDialogPosition[defaultPosition][0]
    right = 0  # DungeonDialogPosition[defaultPosition][1]
    height = 80  # DungeonDialogPosition[defaultPosition][3]
    width = 182  # DungeonDialogPosition[defaultPosition][2]
    crop_img = now[top: (top + height), right: (right + width)]
    sought = [141, 176, 255]  # red
    imm = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
    result = np.count_nonzero(np.all(imm == sought, axis=2))

    print("Total blue pixels : " + str(result))
    if result >= 600:
        return True
    else:
        return False


def getDoneStatus():
    from .loginL2 import now  # extracted text
    if now is None:
        time.sleep(7)  # skip to next thread execution
        return False

    top = 219
    right = 219
    height = 50
    width = 50
    crop_img = now[top: (top + height), right: (right + width)]
    sought = [255, 255, 255]  # red
    imm = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
    result = np.count_nonzero(np.all(imm == sought, axis=2))
    print("Total pixels white : " + str(result))
    if result > 9 and result < 15:  # 240
        return True
    else:
        return False


def getAutoClearAll():
    global finished, now
    if countPixelsInPosition_NOW(629,630,350,60,[124,139,158],70,100,now) > 0:
        return False
    else:
        return True


def claimAll():
    print('Done Elite Quest')
    global EliteQuestIsDone, finished, currentStep
    touch(790, 657)  # touch in Auto-Clear All
    time.sleep(3)
    # tem que verificar aqui se ja terminou para ignorar
    touch(925, 618)
    time.sleep(3)
    touch(1103, 87)
    time.sleep(3)
    touch(1245, 38)
    time.sleep(3)
    currentStep = 0  # select the dungeon
    finished = 6
    EliteQuestIsDone = 1
    return False

def detectInvalidScreen():
    global now,currentStep, mapOpened, invalid1Resource, invalid2Resource
    # check map is opened for any reason
    if countPixelsInPosition_NOW(660, 1015, 200, 50, [52, 83, 112], 300, 1000, now):
        print("Closing Map")
        touch(1243, 38)  # touch in back
        return True
    
    if findImage(now, invalid1Resource) : # I'm Normal Dungeon ?
        currentStep = 0
        touch(1247,40)
        return True
    if findImage(now, invalid2Resource) : # I'm Normal Dungeon ?
        currentStep = 3
        touch(40,38)
        return True
    

def detectCurrentStep():
    global now, currentStep, store, shopOpened, shopOpened2, eliteResource
    if findImageByPosition(167,543,320,515,now, eliteResource):
        print("Elite Dungeon Menu")
        currentStep = 3
        return True
    if detectMenuIsOpened() and currentStep != 2 and currentStep != 1:
         currentStep = 1
         print("Change to step 1")
         return True
    elif countPixelsInPosition_NOW(605,234,130,55,[129, 236, 255], 1, 50, now) or countPixelsInPosition_NOW(605,234,130,55,[178,200,228], 1, 50, now)  or countPixelsInPosition_NOW(605,234,130,55,[128,233,255], 1, 50, now) or countPixelsInPosition_NOW(493,146,20,30,[184,16,36], 1, 50, now):
        currentStep = 2
        print("Selected Dungeon")
        return True
    #elif currentStep != 4 and findImageByPosition(320,1099,160,78,now, elite2Resource):
    #    print("Elite Dungeon Menu Selector")
    #    currentStep = 4   
    #    return True
    #elif currentStep == 5 and not ImEliteDungeon(now):
    #    currentStep = 0
    #    return True
    elif currentStep > 0 and currentStep < 6 and detectInvalidStep():
        currentStep = 0
        return True
    # check is store screen
    elif findImage(now, store):
        print("Invalid Screen, Backing to Main Screen")
        touch(1243, 38)
        time.sleep(1)
        currentStep = 0
        return True
    elif findImage(now, shopOpened) and currentStep != 4:
        print("Invalid Screen, MAP, Backing to Main Screen")
        touch(1243, 38)
        time.sleep(1)
        currentStep = 0
        return True
    elif findImage(now, shopOpened2) and currentStep != 4:
        print("Invalid Screen, MAP, Backing to Main Screen")
        touch(1068, 57)
        time.sleep(1)
        currentStep = 0
        return True
    else:
        return False
    
    

def detectInvalidStep():
    global now
    if checkExist_NOW(now, "Resources\pot.png"):  # todo check pot 100
        print("Invalid Step")
        return True
    elif checkExist_NOW(now, "Resources\pot2.png"):  # todo check pot 100
        print("Invalid Step")
        return True
    elif checkExist_NOW(now, "Resources\pot3.png"):  # offline mode
        print("Invalid Step")
        return True
    elif checkExist_NOW(now, "Resources\pot4.png"):  # offline mode
        print("Invalid Step")
        return True
    elif checkExist_NOW(now, "Resources\pot5.png"):  # offline mode
        print("Invalid Step")
        return True
    elif checkExist_NOW(now, "Resources\pot6.png"):  # offline mode
        print("Invalid Step")
        return True
    else:
        return False
    
def detectMenuIsOpened():
    global now, currentStep
    # Rankig icon
    print("Detecting menu is opened")
    # Selected Dungeon
    if countPixelsInPosition_NOW(652,1130,30,20,[184, 184, 185], 1, 10, now):
        print("Rankig Icon")
        return True
    
    # Trading Post icon
    if countPixelsInPosition_NOW(650,964,45,35,[184, 184, 185], 1, 20, now):
        print("Trading Post Icon")
        return True
    
    # Friends icon
    if countPixelsInPosition_NOW(638,800,40,35,[184, 184, 185], 1, 50, now):
        print("Friends Icon")
        return True
    
    return False


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
    
def ImEliteDungeon(now):
    print("Detecting I'm in World Dungeon")
    # black ton
    if detectMainScreen() and countPixelsInPosition_NOW(157, 1165, 30, 25, [176, 177, 178], 1, 100, now):
        print("I'm Elite Dungeon")
        return True
    # gray ton
    elif detectMainScreen() and countPixelsInPosition_NOW(157, 1165, 30, 25, [190, 191, 192], 1, 100, now):
        print("I'm Elite Dungeon²")
        return True
    elif not detectMainScreen():
        return True
    else:
        return False