from .loginL2 import checkExist
from .Utils import extractTextFromResize, liveScreen, swipe, touch, extractText, countPixelsInPosition, findImageByPosition
from .Utils import findImage
import cv2
import threading
import time
from .Utils import restart
from datetime import date, timedelta, datetime
import numpy as np
import pytesseract
EliteQuestIsDone = 1
finished = 1  # 1-5 max
currentStep = 0  # step 0 = no runinng scroll, 1 = Select Dungeon, 2 = Enter Doungeon, 3 = Start, 4 = Done
inExecution = 0
DungeonDialogPosition = [[205, 0, 230, 90], [289, 0, 230, 90]]
DungeonDialogPositionToTouch = [[108, 249], [108, 335]]
defaultPosition = 0
# TODO/IMPROVEMENT
# 1.) Na quinta masmorra o cha fica parado pq tem um mob na frente (Fazer mais testes)
# 2.) Auto-clear all nao funcionando
# 3.) Detectar em qual tela esta em todas as telas


def loopEliteQuest():
    threading.Timer(6.0, loopEliteQuest).start()
    doEliteQuests()


def doEliteQuests():
    global finished
    global currentStep
    global inExecution
    global EliteQuestIsDone
    from .loginL2 import logged
    from .loginL2 import text  # extracted text
    from .SummoningCircle import finishedSummoningCircle
    from .DailyDungeon import DailyDungeonIsDone
    from .TempleGuardian import finishedTempleGuardian
    from .TowerOfInsolence import TowerOfInsolenceIsDone
    if logged == 0:
        return False

    if TowerOfInsolenceIsDone == 0:
        return False

    if DailyDungeonIsDone == 0:
        return False

    if finishedTempleGuardian == 0:
        return False

    if EliteQuestIsDone == 1:
        return False

    if finished > 5:
        # temos que verificar se acabou tudo
        if getAutoClearAll():
            claimAll()
            touch(1243, 39)  # back to main screen
            return True

        return False

    if inExecution == 0:
        print("Current Dungeon : " + str(finished))
        now = datetime.now()
        print(str(now.strftime("%H:%M:%S")))
        inExecution = 1
        checkDie()
        checkStep()
        inExecution = 0

# change step 1-3 to close dialogs and step 4 is final quest


def checkStep():
    global currentStep
    # verificar qual passo esta baseado em prints
    print("Elite Quests : Cheking Steps")
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
    elif currentStep == 8:  # start quest
        print("Step 8")
        step08()


def checkCompleted():
    global finished
    global currentStep
    from .loginL2 import text  # extracted text
    if text.find('Complete Count 10/10') > 0:
        finished = 10
        currentStep = 1
        touch(1014, 173)
        return True
    elif text.find('Count 10/10') > 0:
        finished = 10
        currentStep = 1
        touch(1014, 173)
        return True
    elif text.find('Recharge') > 0:
        finished = 10
        currentStep = 1
        touch(1014, 173)
        return True


def checkDie():
    from .loginL2 import now  # extracted text
    global currentStep
    if now is None:
        time.sleep(7)  # skip to next thread execution
        return 'NO'
    die = cv2.imread("Resources\die.png")
    status = findImage(now, die)
    if(status):
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
    global currentStep
    touch(923, 30)  # touch(235, 400)
    from .loginL2 import text  # extracted text
    if text.find('Dungeon'):
        currentStep = 1  # run to NPC


def step01():
    global currentStep
    touch(300, 659)  # touch in dungeon
    from .loginL2 import text  # extracted text
    if text.find('Normal Dungeon'):
        currentStep = 2  # run to NPC
    elif text.find('Temporal Rift'):
        currentStep = 2  # run to NPC


def step02():
    global currentStep
    touch(120, 515)  # touch in Normal Dungeon
    from .loginL2 import text  # extracted text
    if text.find('Elite Dungeon'):
        currentStep = 3  # run to NPC
    elif text.find('Extraction Pit'):
        currentStep = 3  # run to NPC


def step03():
    global currentStep
    touch(700, 358)  # touch in dungeon
    from .loginL2 import text  # extracted text
   # if getAutoClearAll():
   #     return claimAll()
    if text.find('Required Level'):
        currentStep = 4  # run to NPC
        time.sleep(10)
    elif text.find('Ivory Tower'):
        currentStep = 4  # run to NPC
        time.sleep(10)
    elif text.find('Catacomb'):
        currentStep = 4  # run to NPC
        time.sleep(10)


def step04():
    global currentStep
    global finished
    from .loginL2 import text, now  # extracted text
    required16 = cv2.imread("Resources\elvenRuins1.png")
    if findImageByPosition(100, 27, 250, 150, now, required16):
        print('First Dungeon')
        currentStep = 5  # select the dungeon
        return False
    else:
        currentStep = 4  # swipe again
        swipe(320, 129, 320, 655, 0.5)  # swipe to top
        time.sleep(10)


def step05():
    global currentStep
    global finished
    finished = autoDetectDone()
    if finished == 1:
        touch(325, 179)
    elif finished == 2:
        touch(336, 323)
    elif finished == 3:
        touch(325, 457)
    elif finished == 4:
        touch(334, 583)
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
        currentStep = 6
        time.sleep(10)
        return True
    else:
        time.sleep(7)
        currentStep = 4 # back to previous step, and select first dungeon
        return False

# check is complete if not enter dungeon
def autoDetectDone():
    from .loginL2 import now  # extracted text
    global finished
    required16Done = cv2.imread("Resources\Screenshot_20211217-225542.png")
    if(findImageByPosition(127, 453, 593-453, 238-127, now, required16Done)):
        print("Selected Elven Ruins 1 Done")
        return 1
    
    required16Done = cv2.imread("Resources\Screenshot_20211217-225542.png")
    if(findImageByPosition(260, 453, 593-453, 584-260, now, required16Done)):
        print("Selected Elven Ruins 2 Done")
        return 2
    
    return 3

def step06():
    global currentStep
    global finished
    if getAutoClearAll():
        return claimAll()
    elif checkDOungeonCompleted():
        touch(1113, 656)  # enter in dungeon
        time.sleep(5)
        currentStep = 7
    else:
        finished += 1
        currentStep = 5


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


def step08():
    global currentStep
    global finished
    from .loginL2 import text  # extracted text
    if text.find('[Conquest]') > 0:
        startOrClaim(text)
        return False
    elif text.find('[Season]') > 0:
        startOrClaim(text)
        return False
    elif text.find('[Dungeon]') > 0:
        print("This is finished")
        #finished += 1
        #currentStep = 5
    else:
        finished += 1
        currentStep = 5
        touch(861, 88)  # touch in leave
        time.sleep(2)


def startOrClaim(text):
    if text.find('(20/20)') > 0:
        successClaim()
    elif text.find('(30/30)') > 0:
        successClaim()
    elif text.find('(2/2)') > 0:
        successClaim()
    elif text.find('(1/1)') > 0:
        successClaim()
    elif text.find('(40/40)') > 0:
        successClaim()
    else:
        touch(114, 338)  # start quest


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
    from .loginL2 import now  # extracted text
    if now is None:
        time.sleep(7)  # skip to next thread execution
        return 'NO'
    top = 530
    right = 950
    height = 60
    width = 80
    crop_img = now[top: (top + height), right: (right + width)]
    sought = [49, 76, 106]
    imm = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
    result = np.count_nonzero(np.all(imm == sought, axis=2))
    if result > 200:
        return True
    else:
        return False


def getSelectedDungeon():
    from .loginL2 import now  # extracted text
    if checkExist("Resources\dungeon1.png") == True:
        print("Selected Elven Ruins 1")
        return 1
    
    if checkExist("Resources\dungeon2.png") == True:
        print("Selected Elven Ruins 2")
        return 2

    if checkExist("Resources\dungeon3.png") == True:
        print("Selected Ant Nest 1")
        return 3

    if checkExist("Resources\dungeon4.png") == True:
        print("Selected Ant Nest 2")
        return 4

    if checkExist("Resources\dungeon5.png") == True:
        print("Selected Cruma Tower 2F")
        return 5

    print("Elite not found")
    return 0


def getSelectedDungeon2():
    from .loginL2 import now  # extracted text
    if now is None:
        time.sleep(7)  # skip to next thread execution
        return 0
    top = 138
    right = 615
    height = 160
    width = 600
    im = now[top: (top + height), right: (right + width)]
    text = pytesseract.image_to_string(im, lang='eng')
    print(text)
   # print(text)
    if (text.find('Elven Ruins 1') > 0 or text.find('Recommended cP 11,600') > 0 or text.find('Recommended CP 11.600') > 0 or text.find('Recommended CP 11,600') > 0 or text.find('Aplace filled with magic') > 0 or text.find('this is the academy where Elves taught magic') > 0):
        print("Selectd Elven Ruins 1")
        return 1
    if ((text.find('Elven Ruins 2') > 0) or (text.find('Elven Ruins2') > 0) or (text.find('Recommended CP 26.700')) or (text.find('Recommended CP 26,700') > 0) or (text.find('Recommended cP 26,700') > 0)):
        print("Selectd Elven Ruins 2")
        return 2
    if (text.find('Ant Nest 1') > 0 or text.find('Recommended CP 186.500') or text.find('Recommended CP 186,500') > 0 or text.find('Recommended cP 186,500') > 0 or text.find('filled with Giant Ant') > 0 or text.find('created by the gigantic dar') > 0):
        print("Selectd Ant Nest 1")
        return 3
    if (text.find('Ant Nest 2') > 0 or text.find('Recommended CP 407.700') > 0 or text.find('Recommended CP 407,700') > 0 or text.find('Recommended cP 407,700') > 0 or text.find('The ants created an even') > 0 or text.find('complicated maze here to protect their') > 0):
        print("Selectd Ant Nest 2")
        return 4
    if (text.find('Cruma Tower 2F') > 0 or text.find('Recommended CP 650.900') > 0 or text.find('Recommended CP 650,900') > 0 or text.find('Recommended cP 650,900') > 0 or text.find('Amoving fortress and science facility') > 0 or text.find('used by ancient giants') > 0):
        print("Selectd Cruma Tower 2F")
        return 5

    print("Elite not found")
    return 0


def getDoingStatus():
    global DungeonDialogPosition, defaultPosition
    from .loginL2 import now  # extracted text
    if now is None:
        time.sleep(7)  # skip to next thread execution
        return False

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
    from .loginL2 import now  # extracted text
    global finished
    if now is None:
        time.sleep(7)  # skip to next thread execution
        return False

    top = 628
    right = 622
    height = 60
    width = 363
    crop_img = now[top: (top + height), right: (right + width)]
    text = pytesseract.image_to_string(crop_img, lang='eng')
    #print("Text from auto-clear")
    # print(text)
    # print(text.find("Free"))
    #print(text.find("Auto-Clear All"))

    if text.find("Until Free Auto-Clear All") > 0:  # UntilFree Auto-Clear All MM = 1/5
        return False
    elif text.find("Until Free Auto-Clear") > 0:
        return False
    elif text.find("Clear All") > 0 and text.find("Free") <= 0:
        print("CAiu")
        return True
    elif text.find("UntilFree Auto-Clear") > 0:
        return False
    elif text.find("0/5") > 0:
        return False
    elif text.find("1/5") > 0:
        finished = 1
        return False
    elif text.find("2/5") > 0:
        finished = 2
        return False
    elif text.find("3/5") > 0:
        finished = 3
        return False
    elif text.find("4/5") > 0:
        finished = 4
        return False
    elif text.find("5/5") > 0:
        finished = 5
        return True
    elif text.find("6/5") > 0:
        return True
    elif text.find("7/5") > 0:
        return True
    else:
        time.sleep(4)
        return False


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
