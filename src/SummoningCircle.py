from .Utils import countPixelsInPosition_NOW, findImageByPosition, touch, liveScreen, findImage, find_matches, extractTextFromResize
from .Utils import swipe, restartL2
import cv2
import threading
import time
import os
import numpy as np
Try = 0
alreadyDone = cv2.imread("Resources\Screenshot_20220101-172942.png")
die = cv2.imread("Resources\die.png")
limitBreak = cv2.imread("Resources\Screenshot_20220101-161653.png")
dungeon1 = cv2.imread("Resources\Screenshot_20220101-155243.png")
closeDialog = cv2.imread("Resources\summoningCircle.png")
summoningCircle2 = cv2.imread("Resources\summoningCircleText.png")
dungeon = cv2.imread("Resources\Screenshot_20220101-143001.png")
dungeon2 = cv2.imread("Resources\Screenshot_20220101-150154.png")
store = cv2.imread("Resources\Screenshot_20220111-002625.png")
invalid1Resource = cv2.imread("Resources\Screenshot_20220307-135104.png")
invalid2Resource = cv2.imread("Resources\Screenshot_20220306-142327.png")

finishedSummoningCircle = 1
currentStepSummoningCircle = 0
inExecution = False
thread = False
jumps = 1
jumpsC = 0
now = False
# 2 bugs
# verificar telas invalidas
# verificar se tem tons vermelhos para n repetir e gastar os reds
def loopSummoningCircle():
    global thread, jumpsC, jumps
    if thread != False and thread.isAlive():
        thread.join()   
        
    thread = threading.Timer(8.0, doSummoningCircle)
    thread.daemon = True # stop if the program exits
    thread.setName("Summoning Circle Thread")
    thread.start()


def doSummoningCircle():
    global inExecution,Try, now, thread, finishedSummoningCircle, currentStepSummoningCircle
    from .loginL2 import logged
    if logged == 0:
        return False
    
    if finishedSummoningCircle == 1:
        thread.cancel()
        thread = False
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
        channels = now.shape[2]
        if size < 200:
            print("problem with current screen : " + str(size))
            
        assert not isinstance(now, type(None)), 'image not found'
        Try = 0
        checkStep()

# change step 1-3 to close dialogs and step 4 is final quest

def checkDie():
    global now,die
    if now is None:
        time.sleep(5)  # skip to next thread execution
        return False

    if findImage(now, die):
        print("I die back to spot")
        revival()
        return True
    return False

def revival():
    print("Back to live")
    touch(637, 480)  # click in OK
    time.sleep(1)
    touch(635, 500)  # click in OK
    time.sleep(1)
    touch(1153, 530)  # tap in spot revival

def checkStep():
    invalidStep()
    detectCurrentStep()
    global currentStepSummoningCircle
    print("Sumonning Circle : Checking Steps " + str(currentStepSummoningCircle))  # verificar qual passo esta baseado em prints
    if currentStepSummoningCircle == 0:  # Tap in Menu
        print("Step 0")
        step00()
    elif currentStepSummoningCircle == 1:  # Tap in Dungeon
        print("Step 1")
        step01()
    elif currentStepSummoningCircle == 2:  # Tap in Normal Dungeon
        print("Step 2")
        step02()
    elif currentStepSummoningCircle == 3:  # Swipe to Summoning Circle
        print("Step 3")
        step03()
    elif currentStepSummoningCircle == 4:  # Enter in Sumonning Circle
        print("Step 4")
        step04()
    elif currentStepSummoningCircle == 5:  # wait to done
        print("Step 5")
        step05()
    elif currentStepSummoningCircle == '?':  
        print("Invalid Step")


def step00():
    global currentStepSummoningCircle
    if detectInvalidStep():
        touch(923, 30)  # touch(235, 400)
        

def step01():
    global currentStepSummoningCircle, now
    touch(300, 659)  # touch in dungeon
    time.sleep(2)
    liveScreen()
    time.sleep(2)
    if os.path.isfile('now.png') == True:
        now = cv2.imread("now.png")

def step02():
    global currentStepSummoningCircle, dungeon, now
    touch(120, 515)  # touch in Normal Dungeon
    time.sleep(2)
    liveScreen()
    time.sleep(2)
    if os.path.isfile('now.png') == True:
        now = cv2.imread("now.png")

def step03():
    global currentStepSummoningCircle
    if detectAreInEnd():
        print("DEVERIAMOS CLICAR AQUI")
        touch(850, 346)
        currentStepSummoningCircle = 4  # ready to touch in Temple Guardian
        return True
    else:
        print("Swiping to end")
        swipe(800, 420, 40, 420, 0.5)  # swipe a little bit to down
        return False

def step04():
    global currentStepSummoningCircle, now, alreadyDone
    global finishedSummoningCircle
    # final quest
    checkAlreadyDone = findImage(now, alreadyDone)
    if checkAlreadyDone or countPixelsInPosition_NOW(622,1086,80,60,[246,109,181],1,100,now):
        print("Already FInished")
        currentStepSummoningCircle = 0  # reset steps
        finishedSummoningCircle = 1  # run to NPC
        # touch(1066, 278) # Back to main screen
        # time.sleep(2)
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
        currentStepSummoningCircle = 5
    
def step05():
    global currentStepSummoningCircle
    global finishedSummoningCircle
    global closeDialog,now
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

def invalidStep():
    global invalid1Resource, invalid2Resource, currentStepSummoningCircle
    if findImage(now, invalid1Resource) : # I'm Normal Dungeon ?
        currentStepSummoningCircle = 0
        touch(1247,40)
        return True
    if findImage(now, invalid2Resource) : # I'm Normal Dungeon ?
        currentStepSummoningCircle = 3
        touch(40,38)
        return True
    
    return False

def detectCurrentStep():
    from .loginL2 import text  # extracted text
    global dungeon1,limitBreak, now, currentStepSummoningCircle,store, summoningCircle2, dungeon, dungeon2
    if findImage(now, dungeon1) : # I'm Normal Dungeon ?
        currentStepSummoningCircle = 3
        return True
    elif findImage(now, limitBreak) : # I'm Normal Dungeon
        touch(39,37)
        currentStepSummoningCircle = 3  
        return True
    elif findImageByPosition(165,686,300,400,now,summoningCircle2) : # I'm Normal Dungeon
        print("set Dungeons")
        currentStepSummoningCircle = 3     
        return True
    elif findImage(now, dungeon) : # I'm Dungeon Screen
        currentStepSummoningCircle = 2    
        return True
    elif findImage(now, dungeon2) : # I'm Main Menu
        currentStepSummoningCircle = 1    
        return True
    elif countPixelsInPosition(500, 103, 45, 20, [210, 210, 210], 1, 30,True) and countPixelsInPosition(500, 277, 45, 45, [210, 210, 210], 1, 30,True):
        currentStepSummoningCircle = 2  
        return True
    elif countPixelsInPosition(500, 103, 45, 20, [209, 209, 210], 1, 30,True) and countPixelsInPosition(500, 277, 45, 45, [209, 209, 210], 1, 30,True):
        currentStepSummoningCircle = 2  
        return True
    elif countPixelsInPosition(635, 451, 40, 50, [210, 210, 210], 1, 30,True) and countPixelsInPosition(655, 277, 45, 20, [210, 210, 210], 1, 30,True):
        currentStepSummoningCircle = 1    
        return True
    elif countPixelsInPosition(635, 451, 40, 50, [209, 209, 210], 1, 30,True) and countPixelsInPosition(655, 277, 45, 20, [209, 209, 210], 1, 30,True):
        currentStepSummoningCircle = 1    
        return True
    elif currentStepSummoningCircle != 0 and currentStepSummoningCircle != 5 and detectInvalidStep():
        currentStepSummoningCircle = 0  
        return True
    elif findImage(now, store) :
        print("Invalid Screen, Backing to Main Screen")
        touch(1243, 38)
        time.sleep(1)
        currentStepSummoningCircle = 0
        return True
    else:
        currentStepSummoningCircle == '?'
        return False

def markLikeDone():
    global currentStepSummoningCircle, finishedSummoningCircle
    print("Sumonning Circle Done Exiting...")
    touch(1000, 673)  # Tap in OK
    currentStepSummoningCircle = 0
    finishedSummoningCircle = 1
    time.sleep(15)
    touch(1243, 39)  # back to main screen
    time.sleep(10)
    

def detectAreInEnd():
    global currentStepSummoningCircle,now, summoningCircle2
    if findImageByPosition(165,686,300,400,now,summoningCircle2):
        return True
  
    return False
    """
    text = extractTextFromResize(165, 985, 257, 420)
    print("TEXT FROM RESZIZE : ")
    print(text)
    if text.find("Harvest") > 0:
        return True
    elif text.find("Mam Professions") > 0 or text.find("Mai Professions") > 0:
        return True
    else:
        return False"""
    
def detectInvalidStep():
    global currentStepSummoningCircle
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