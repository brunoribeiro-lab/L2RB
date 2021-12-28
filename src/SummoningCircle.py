from .Utils import touch, liveScreen, findImage, find_matches, extractTextFromResize
from .Utils import swipe
import cv2
import threading
import time

closeDialog = cv2.imread("Resources\summoningCircle.png")
finishedSummoningCircle = 1
currentStepSummoningCircle = 0
inExecution = False
thread = False

def loopSummoningCircle():
    global thread
    if thread != False and thread.isAlive():
        thread.cancel()
        
    thread = threading.Timer(8.0, loopSummoningCircle)
    thread.start()
    doSummoningCircle()


def doSummoningCircle():
    global inExecution, thread, finishedSummoningCircle, currentStepSummoningCircle
    from .loginL2 import logged
    if logged == 0:
        return False
    
    if finishedSummoningCircle == 1:
        thread.cancel()
        inExecution = False
        return False
    
    if inExecution == False:
        inExecution = True
        checkStep()
        inExecution = False

# change step 1-3 to close dialogs and step 4 is final quest


def checkStep():
    global currentStepSummoningCircle
    print("Sumonning Circle : Checking Steps")  # verificar qual passo esta baseado em prints
    if currentStepSummoningCircle == 0:  # start quest
        print("Step 0")
        step00()
    elif currentStepSummoningCircle == 1:  # I'm in summoning circle scren
        print("Step 1")
        step01()
        detectInvalidStep()
    elif currentStepSummoningCircle == 2:  # Checking if avaiable
        print("Step 2")
        step02()
        detectInvalidStep()
    elif currentStepSummoningCircle == 3:  # check already done
        print("Step 3")
        step03()
        detectInvalidStep()
    elif currentStepSummoningCircle >= 4:  # wait to done
        print("Step 4")
        step04()


def step00():
    global currentStepSummoningCircle
    touch(923, 30)  # touch(235, 400)
    from .loginL2 import text  # extracted text
    if text.find('Dungeon'):
        touch(300, 659)  # touch in dungeon
        time.sleep(1)
        liveScreen()
        time.sleep(2)
        currentStepSummoningCircle = 1
    """
    # tap
    touch(921, 31)
    time.sleep(2)
    touch(300, 661)  # Dungeon
    time.sleep(3)
    touch(123, 517)  # Normal Dungeon
    time.sleep(4)
    swipe(373, 390, 1190, 390, 0.5)  # swipe to start
    time.sleep(4)
    swipe(1190, 390, 373, 390, 0.5)  # swipe to end
    time.sleep(3)
    touch(852, 359)  # Enter SUmmoning Circle
    currentStepSummoningCircle = 1"""


def step01():
    global currentStepSummoningCircle
    from .loginL2 import text  # extracted text
    if text.find('Normal Dungeon'):
        currentStepSummoningCircle = 2  # run to NPC
        touch(120, 515)  # touch in Normal Dungeon
        time.sleep(1)
        liveScreen()
        time.sleep(2)
    elif text.find('Temporal Rift'):
        currentStepSummoningCircle = 2  # run to NPC
        touch(120, 515)  # touch in Normal Dungeon
        time.sleep(1)
        liveScreen()
        time.sleep(2)
    """
    print("Checking if I'm in Summoning Circle screen")
    now = cv2.imread("now.png")
    ImHere = cv2.imread("Resources\summoningCircleScreen.png")
    checkImHere = findImage(now, ImHere)
    if checkImHere:
        print("I'm here")
        currentStepSummoningCircle = 2
    else:
        print("I'm not here")
        touch(1246, 41)  # Back to main screen
        time.sleep(2)
        touch(995, 341)  # touch out
        currentStepSummoningCircle = 1"""


def step02():
    global currentStepSummoningCircle
    if detectAreInEnd():
        print("DEVERIAMOS CLICAR AQUI")
        #touch(1200, 377)  # touch in dungeon
        currentStepSummoningCircle = 3  # ready to touch in Temple Guardian
        return False
    else:
        print("Swiping to end")
        swipe(800, 420, 40, 420, 0.5)  # swipe a little bit to down
        time.sleep(2)
        liveScreen()
        time.sleep(2)
    """
    print("Checking if avaiable")
    now = cv2.imread("now.png")
    alreadyDone = cv2.imread("Resources\play2.png")
    enter = cv2.imread("Resources\enter.png")
    checkTypeButton = findImage(now, alreadyDone)
    checkEnterButton = findImage(now, enter)
    if checkTypeButton:
        print("Sumonning Circle Avaiable")
        time.sleep(3)
        touch(1068, 645)  # Enter SUmmoning Circle
        time.sleep(3)
        touch(755, 487)  # Confirm enter
        time.sleep(3)
        touch(1103, 83)  # close first dialog
        time.sleep(2)
        touch(1246, 41)  # Back to main screen
        currentStepSummoningCircle = 3  # next Step
        return True
    elif checkEnterButton:
        print("Sumonning Circle Avaiable")
        time.sleep(3)
        touch(1068, 645)  # Enter SUmmoning Circle
        time.sleep(3)
        touch(755, 487)  # Confirm enter
        time.sleep(3)
        touch(1103, 83)  # close first dialog
        time.sleep(2)
        touch(1246, 41)  # Back to main screen
        currentStepSummoningCircle = 3  # next Step
        return True
    else:
        print("Sumonning Circle unavaiable")
        global finishedSummoningCircle
        currentStepSummoningCircle = 0
        finishedSummoningCircle = 1
        return False"""


def step03():
    global currentStepSummoningCircle
    global finishedSummoningCircle
    # final quest
    now = cv2.imread("now.png")
    alreadyDone = cv2.imread("Resources\summoningCircleAlreadyDone.png")
    checkAlreadyDone = findImage(now, alreadyDone)
    if checkAlreadyDone:
        print("Already FInished")
        currentStepSummoningCircle = 0  # reset steps
        finishedSummoningCircle = 1  # run to NPC
        # touch(1066, 278) # Back to main screen
        # time.sleep(2)
        touch(1246, 41)  # Back to main screen
    else:
        print("Waiting to Finish")
        # touch(1372, 804) # Enter SUmmoning Circle
        # time.sleep(2)
        # touch(1372, 804) # Auto Join
        # time.sleep(2)
        # touch(1376, 104) # Close AUto Join
        # time.sleep(2)
        # touch(1556, 49) # Back to main screen
        currentStepSummoningCircle = 3


def step04():
    global currentStepSummoningCircle
    global finishedSummoningCircle
    global closeDialog
    from .loginL2 import now,text  # extracted text
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
    print("Sumonning Circle Done Exiting...")
    touch(1000, 673)  # Tap in OK
    currentStepSummoningCircle = 0
    finishedSummoningCircle = 1
    time.sleep(25)
    touch(1243, 39)  # back to main screen
    time.sleep(5)
    

def detectAreInEnd():
    global currentStepSummoningCircle
    from .loginL2 import now  # extracted text
    if now is None:
        time.sleep(7)  # skip to next thread execution
        return 0
    
    lauch = cv2.imread("Resources\Screenshot_20211227-143650.png")
    positions = find_matches(now, lauch)
    if len(positions) > 0:
        print("Opening Sumonning Circle ....")
        x = positions[0][0]
        y = positions[0][1]
        touch(x, y)
        currentStepSummoningCircle = 3
        return True
    else:
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
        currentStepSummoningCircle = 0
        return True
    elif checkExist("Resources\pot2.png"): # todo check pot 100
        print("Invalid Step")
        currentStepSummoningCircle = 0
        return True
    elif checkExist("Resources\pot3.png"):  # offline mode
        print("Invalid Step")
        currentStepSummoningCircle = 0
        return True
    elif checkExist("Resources\pot4.png"):  # offline mode
        print("Invalid Step")
        currentStepSummoningCircle = 0
        return True
    elif checkExist("Resources\pot5.png"):  # offline mode
        print("Invalid Step")
        currentStepSummoningCircle = 0
        return True
    elif checkExist("Resources\pot6.png"):  # offline mode
        print("Invalid Step")
        currentStepSummoningCircle = 0
        return True
    
def checkExist(pic):
    from .loginL2 import now  # extracted text
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