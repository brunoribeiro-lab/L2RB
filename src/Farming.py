from .Utils import findImageByPosition, checkProcessExist,killProcess, countPixelsInPosition_NOW, checkExist_NOW, restartL2, liveScreen, swipe, touch, findImage
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
spotLocation = [[32, 527, 239], [32, 563,290], [32, 382,382]]
spotFieldLocation = [[444, 632], [405, 401]]
spotWorldDungeonLocation =  [[453, 404], [682, 358]] # [[682, 358], [474, 377]]
fieldOrElite = 'WD'  # elite
inExecution = 0
channel = 1
currentStep = 0  # 0 = main screen, 1 = dungeon, 2 normal dungeon, 3 world dungeon or elite, 4 = elite, 5 = farming
lastCheck = datetime.now()
lastDied = datetime.now()
lastFieldSpot = datetime.now()
backing = 0
thread = False
EliteDungeonList = ['Elven Ruins 1', 'Elven Ruins 2', 'Ant Nest 1', 'Ant Nest 2', 'Cruma Tower 2F', 'Cruma Tower 3F', 'Ivory Tower Catacomb 1', 'Ivory Tower Catacomb 2', 'Ivory Tower Catacomb 3', 'Ivory Tower Catacomb Laboratory', 'Forest of Secrets Canopy', 'Forest of Secrets Understory', 'Forest of Secrets Slaughter Site', 'Dragon\'s Cave Catacomb 1', 'Dragon\'s Cave Catacomb 2', 'Dragon\'s Cave Catacomb Depths', 'Cave of Trials Catacomb 1', 'Cave of Trials Catacomb 2',
                    'Cave of Trials Catacomb 3', 'Tower of Insolence Catacomb 1', 'Tower of Insolence Catacomb 2', 'Tower of Insolence Catacomb Hall', 'Giant\'s Grave Catacomb 1', 'Giant\'s Grave Catacomb 2', 'Giant\'s Grave Catacomb Depths', 'Sunken Kingdom Upperstory', 'Sunken Kingdom Understory', 'Sunken Kingdom Sanctuary', 'Forsaken Sanctuary Upperstory', 'Forsaken Sanctuary Understory', 'Forsaken Sanctuary Depths', 'Embrion Testing Ground Upper Level', 'Embrion Testing Ground Lower Level']
Decks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
# just load once die sample
die = cv2.imread("Resources\die.png")
inventory = cv2.imread("Resources\Screenshot_20211221-151013.png")
life = cv2.imread("Resources\monster00.png")
store = cv2.imread("Resources\Screenshot_20220111-002625.png")
shopOpened = cv2.imread("Resources\Screenshot_20220111-002625.png")
shopOpened2 = cv2.imread("Resources\Screenshot_20220111-021906.png")
worldDungeonScreen = cv2.imread("Resources\Screenshot_20220109-195401.png")
mapOpened = cv2.imread("Resources\Screenshot_20220111-020752.png")
eliteResource = cv2.imread("Resources\Screenshot_20220228-184657.png")
elite2Resource = cv2.imread("Resources\Screenshot_20220228-190211.png")
elite3Resource = cv2.imread("Resources\Screenshot_20220228-190930.png")
elite4Resource = cv2.imread("Resources\Screenshot_20220228-203657.png")
now = False
Try = 0
waitToActiveBattleOn = False


def loopFarming():
    global thread
    if thread != False and thread.isAlive():
        thread.join()

    thread = threading.Timer(8.0, doFarming)  # every 7 minutes
    thread.daemon = True
    thread.setName("Farming Thread")
    thread.start()
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
    print("****************** Farming THREAD ************************")
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
    print("********************************************************")


def checkStep():
    # talvez aqui resolva o problema de travamento em telas
    # se houver uma diferenca de 1m com a data atual reinicia com a funcao restart()
    detectInvalidScreen()  # detect black screen error crasher
    if fieldOrElite == 'WD' or fieldOrElite == 'elite':
        detectCurrentStep()

    global currentStep
    print("Farming in "+str(fieldOrElite) +
          " | Checking Steps : " + str(currentStep))

    if currentStep == 0:  # Main screen
        print("Step 0")
        if fieldOrElite != 'field':
            step00()
        else:
            checkDie()
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
    global die, currentStep, lastFieldSpot, inventory, lastDied, farming, spotLocation, spotFieldLocation, fieldOrElite, backing, lastCheck
    from .loginL2 import now  # current now
    from .loginL2 import text  # extracted text
    if now is None:
        return False
    
    assert not isinstance(now, type(None)), 'image not found'
    # if detectImElite() == False:
    #    farming = 0
    #    backing = 1
    #    backToElite()
    current = datetime.now()
    if findImage(now, die):
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
        # detectImNotInDungeon()
        # Yeah, I'm living
        if smarthDetectImFarming():  # melhorar isso aqui ta errado
            print("I'm farming right now")
            lastFieldSpot = current
            lastCheck = current

        # vai da merda
        if fieldOrElite == 'field' and lastFieldSpot != False:
            #lastFieldSpot = current
            now_plus = lastFieldSpot + timedelta(0, 1 * 60)
            if datetime.timestamp(now_plus) < datetime.timestamp(current):
                print("waited 1 minute, auto on")
                detectAutoOn()  # is auto ?
                
                    
        if backing == 0 and findImage(now, inventory) == False:
            if detectMainScreen() and currentStep == 5:
                if waitToActiveBattleOn == False or datetime.timestamp(waitToActiveBattleOn) < datetime.timestamp(current):
                    print("shoud be here")
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
                if fieldOrElite == 'field':
                    lastFieldSpot = current
                backToFarm()
                print("yes")
            else:
                print("no")

        return False

def step01():
    global fieldOrElite, currentStep, now
    if fieldOrElite != 'field':
        if detectMenuIsOpened() :
            print("Touch in Dungeon")
            touch(300, 659)  # touch in dungeon
            time.sleep(2)
            liveScreen()
            time.sleep(2)
            if os.path.isfile('now.png') == True:
                now = cv2.imread("now.png")
            #currentStep = 2
        else:
            print("aqui deveria da merda 6431")
            
def step02():
    global currentStep, thread, now
    if fieldOrElite == "WD":
        if detectDungeonMenuIsOpened():
            print("Touch in World Dungeon")
            touch(1000, 521)  # touch in World Dungeon
            time.sleep(2)
            liveScreen()
            time.sleep(2)
            if os.path.isfile('now.png') == True:
                now = cv2.imread("now.png")
            #currentStep = 3
        else:
            print("Aqui deveria da merda 314")
    elif fieldOrElite == "elite":
        touch(278, 524)  # touch in Normal Dungeon
        currentStep = 3
        time.sleep(3)
        liveScreen()
        time.sleep(2)
        if os.path.isfile('now.png') == True:
            now = cv2.imread("now.png")
    # thread.cancel()


def step03():
    global currentStep, thread, now,eliteResource, fieldOrElite
    # detect first I'm correct screen
    if fieldOrElite == "WD":
        if checkExist_NOW(now, "Resources\Screenshot_20220109-195401.png"):  # todo check pot 100
            # insuficient proof blood (BUG)
            if countPixelsInPosition_NOW(653, 1121, 70, 40, [194, 5, 1], 100, 1000, now, True):
                print("insuficient proof blood, changing to Elite Farm")
                touch(1240, 41)  # tap in Main screen
                fieldOrElite = 'elite'  # change to elite
                currentStep = 0  # just choice the spot
                return True
            else:
                touch(1013, 666)  # touch in Entry Request
                currentStep = 4
                liveScreen()
                time.sleep(2)
                if os.path.isfile('now.png') == True:
                    now = cv2.imread("now.png")
                return True
        else:
            touch(1240, 41)  # I no have Idea, Main screen ?
            time.sleep(1)
            fieldOrElite = 'field'  # change to elite
            currentStep = 4  # just choice the spot
    if fieldOrElite == "elite":
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
            swipe(320, 655, 320, 455, 0.5)  # swipe a little bit to down
            time.sleep(4)
            liveScreen()
            time.sleep(2)
            if os.path.isfile('now.png') == True:
                now = cv2.imread("now.png")

# step 4 go to spot

def step04():
    global currentStep, fieldOrElite, elite3Resource,elite4Resource, now
    if fieldOrElite == "WD":
        if ImWorldDungeon():
            print("Go to spot")
            currentStep = 5
            moveToAnyDirection()
            time.sleep(2)
            backToFarm()
            return True
        else:
            print("Wait enter in Would Dungeon")
            return False
    elif fieldOrElite == "field":
        print("Go to spot")
        currentStep = 5
        backToFarm()
        return True
    elif fieldOrElite == "elite":
        if findImageByPosition(535,33,580,150, now, elite3Resource) or findImageByPosition(535,33,580,150, now, elite4Resource):
            print("Tap in Embrion Testing Grgound Restricted Area")
            touch(335,610)
            time.sleep(2)
            touch(1109,659)
            currentStep = 5  # just choice the spot
            time.sleep(2)
            liveScreen()
            time.sleep(2)
            if os.path.isfile('now.png') == True:
                now = cv2.imread("now.png")
            time.sleep(3)
            backToFarm()
        else:
            swipe(320, 655, 320, 455, 0.5)  # swipe to down
            currentStep = 4
        return False


def step00():
    global fieldOrElite, currentStep, now
    if fieldOrElite != 'field' and detectMainScreen():
        print("Touch in Menu")
        touch(923, 30)  # Touch in menu
        # evita clicks invalidos
        time.sleep(2)
        liveScreen()
        time.sleep(2)
        if os.path.isfile('now.png') == True:
            now = cv2.imread("now.png")
    elif fieldOrElite == 'field':
        # verificar se no field e pular para o passo de ir para o spot
        print("Farming Field")





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
    waitToActiveBattleOn = datetime.now() + timedelta(0, 3 *
                                                      60)  # wait 3 minutes for active
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
    
    if fieldOrElite == "field" and detectMainScreen() and countPixelsInPosition_NOW(67, 506, 250, 20, [184, 15, 15], 100, 10000, now, True):
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


def ImWorldDungeon():
    global currentStep, now
    print("Detecting I'm in World Dungeon")
    # black ton
    if detectMainScreen() and countPixelsInPosition_NOW(142, 1102, 21, 27, [185, 186, 186], 1, 100, now, True):
        print("I'm not World Dungeon")
        return False
    # gray ton
    elif detectMainScreen() and countPixelsInPosition_NOW(142, 1102, 21, 27, [190, 191, 192], 1, 100, now, True):
        print("I'm not in World Dungeon²")
        return False
    else:
        return True

def ImEliteDungeon():
    global currentStep, now
    print("Detecting I'm in World Dungeon")
    # black ton
    if detectMainScreen() and countPixelsInPosition_NOW(157, 1165, 30, 25, [176, 177, 178], 1, 100, now, True):
        print("I'm Elite Dungeon")
        return True
    # gray ton
    elif detectMainScreen() and countPixelsInPosition_NOW(157, 1165, 30, 25, [190, 191, 192], 1, 100, now, True):
        print("I'm Elite Dungeon²")
        return True
    elif not detectMainScreen():
        return True
    else:
        return False
    
def detectImInWorldDungeon():
    if detectMainScreen() and countPixelsInPosition_NOW(137, 1102, 25, 40, [73, 78, 75], 1, 100, now, True):
        return False
    elif detectMainScreen() and countPixelsInPosition_NOW(137, 1102, 25, 40, [199, 199, 198], 1, 100, now, True):
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
    global now, currentStep, store, fieldOrElite, shopOpened, shopOpened2, eliteResource
    if detectDungeonMenuIsOpened():
        #currentStep = 2
        return True
    elif fieldOrElite == 'elite' and findImageByPosition(167,543,320,515,now, eliteResource):
        print("Elite Dungeon Menu")
        currentStep = 3
        return True
    elif countPixelsInPosition_NOW(605,234,130,55,[129, 236, 255], 1, 50, now) or countPixelsInPosition_NOW(605,234,130,55,[178,200,228], 1, 50, now) or countPixelsInPosition_NOW(605,234,130,55,[128,233,255], 1, 50, now):
        currentStep = 2
        print("Selected Dungeon")
        return True
    elif fieldOrElite == 'elite' and currentStep != 4 and findImageByPosition(320,1099,160,78,now, elite2Resource):
        print("Elite Dungeon Menu Selector")
        currentStep = 4   
        return True
    elif detectMenuIsOpened() and currentStep != 2:
        print("Auto detect menu")
        return True
    elif currentStep == 5 and fieldOrElite == 'WD' and not ImWorldDungeon():
        currentStep = 0
        return True
    elif currentStep == 5 and fieldOrElite == 'elite' and not ImEliteDungeon():
        currentStep = 0
        return True
    elif (currentStep != 5) and (currentStep != 2) and (currentStep != 3)  and (currentStep != 4) and fieldOrElite == 'elite' and ImEliteDungeon():
        print("..")
        currentStep = 5
        return True
    elif (currentStep != 5) and (currentStep != 2) and (currentStep != 3)  and (currentStep != 4) and fieldOrElite == 'WD' and ImWorldDungeon():
        print("..")
        currentStep = 5
        return True
    elif currentStep != 0 and currentStep != 5 and currentStep != 4 and detectInvalidStep():
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
    elif findImage(now, worldDungeonScreen) and currentStep != 3:
        print("Invalid Screen, World Dungeon, Backing to Main Screen")
        currentStep = 3
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

# sometimes the game frezen in a black screen


def detectInvalidScreen():
    global now, mapOpened
    # check map is opened for any reason
    if countPixelsInPosition_NOW(660, 1015, 200, 50, [52, 83, 112], 300, 1000, now):
        print("Closing Map")
        touch(1243, 38)  # touch in back
        return True
    # check tower of isonece 
    # darly quest

def detectDungeonMenuIsOpened():
    global now, currentStep
    print("Detecting dungeon menu is opened")
    # World Raid icon
    if countPixelsInPosition_NOW(510,990,10,20,[195,196,197], 1, 100, now, True):
        currentStep = 2
        print("World Raid Icon")
        return True
    
    # normal dungeon icon
    if countPixelsInPosition_NOW(510,264,30,20,[195,196,197], 1, 100, now, True):
        currentStep = 2
        print("Normal Dungeon Icon")
        return True
    
    # Temporal Rift icon
    if countPixelsInPosition_NOW(513,412,30,20,[195,196,197], 1, 100, now, True):
        currentStep = 2
        print("Temporal Rift Icon")
        return True
    
    if countPixelsInPosition_NOW(510,990,10,20,[187,187,187], 1, 100, now, True):
        currentStep = 2
        print("World Raid Icon2")
        return True
    
    # normal dungeon icon
    if countPixelsInPosition_NOW(510,264,30,20,[187,187,187], 1, 100, now, True):
        currentStep = 2
        print("Normal Dungeon Icon2")
        return True
    
    # Temporal Rift icon
    if countPixelsInPosition_NOW(513,412,30,20,[187,187,187], 1, 100, now, True):
        currentStep = 2
        print("Temporal Rift Icon2")
        return True
    
    return False

def detectMenuIsOpened():
    global now, currentStep
    # Rankig icon
    print("Detecting menu is opened")
    if countPixelsInPosition_NOW(645,1053,30,20,[187,187,187], 1, 50, now, True):
        currentStep = 1
        print("Rankig Icon")
        return True
    
    # Trading Post icon
    if countPixelsInPosition_NOW(650,928,45,35,[187,187,187], 1, 50, now, True):
        currentStep = 1
        print("Trading Post Icon")
        return True
    
    # Friends icon
    if countPixelsInPosition_NOW(630,774,40,35,[187,187,187], 1, 50, now, True):
        currentStep = 1
        print("Friends Icon")
        return True
    
    return False