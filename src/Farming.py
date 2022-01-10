from .Utils import countPixelsInPosition_NOW, checkExist_NOW, restartL2, liveScreen, swipe, touch, findImage
import cv2
import threading
import time
from .Utils import restart
import numpy as np
import random
import pytesseract
from datetime import date, timedelta, datetime
from .loginL2 import checkStopService, checkExist
import os
farming = 0
elite = 0
blackWindowsError = False
# spot Elite, x, y ( 0 in spot elite is like normal field)
spotLocation = [[32, 527, 206], [32, 510, 256]]
spotFieldLocation = [[488, 295], [493, 203]]
spotWorldDungeonLocation = [[682, 358], [433, 612]]
fieldOrElite = 'WD'  # elite
inExecution = 0
channel = 1
currentStep = 0  # 0 = main screen, 1 = dungeon, 2 normal dungeon, 3 world dungeon or elite, 4 = elite, 5 = farming
lastCheck = datetime.now()
lastDied = datetime.now()
backing = 0
thread = False
EliteDungeonList = ['Elven Ruins 1', 'Elven Ruins 2', 'Ant Nest 1', 'Ant Nest 2', 'Cruma Tower 2F', 'Cruma Tower 3F', 'Ivory Tower Catacomb 1', 'Ivory Tower Catacomb 2', 'Ivory Tower Catacomb 3', 'Ivory Tower Catacomb Laboratory', 'Forest of Secrets Canopy', 'Forest of Secrets Understory', 'Forest of Secrets Slaughter Site', 'Dragon\'s Cave Catacomb 1', 'Dragon\'s Cave Catacomb 2', 'Dragon\'s Cave Catacomb Depths', 'Cave of Trials Catacomb 1', 'Cave of Trials Catacomb 2',
                    'Cave of Trials Catacomb 3', 'Tower of Insolence Catacomb 1', 'Tower of Insolence Catacomb 2', 'Tower of Insolence Catacomb Hall', 'Giant\'s Grave Catacomb 1', 'Giant\'s Grave Catacomb 2', 'Giant\'s Grave Catacomb Depths', 'Sunken Kingdom Upperstory', 'Sunken Kingdom Understory', 'Sunken Kingdom Sanctuary', 'Forsaken Sanctuary Upperstory', 'Forsaken Sanctuary Understory', 'Forsaken Sanctuary Depths', 'Embrion Testing Ground Upper Level', 'Embrion Testing Ground Lower Level']
Decks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
# just load once die sample
die = cv2.imread("Resources\die.png")
inventory = cv2.imread("Resources\Screenshot_20211221-151013.png")
life = cv2.imread("Resources\monster00.png")
now = False
Try = 0
waitToActiveBattleOn = False

def loopFarming():
    global thread
    if thread != False and thread.isAlive():
        thread.cancel()
        thread = False

    thread = threading.Timer(8.0, loopFarming)  # every 7 minutes
    thread.daemon = True
    thread.setName("Farming Thread")
    thread.start()
    doFarming()
    # thread.join()


def doFarming():
    global inExecution, elite, farming
    from .loginL2 import logged
    from .SummoningCircle import finishedSummoningCircle
    from .TempleGuardian import finishedTempleGuardian
    from .EliteQuest import EliteQuestIsDone
    from .DailyDungeon import DailyDungeonIsDone
    from .ScrollQuest import scrollQuestIsDone
    from .TowerOfInsolence import TowerOfInsolenceIsDone

    if not logged or not TowerOfInsolenceIsDone or not finishedTempleGuardian or not scrollQuestIsDone or not DailyDungeonIsDone or not EliteQuestIsDone or not finishedSummoningCircle:
        return False

    global Try, now
    liveScreen()
    if os.path.isfile('now.png') == True:
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
        size = os.path.getsize("now.png")
        print("Size : " + str(size))
        if size < 200:
            print("problem with current screen : " + str(size))

        assert not isinstance(now, type(None)), 'image not found'
        Try = 0
        print("Farming")
        checkStep()


def checkStep():
    detectBlackScreen() # detect black screen error crasher
    if fieldOrElite == 'WD' or fieldOrElite == 'elite':
        detectCurrentStep()

    global currentStep
    print("Farming in "+str(fieldOrElite) +
          " | Checking Steps : " + str(currentStep))
    # I'm not farming go to spot
    if currentStep != 5 and (fieldOrElite == 'WD' or fieldOrElite == 'elite'):
        detectImInDungeon()

    if currentStep == 0:  # Main screen
        print("Step 0")
        step00()
    elif currentStep == 1:  # Touch Dungeon
        print("Step 1")
        step01()
    elif currentStep == 2:  # Touch in Normal Dungeon
        print("Step 2")
        step02()
    elif currentStep == 3:  # Touch in Normal Dungeon
        print("Step 3")
        step03()
    elif currentStep == 4:  # Touch in Normal Dungeon
        print("Step 4")
        step04()
    elif currentStep == 5:  # Farming
        print("Step 5")
        checkDie()


def checkDie():
    global die,currentStep, inventory, lastDied, farming, spotLocation, spotFieldLocation, fieldOrElite, backing, lastCheck
    from .loginL2 import now  # current now
    from .loginL2 import text  # extracted text
    if now is None:
        time.sleep(5)  # skip to next thread execution
        return False

    # if detectImElite() == False:
    #    farming = 0
    #    backing = 1
    #    backToElite()
    current = datetime.now()
    if findImage(now, die) or text.find("illed by") > 0:
        lastDied = datetime.now()
        print("I die back to spot")
        lastCheck = False
        farming = 0
        backing = 1
        revival()
        backToFarm()
        backing = 0
        return True
    else:
        detectImNotInDungeon()
        # Yeah, I'm living
        if smarthDetectImFarming():  # melhorar isso aqui ta errado
            print("I'm farming right now")
            lastCheck = current

        if backing == 0 and findImage(now, inventory) == False:
            if detectMainScreen() and currentStep == 5:
                if waitToActiveBattleOn == False or datetime.timestamp(waitToActiveBattleOn) < datetime.timestamp(current):
                    detectAutoOn()  # is auto ?
        # if backing == 0 :
        #    detectAutoOn() # is auto ?
        print("Last Check")
        print(lastCheck)
        # tem um bug aqui
        # aqui tem que verificar se foi encontrado batendo no alvo
        # se passou 2 minutos e n verificou nada
        # volta para o spot (EVITA os noobs que lura pra fora do spot)
        if lastCheck != False:
            now_plus_2 = lastCheck + timedelta(0, 2 * 60)
            if datetime.timestamp(current) >= datetime.timestamp(now_plus_2):
                lastCheck = current
                backToFarm()
                print("yes")
            else:
                print("no")

        return False


def step02():
    global currentStep, thread, now
    if fieldOrElite == "WD":
        touch(988, 521)  # touch in World Dungeon
        currentStep = 3
    elif fieldOrElite == "elite":
        touch(120, 517)  # touch in Normal Dungeon
        currentStep = 3
    # thread.cancel()


def step03():
    global currentStep, thread, now, fieldOrElite
    # detect first I'm correct screen
    if fieldOrElite == "WD":
        if checkExist_NOW(now, "Resources\Screenshot_20220109-195401.png"):  # todo check pot 100
            # insuficient proof blood (BUG)
            if countPixelsInPosition_NOW(653, 1121, 70, 40, [194, 5, 1], 100, 1000, now, True):
                print("insuficient proof blood, changing to Elite Farm")
                touch(1240, 41)  # tap in Main screen
                fieldOrElite = 'elite'  # change to elite
                currentStep = 0
                return True
            else:
                touch(1013, 666)  # touch in Entry Request
                currentStep = 4
                return True
        else:
            touch(1240, 41)  # I no have Idea, Main screen ?
            currentStep = 0

# step 4 go to spot
def step04():
    global currentStep, fieldOrElite
    if fieldOrElite == "WD":
        if detectImInWorldDungeon():
            print("Go to spot")
            currentStep = 5
            backToFarm()
            return True
        else:
            print("Wait enter in Would Dungeon")
            return False
    else:
        return False


def step00():
    global fieldOrElite, currentStep
    if detectInvalidStep() and fieldOrElite != 'field':
        touch(923, 30)  # touch(235, 400)
    elif fieldOrElite == 'field':
        # verificar se no field e pular para o passo de ir para o spot
        print("Farming Field")


def step01():
    global fieldOrElite
    if fieldOrElite != 'field':
        touch(300, 659)  # touch in dungeon


def revival():
    global fieldOrElite
    print("Back to live")
    touch(637, 480)  # click in OK
    time.sleep(1)
    touch(635, 500)  # click in OK
    time.sleep(1)

    if fieldOrElite == 'WD':  # World Dungeon
        touch(1141, 549)  # tap in spot revival
    else:
        touch(1153, 530)  # tap in spot revival
    time.sleep(5)

    if fieldOrElite == "WD":
        moveToAnyDirection()


def backToFarm():
    global spotLocation, fieldOrElite, spotFieldLocation, spotWorldDungeonLocation, waitToActiveBattleOn
    waitToActiveBattleOn = datetime.now() + timedelta(0, 3 * 60) # wait 3 minutes for active
    # click on map
    touch(1172, 92)
    time.sleep(5)
    # click on spot
    index = 0
    if random.randint(0, 100) < 50:
        index = 0
    else:
        index = 1

    if fieldOrElite == 'elite':
        # 508, 558 # campo 700, 230   #elite 736, 672
        touch(spotLocation[index][1], spotLocation[index][2])
    elif fieldOrElite == 'field':
        # 505, 581 # campo 700, 560   elite  797, 659
        touch(spotFieldLocation[index][0], spotFieldLocation[index][1])
    else:
        # 505, 581 # campo 700, 560   elite  797, 659
        touch(spotWorldDungeonLocation[index][0],
              spotWorldDungeonLocation[index][1])

    # 530 undead  423, 291 | 466, 342
    if fieldOrElite != 'WD':
        time.sleep(35)  # 43
    # set auto
    touch(1089, 850)


def getSelectedDungeon():
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
   # print(text)
    if text.find('Elven Ruins 1') > 0 or text.find('Recommended cP 11,600') > 0 or text.find('Recommended CP 11,600') > 0 or text.find('Aplace filled with magic') > 0 or text.find('this is the academy where Elves taught magic') > 0:
        return 1
    elif text.find('Elven Ruins 2') > 0 or text.find('Recommended CP 26,700') > 0 or text.find('Recommended cP 26,700') > 0 or text.find('When the Elves ruled the') > 0 or text.find('exceptional talent') > 0:
        return 2
    elif text.find('Ant Nest 1') > 0 or text.find('Recommended CP 186,500') > 0 or text.find('Recommended cP 186,500') > 0 or text.find('filled with Giant Ant') > 0 or text.find('created by the gigantic dar') > 0:
        return 3
    elif text.find('Ant Nest 2') > 0 or text.find('Recommended CP 407,700') > 0 or text.find('Recommended cP 407,700') > 0 or text.find('The ants created an even') > 0 or text.find('complicated maze here to protect their') > 0:
        return 4
    elif text.find('Cruma Tower 2F') > 0 or text.find('Recommended CP 650,900') > 0 or text.find('Recommended cP 650,900') > 0 or text.find('Amoving fortress and science facility') > 0 or text.find('used by ancient giants') > 0:
        return 5
    elif text.find('Embrion Tower 2F') > 0 or text.find('Recommended CP 650,900') > 0 or text.find('Recommended cP 650,900') > 0 or text.find('Amoving fortress and science facility') > 0 or text.find('used by ancient giants') > 0:
        return 32
    else:
        print("Elite not found")
        return 0


def backToElite():
    from .loginL2 import text  # extracted text
    # ainda tem bug aqui sempre deixa passar algo add mais validacoes
    print("Back to elite")


def detectImElite():
    from .loginL2 import text  # extracted text
    if text.find('Bonus Points') > 0:
        return True
    elif text.find('Points Expired') > 0:
        return True
    elif text.find('[Conquest]') > 0:
        return True
    elif text.find('[Conquest') > 0:
        return True
    elif text.find('Conquest]') > 0:
        return True
    elif text.find('(/300)]') > 0:
        return True
    elif text.find('ON/ OFF') > 0:
        return True
    else:
        return False


def detectAutoOn():
    from .loginL2 import now  # now
    if now is None:
        time.sleep(5)  # skip to next thread execution
        return False
    top = 653
    right = 843
    height = 58
    width = 60
    crop_img = now[top: (top + height), right: (right + width)]
    sought = [250, 255, 255]
    imm = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
    result = np.count_nonzero(np.all(imm == sought, axis=2))
    print("Auto : " + str(result))
    if result >= 3:
        print("Auto On")
    else:
        touch(873, 681)
        time.sleep(10)
        print("Auto Off")


def moveToAnyDirection():
    swipe(148, 568, 199, 568, 2.5)  # swipe to top
    time.sleep(3)


def smarthDetectImFarming():
    # from .loginL2 import now, text  # extracted text
    global fieldOrElite, life, now
    if fieldOrElite == "WD" and detectMainScreen() and countPixelsInPosition_NOW(67, 506, 250, 20, [184, 15, 15], 100, 10000, now, True):
        print("Farming in World Dungeon")
        return True
    # elif fieldOrElite == "WD" and (checkExist("Resources\monster0.png") or text.find('World Dungeon') > 0 or text.find('Berserker') > 0 or text.find('Berse') > 0  or text.find('Manipulated') > 0 or text.find("Manipula") > 0 or text.find("Manimilate") > 0 or text.find("erker") > 0 or text.find("Manipul") > 0) :
    #    print("Farming in World Dungeon")
    #    return True

    if checkExist_NOW(now, "Resources\monster1.png"):
        print("Farming in Magic Monster")
        return True
    elif checkExist_NOW(now, "Resources\monster2.png"):
        print("Farming in Undead Monster")
        return True
    else:
        return False


def detectImNotInDungeon():
    global currentStep, now
    if countPixelsInPosition_NOW(137, 1102, 25, 40, [73, 78, 75], 1, 100, now):
        print("I'm not World Dungeon")
        currentStep = 0
    elif countPixelsInPosition_NOW(137, 1102, 25, 40, [199, 199, 198], 1, 100, now):
        print("I'm not World Dungeon")
        currentStep = 0


def detectImInDungeon():
    global currentStep, now
    print("Detecting I'm in World Dungeon")
    if countPixelsInPosition_NOW(137, 1102, 25, 40, [73, 78, 75], 1, 100, now):
        print("I'm not World Dungeon")
        currentStep = 0
    elif countPixelsInPosition_NOW(137, 1102, 25, 40, [199, 199, 198], 1, 100, now):
        print("I'm not in World Dungeon²")
        currentStep = 0

def detectImInWorldDungeon():
    if detectMainScreen() and countPixelsInPosition_NOW(137, 1102, 25, 40, [73, 78, 75], 1, 100, now):
        return False
    elif detectMainScreen() and countPixelsInPosition_NOW(137, 1102, 25, 40, [199, 199, 198], 1, 100, now):
        return False
    else:
        return True

def detectInvalidStep():
    global currentStep
    if detectMainScreen():  # todo check pot 100
        print("Invalid Step")
        currentStep = 0
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


def detectCurrentStep():
    from .loginL2 import text  # extracted text
    global now, currentStep
    if countPixelsInPosition_NOW(500, 103, 45, 20, [210, 210, 210], 1, 30, now) and countPixelsInPosition_NOW(500, 277, 45, 45, [210, 210, 210], 1, 30, now):
        currentStep = 2
        return True
    elif countPixelsInPosition_NOW(500, 103, 45, 20, [209, 209, 210], 1, 30, now) and countPixelsInPosition_NOW(500, 277, 45, 45, [209, 209, 210], 1, 30, now):
        currentStep = 2
        return True
    elif countPixelsInPosition_NOW(635, 451, 40, 50, [210, 210, 210], 1, 30, now) and countPixelsInPosition_NOW(655, 277, 45, 20, [210, 210, 210], 1, 30, now):
        currentStep = 1
        return True
    elif countPixelsInPosition_NOW(635, 451, 40, 50, [209, 209, 210], 1, 30, now) and countPixelsInPosition_NOW(655, 277, 45, 20, [209, 209, 210], 1, 30, now):
        currentStep = 1
        return True
    elif currentStep != 0 and currentStep != 5 and detectInvalidStep():
        currentStep = 0
        return True
    elif detectImInWorldDungeon() and currentStep != 5:
        currentStep = 5
        return True
    # check is store screen
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

# sometimes the game frezen in a black screen
def detectBlackScreen():
    global now, blackWindowsError
    print("Checking Erro Black Screen")
    if countPixelsInPosition_NOW(0, 0, 1280, 720, [0, 0, 0], 900000, 931600, now,True):
        if blackWindowsError != False:
            if datetime.timestamp(blackWindowsError) < datetime.timestamp(datetime.now()):
                print("Error Black Screen, Restarting Emulator....")
                from .loginL2 import logged
                logged = False
                restartL2()
                blackWindowsError = False
                return True
            else:
                print("Black Screen detected, maybe it's nothing")
                #blackWindowsError = datetime.now() + timedelta(0, 1 * 60) # wait 1 minute for restart emulator
                return True
        else:
            blackWindowsError = datetime.now() + timedelta(0, 1 * 60) # wait 1 minute for restart emulator
            return True
    else:
        print("No Erro Black Screen detected")
        blackWindowsError = False
        return False
