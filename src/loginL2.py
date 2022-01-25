from .Utils import liveScreen,killL2Process, restartL2, touch,countPixelsInPosition_NOW, countPixelsInPosition, emulators, currentEmulator
from .Utils import findImage
from .Utils import find_matches
from .Utils import restart
from .Utils import process_exists
from .Utils import extractText
import subprocess
import threading
import multiprocessing
from threading import Thread
import cv2
import numpy as np
import os
import time
import re
from datetime import date, timedelta, datetime
logged = 1
loggedStep = 0
threadLogin = False
ThreadProcess = False
executing = False
now = False
text = '' # text extracted 
Try = 0
attempt = 0
# BUGS/IMPROVEMENTS
# 1. Fazer validacao se n logou em 10m reabre o emulador e faz td novamente (evita bugs)
# 2. Fechar a porra do ads do LD player qndo inicia o emulador
# 3. Selecionar cha de algum lugar dinamico
# 4. Ainda da pra deixar mais rapido
# 5. Adicionar Pan's Special Auto-Clear
lauch = cv2.imread("Resources\lauch.png")
lauch2 = cv2.imread("Resources\lauch2.png")
banner_find = cv2.imread("Resources\closeBanner1.png")
banner_find2 = cv2.imread("Resources\closeBanner2.png")
crashed = cv2.imread("Resources\crasher.png")
pot1 = cv2.imread("Resources\pot.png")
pot2 = cv2.imread("Resources\pot2.png")
pot3 = cv2.imread("Resources\pot3.png")
pot4 = cv2.imread("Resources\pot4.png")
pot5 = cv2.imread("Resources\pot5.png")
pot6 = cv2.imread("Resources\pot6.png")
offline1 = cv2.imread("Resources\clock.png")
loaded = cv2.imread("Resources\loaded.png")
lastConfirmedLogged = datetime.now()
lastStep2Invalid = False # prevent long time (probability frozen)

# find icon positions and save in RAM
iconPositionX= False
iconPositionY = False

jumps = 3
jumpsC = 0
def checkLogged():
    global logged
    return logged

def loopLoggin():
    global threadLogin
    if threadLogin != False and threadLogin.isAlive():
        threadLogin.cancel()
        threadLogin.join()
      
    threadLogin = threading.Timer(8.0, mainThread)
    threadLogin.daemon = True # stop if the program exits
    threadLogin.start()

def mainThread():
    global  logged, Try, now, jumpsC , jumpsC
    if not process_exists(emulators[currentEmulator][0]):
        print("Emulator not running, starting : " + emulators[currentEmulator][1])
        logged = 0
        try:
            subprocess.Popen([emulators[currentEmulator][1],emulators[currentEmulator][2]])
            time.sleep(10)
        except WindowsError:
            print("Cant Start " + emulators[currentEmulator][1])
            # [Error 22] No application is associated with the specified
            # file for this operation: '<URL>'
            return False
    else:
        liveScreen()
        if os.path.isfile('./now.png') == True:
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
            print("Size : " + str(size))
            #channels = now.shape[2] resolution
            if size < 200:
                print("problem with current screen : " + str(size))
                
            assert not isinstance(now, type(None)), 'image not found'
            Try = 0
            doLogin()

# check playstore service has stopped and touch tap
def checkStopService():
    global text
    if now is None:
        print("Erro to get now in checking l2 crasher")
        return False
    
    if text.find("has stopped") > 0:
        print("has stopped")
        touch(556, 387)  # tap in  Open app again
        time.sleep(1)
        touch(556, 387)  # tap in  Open app again
        return False
    elif text.find("keeps stopping") > 0:
        print("keeps stopping")
        touch(556, 387)  # tap in  Open app again
        time.sleep(1)
        touch(556, 387)  # tap in  Open app again
        return False
    elif checkExist("Resources\crash.png"):
        print("has stopped")
        touch(556, 387)  # tap in  Open app again
        time.sleep(1)
        touch(556, 387)  # tap in  Open app again
        return False


def doLogin():
    global now, text, loggedStep, logged, executing, text, attempt
    print("================== LOGIN THREAD ========================")
    #text = ''
    text = extractText(now) # esse talvez seja o problema de high RAM
    checkisLogged()  # necessario para que o L2 feche por algum motivo
    if logged == 0:
        checkSteps()
    print("================================================")
    attempt = 0


def checkSteps():
    global loggedStep, executing, now, attempt
    detectCurrentStep()
    if loggedStep == 0:  # Emulator not runing
        listOfProcessIds = process_exists(emulators[currentEmulator][0])
        running = False
        if listOfProcessIds:
            print('Process Exists | PID and other details are')
            loggedStep = 1
            running = True
                
        if not running :
            print('No Running Process found with given text')
            openL2()
            loggedStep = 1  # step Emulator is oppened
            time.sleep(20) # wait 20 secs"""   
    elif loggedStep == 1:  # Check is rdy for run (talvez seja melhor verificar as cores do botao para ficar mais rapido)
        print("Login Step 1")
        checkL2isOpen()
    elif loggedStep == 2:  # Check l2 is rdy to login in
        print("Login Step 2")
        # seria interessante ter um limite de 1m, se n mostrar fecha apenas o l2 e abre de novo
        #closeBanners() # detect babbers
        findMyChar()
    elif loggedStep == 3:  # Closing Banners
        print("Login Step 3")
        closeBanners()
    else:
        return False

def detectCurrentStep():
    global loggedStep, banner_find, banner_find2, now, text, logged,lastConfirmedLogged
    print("detecting current step")
    positions = find_matches(now, banner_find)
    if len(positions) > 0:
        print("Closing banner")
        x = positions[0][0]
        y = positions[0][1]
        loggedStep = 3  # step waiting for login
        logged = 0
        touch(x, y)  # touch in close banner button
        return True
    
    positions2 = find_matches(now, banner_find2)
    if len(positions2) > 0:
        print("Closing banner 2")
        x = positions2[0][0]
        y = positions2[0][1]
        loggedStep = 3  # step waiting for login
        logged = 0
        touch(x, y)  # touch in close banner button
        return True
    
    if text.find('Character Name') > 0:
        print("Tap in Log In 1")
        loggedStep = 3  # step waiting for login
        touch(1025, 285)  # touch in Login in with first character on list
        return True
    
    if text.find('Character') > 0:
        print("Tap in Log In 2")
        loggedStep = 3  # step waiting for login
        touch(1025, 285)  # touch in Login in with first character on list
        return True
    
def closeBanners():
    global loggedStep, banner_find, banner_find2, now, text
    if now is None:
        print("Erro to get now in checking l2 crasher")
        time.sleep(7) # skip to next thread execution
        return False
    
    positions = find_matches(now, banner_find)
    print(positions)
    if len(positions) > 0:
        print("Closing banner")
        x = positions[0][0]
        y = positions[0][1]
        loggedStep = 3  # step waiting for login
        touch(x, y)  # touch in close banner button
        return True
    
    positions2 = find_matches(now, banner_find2)
    if len(positions2) > 0:
        print("Closing banner 2")
        x = positions2[0][0]
        y = positions2[0][1]
        loggedStep = 3  # step waiting for login
        touch(x, y)  # touch in close banner button
        return True
    elif text.find('Recently Used') > 0:
        print("Ready to Play Game")
        touch(1105, 655)  # play game
        return False
    elif text.find('List') > 0:
        print("Ready to Play Game")
        touch(1105, 655)  # play game
        return False
    elif text.find('Highest CP') > 0:
        print("Ready to Play Game")
        touch(1105, 655)  # play game
        return False
    # detect play button
    elif countPixelsInPosition_NOW(628,960,280,63, [50,101,70], 130, 1000, now, True):
        print("Tap in Play from smart detect")
        loggedStep = 3  # step waiting for login
        touch(1105, 655)  # play game
        return True
    else:
        print("Wait banners")
        return False
# talvez eu precise melhorar, ex se tiver aberto outra tela no jogo


def checkL2Crasher():
    global loggedStep, lastStep2Invalid, text, logged, now,lauch, lauch2, iconPositionX, iconPositionY, crashed, pot3, pot4
    print("Checking L2 Crashed")
    if (text.find("You have been disconnected") > 0 or text.find("been disconnected") > 0) and (findImage(now,pot3) or findImage(now,pot4)) :    
        logged = 0
        loggedStep = 0
        print("You have disconnected, restarting Lineage")
        #killL2Process()
        return True
         
    #icon1 = find_matches(current, lauch)   
    positionsLauch = find_matches(now, lauch)
    if len(positionsLauch) > 0:
        print("Lineage crasher 1")
        logged = 0
        # save position just once
        iconPositionX = positionsLauch[0][0]
        iconPositionY = positionsLauch[0][1]
        lastStep2Invalid = datetime.now()
        loggedStep = 2  # step waiting for login
        print("Opening ...")
        touch(iconPositionX, iconPositionY)
        return True
    
    if findImage(now, crashed):
        print("Lineage crasher")
        logged = 0
        loggedStep = 1
        touch(800,161)
        time.sleep(2)
        return True
    
    return False  


def detectMimeDate():
    # detect mime date and check is 5 minutes ago
    # prevent crash emulator
    return True

def checkisLogged():
    global logged, loggedStep, lastStep2Invalid, text, now, lastConfirmedLogged,offline1, pot1, pot2, pot3, pot4,pot5, pot6
    print("Checking is logged")
    now_plus_15 = lastConfirmedLogged + timedelta(0, 15 * 60)
    
    if checkL2Crasher():
        return True
        
    if lastStep2Invalid != False and loggedStep == 2 and datetime.timestamp(datetime.now()) >= datetime.timestamp(lastStep2Invalid + timedelta(0, 1 * 60)): 
        print("You emulator probability frozenm restart lineage")
        logged = 0
        loggedStep = 0
        lastStep2Invalid = False
        killL2Process()
        
    if lastStep2Invalid != False and logged != 2 :
        lastStep2Invalid = False
        
    if findImage(now,pot1): # todo check pot 100
        print("Character Logged 1")
        loggedStep = 0
        logged = 1
        lastConfirmedLogged = datetime.now()
        return True
    if findImage(now,pot2): # todo check pot 100
        print("Character Logged 2")
        loggedStep = 0
        logged = 1
        lastConfirmedLogged = datetime.now()
        return True
    if findImage(now,offline1):  # reward recess point
        print("Recess reward")
        loggedStep = 0
        logged = 1
        lastConfirmedLogged = datetime.now()
        touch(571, 601) # touch in claim reward, but can implement a select choice reward
        time.sleep(2)
        touch(639, 473) # touch in ok in case total points is 0
        time.sleep(3)
        touch(1104, 116) # touch in claim reward, but can implement a select choice reward
        return True
    if findImage(now,pot3):  # offline mode
        print("Character Logged 3")
        loggedStep = 0
        logged = 1
        lastConfirmedLogged = datetime.now()
        #touch(800, 735)
        #time.sleep(3)
        #touch(571, 601) # touch in claim reward, but can implement a select choice reward
        return True
    if findImage(now,pot4):  # offline mode
        print("Character Logged 4")
        loggedStep = 0
        logged = 1
        lastConfirmedLogged = datetime.now()
        #touch(800, 735)
        #time.sleep(3)
        #touch(571, 601) # touch in claim reward, but can implement a select choice reward
        #time.sleep(3)
        #touch(1102, 115)
        return True
    if findImage(now,pot5):  # offline mode
        print("Character Logged 5")
        loggedStep = 0
        logged = 1
        lastConfirmedLogged = datetime.now()
        #touch(800, 735)
        #time.sleep(3)
        #touch(571, 601) # touch in claim reward, but can implement a select choice reward
        #time.sleep(3)
        #touch(1102, 115)
        return True
    if findImage(now,pot6):  # offline mode
        print("Character Logged 6")
        loggedStep = 0
        logged = 1
        lastConfirmedLogged = datetime.now()
       # touch(800, 735)
        #time.sleep(3)
        #touch(571, 601) # touch in claim reward, but can implement a select choice reward
        #time.sleep(3)
        #touch(1102, 115)
        return True
    if datetime.timestamp(datetime.now()) >= datetime.timestamp(now_plus_15):
        print("something went wrong, restarting Lineage")
        restartL2()
        logged = 0
        loggedStep = 0
        lastConfirmedLogged = datetime.now()
        return False

# Detect is Ready To login
def findMyChar():
    # talvez precise add os passos atuais nos outros
    global loggedStep, text, now
    if smartDetectLoginAvaiable():
        print("Ready to login 0")
        tapInLogin()  # touch in Find my Character
        return False
    # se eu add algo que encontra a cor fica mt mais rapido
    elif findImage(now, loaded):
        print("Tap in Log In 3")
        loggedStep = 3  # step waiting for login
        touch(1025, 285)  # touch in Login in with first character on list
        return True
    else:
        print("Not loaded yet !")  
        loggedStep = 2
        return True
        #loggedStep = 2
        


def checkExistLoad(pic):
    global now
    crop_img = now[743:787, 643:962]  # SS
    cv2.imwrite("test.png", crop_img)
    find = cv2.imread(pic)
    # catch
    found = findImage(crop_img, find)
    if found :
        return True
    else:
        return False


def checkExist(pic):
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
        
    # (h, w, d) = find.shape
    # if h == 0:
    #    return False
    # if w == 0:
    #    return False
    # if d == 0:
    #    return False
    # catch

def tapInLogin():
    touch(760, 608)  # touch in Find my Character

def checkL2isOpen():
    global loggedStep, text, now, loaded
    if smartDetectLoginAvaiable() :
        print("Ready to login 0")
        tapInLogin()  # touch in Find my Character
        return False
    elif findImage(now, loaded):
        loggedStep = 3  # step waiting for login
        touch(1025, 285)  # touch in Login in with first character on list
        return True
    else:
        print("Not loaded yet")
        loggedStep = 1
        closeBanners()

def openL2():
    os.startfile(emulators[currentEmulator][1])
    
def smartDetectLoginAvaiable():
    global now
    print("Detecting Login Screen are avaiable")
    if countPixelsInPosition_NOW(583,645,280,60,[255, 255, 255], 1000, 2000, now, True):
        return True
    else:
        return False 

# testar se funcionar remover essa funcao
def smartDetectPlay() :
    from .loginL2 import now  # now
    if now is None:
        time.sleep(5)  # skip to next thread execution
        return False
    top = 628
    right = 960
    height = 63
    width = 280
    crop_img = now[top : (top + height) , right: (right + width)]
    sought = [50,101,70]
    imm = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
    result = np.count_nonzero(np.all(imm==sought,axis=2))
    print("Play pixels :"+str(result) )
    if result >= 130 : 
        return True
    else:
        return False