from .Utils import countPixelsInPosition, liveScreen, swipe, touch, findImage
import cv2
import threading
import time
from .Utils import restart
import numpy as np
import random
import pytesseract
from datetime import date, timedelta, datetime
from .loginL2 import checkStopService, checkExist
farming = 0
elite = 0
# spot Elite, x, y ( 0 in spot elite is like normal field)
spotLocation = [[32, 527, 206], [32, 510, 256]]
spotFieldLocation = [[ 488, 295], [ 493, 203]]
spotWorldDungeonLocation = [[682, 358], [433, 612]]
fieldOrElite = 'WD' # elite
inExecution = 0
channel = 1
currentStep = 0 # 0 = not dungeon, 1 enter 
lastCheck = datetime.now()
lastDied = datetime.now()
backing = 0
thread = False
EliteDungeonList = ['Elven Ruins 1','Elven Ruins 2','Ant Nest 1','Ant Nest 2','Cruma Tower 2F','Cruma Tower 3F','Ivory Tower Catacomb 1','Ivory Tower Catacomb 2','Ivory Tower Catacomb 3','Ivory Tower Catacomb Laboratory','Forest of Secrets Canopy', 'Forest of Secrets Understory','Forest of Secrets Slaughter Site','Dragon\'s Cave Catacomb 1','Dragon\'s Cave Catacomb 2' ,'Dragon\'s Cave Catacomb Depths','Cave of Trials Catacomb 1','Cave of Trials Catacomb 2','Cave of Trials Catacomb 3','Tower of Insolence Catacomb 1','Tower of Insolence Catacomb 2','Tower of Insolence Catacomb Hall', 'Giant\'s Grave Catacomb 1','Giant\'s Grave Catacomb 2','Giant\'s Grave Catacomb Depths','Sunken Kingdom Upperstory','Sunken Kingdom Understory','Sunken Kingdom Sanctuary','Forsaken Sanctuary Upperstory','Forsaken Sanctuary Understory','Forsaken Sanctuary Depths','Embrion Testing Ground Upper Level','Embrion Testing Ground Lower Level']
Decks = ['1','2','3','4','5','6','7','8','9','10']
# just load once die sample
die = cv2.imread("Resources\die.png")
inventory = cv2.imread("Resources\Screenshot_20211221-151013.png")
life = cv2.imread("Resources\monster00.png")

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
    #thread.join()


def doFarming():
    global inExecution, elite, farming
    from .loginL2 import logged
    from .SummoningCircle import finishedSummoningCircle
    from .TempleGuardian import finishedTempleGuardian
    from .EliteQuest import EliteQuestIsDone
    from .DailyDungeon import DailyDungeonIsDone
    from .ScrollQuest import scrollQuestIsDone
    from .TowerOfInsolence import TowerOfInsolenceIsDone
    
    if logged == 0:
        return False

    if TowerOfInsolenceIsDone == 0:
        return False
    
    if finishedTempleGuardian == 0:
        return False
    
    if scrollQuestIsDone  == 0:
        return False
    
    if DailyDungeonIsDone == 0:
        return False

    if EliteQuestIsDone == 0:
        return False
    
    if finishedSummoningCircle == 0:
        return False

    if inExecution == 0:
        inExecution = 1
        checkStopService()
        print("Farming")
        checkStep()
        #checkDie()
        inExecution = 0

def checkStep():
    global currentStep
    print("Farming : Checking Steps")
    if currentStep != 3:
        detectImInDungeon()
    
    if currentStep == 0:  # Main screen
        print("Step 0")
        step00()
    elif currentStep == 1: # Touch Dungeon
        print("Step 1")
        detectInvalidStep()
        step01()
    elif currentStep == 2: # Touch in Normal Dungeon
        print("Step 2")
        detectInvalidStep()
        step02()
    elif currentStep == 3:  # Farming
        print("Step 3")
        checkDie()
        
def checkDie():
    global die, inventory ,lastDied ,farming, spotLocation, spotFieldLocation, fieldOrElite, backing, lastCheck
    from .loginL2 import now  # current now
    from .loginL2 import text  # extracted text
    if now is None:
        time.sleep(5)  # skip to next thread execution
        return False
    
    #if detectImElite() == False:
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
        if smarthDetectImFarming() : # melhorar isso aqui ta errado
            print("I'm farming right now")
            lastCheck = current

        if backing == 0 and  findImage(now, inventory) == False:
            if detectMainScreen():
                detectAutoOn() # is auto ?
        #if backing == 0 :
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
    global currentStep, thread
    if countPixelsInPosition(633,849,305,60,[42,91,61], 1000, 100000):
        touch(1028, 673)  # touch in Entry Request
        currentStep = 3
        #thread.cancel()
    
    
def step00():
    global currentStep
    touch(923, 30)  # touch(235, 400)
    from .loginL2 import text  # extracted text
    if text.find('Dungeon'):
        touch(300, 659)  # touch in dungeon
        time.sleep(1)
        liveScreen()
        time.sleep(3)
        currentStep = 1  # run to NPC


def step01():
    global currentStep, thread
    from .loginL2 import text  # extracted text
    if text.find('Normal Dungeon') or text.find('Temporal Rift'):
        currentStep = 2  # run to NPC
        touch(988, 517)  # touch in World Dungeon
        time.sleep(1)
        liveScreen()
        time.sleep(3)
        #thread.cancel()

def revival():
    global fieldOrElite
    print("Back to live")
    touch(637, 480)  # click in OK
    time.sleep(1)
    touch(635, 500)  # click in OK
    time.sleep(1)
    
    if fieldOrElite == 'WD': # World Dungeon
        touch(1141, 549)  # tap in spot revival
    else:
        touch(1153, 530)  # tap in spot revival
    time.sleep(5)
    
    if fieldOrElite == "WD":
        moveToAnyDirection()

def backToFarm():
    global spotLocation,fieldOrElite, spotFieldLocation, spotWorldDungeonLocation
    # click on map
    touch(1172, 92)
    time.sleep(5)
    # click on spot
    index = 0
    if random.randint(0, 100) < 50:
        index = 0
    else:
        index = 1
        
    if fieldOrElite == 'elite' :
        touch(spotLocation[index][1], spotLocation[index][2])  # 508, 558 # campo 700, 230   #elite 736, 672
    elif fieldOrElite == 'field':
        touch(spotFieldLocation[index][0], spotFieldLocation[index][1])  # 505, 581 # campo 700, 560   elite  797, 659
    else :
        touch(spotWorldDungeonLocation[index][0], spotWorldDungeonLocation[index][1])  # 505, 581 # campo 700, 560   elite  797, 659
        
    # 530 undead  423, 291 | 466, 342
    if fieldOrElite != 'WD' :
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
    crop_img = now[top : (top + height) , right: (right + width)]
    sought = [250,255,255]
    imm = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
    result = np.count_nonzero(np.all(imm==sought,axis=2))
    print("Auto : " + str(result))
    if result >= 3 : 
        print("Auto On")
    else:
        touch(873,681)
        time.sleep(10)
        print("Auto Off")

def moveToAnyDirection():
    swipe(148, 568, 199, 568, 2.5)  # swipe to top
    time.sleep(3)

def smarthDetectImFarming():
    from .loginL2 import now, text  # extracted text
    global fieldOrElite, life

    if fieldOrElite == "WD" and detectMainScreen() and countPixelsInPosition(67, 506, 250,20,[184, 15, 15], 100, 10000, True):
        print("Farming in World Dungeon")
        return True
    #elif fieldOrElite == "WD" and (checkExist("Resources\monster0.png") or text.find('World Dungeon') > 0 or text.find('Berserker') > 0 or text.find('Berse') > 0  or text.find('Manipulated') > 0 or text.find("Manipula") > 0 or text.find("Manimilate") > 0 or text.find("erker") > 0 or text.find("Manipul") > 0) : 
    #    print("Farming in World Dungeon")
    #    return True
    if fieldOrElite == "WD" :
        print(text)
    
    if checkExist("Resources\monster1.png") : 
        print("Farming in Magic Monster")
        return True
    elif checkExist("Resources\monster2.png") : 
        print("Farming in Undead Monster")
        return True
    elif text.find('Undead') > 0 or text.find('undead') > 0 :
        return True
    elif text.find('(Elite)') > 0 or text.find('Elite') > 0 or text.find('elite') > 0:
        return True
    elif text.find('(Demon)') > 0 or text.find('Demon') > 0 or text.find('demon') > 0 :
        return True
    elif text.find('(Magic)') > 0:
        return True
    elif text.find('(Human)') > 0:
        return True
    elif text.find('(Normal)') > 0:
        return True
    else:
        return False
    
def detectImNotInDungeon():
    global currentStep
    if countPixelsInPosition(137,1102,25,40,[73,78,75], 1, 100):
        print("Leave from World Dungeon")
        currentStep = 0
    elif countPixelsInPosition(137,1102,25,40,[199, 199, 198], 1, 100):
        print("Leave from World Dungeon")
        currentStep = 0
  
def detectImInDungeon():
    global currentStep
    if not countPixelsInPosition(137,1102,25,40,[73,78,75], 1, 100):
        print("Leave from World Dungeon")
        currentStep = 3
    elif not countPixelsInPosition(137,1102,25,40,[199, 199, 198], 1, 100):
        print("Leave from World Dungeon")
        currentStep = 3
        
def detectInvalidStep():
    global currentStep
    if detectMainScreen(): # todo check pot 100
        print("Invalid Step")
        currentStep = 0
        return True
    return False
    
def detectMainScreen():
    if checkExist("Resources\pot.png"): # todo check pot 100
        return True
    elif checkExist("Resources\pot2.png"): # todo check pot 100
        return True
    elif checkExist("Resources\pot3.png"):  # offline mode
        return True
    elif checkExist("Resources\pot4.png"):  # offline mode
        return True
    elif checkExist("Resources\pot5.png"):  # offline mode
        return True
    elif checkExist("Resources\pot6.png"):  # offline mode
        return True
  