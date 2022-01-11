from .Utils import liveScreen, restartL2, touch, countPixelsInPosition, emulators, currentEmulator
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
def checkLogged():
    global logged
    return logged

def loopLoggin():
    global threadLogin, logged, Try, now
    if threadLogin != False and threadLogin.isAlive():
        threadLogin.cancel()
        thread = False
      
    threadLogin = threading.Timer(15.0, loopLoggin)
    threadLogin.daemon = True # stop if the program exits
    threadLogin.start()
    from .SummoningCircle import finishedSummoningCircle
    from .TempleGuardian import finishedTempleGuardian
    from .Utils import emulators, currentEmulator
    if finishedSummoningCircle == 0 or finishedTempleGuardian == 0:
        return False
    
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
            channels = now.shape[2]
            if size < 200:
                print("problem with current screen : " + str(size))
                
            assert not isinstance(now, type(None)), 'image not found'
            Try = 0
            doLogin()
    #threadLogin.join()        

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
    global now, loggedStep, logged, threadLogin, executing, text, attempt
    #text = ''
    print("================== LOGIN THREAD ========================")
    text = extractText(now) # esse talvez seja o problema de high RAM
    checkisLogged()  # necessario para que o L2 feche por algum motivo
    if logged == 0:
        checkSteps()
    print("================================================")
    attempt = 0


def checkSteps():
    global loggedStep, executing, now, attempt
    if loggedStep == 0:  # Emulator not runing
        listOfProcessIds = process_exists(emulators[currentEmulator][0])
        running = False
        if len(listOfProcessIds) > 0:
            print('Process Exists | PID and other details are')
            for elem in listOfProcessIds:
                processID = elem['pid']
                processName = elem['name']
                processCreationTime =  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(elem['create_time']))
                print((processID ,processName,processCreationTime ))
                loggedStep = 1
                running = True
                
        if running == False :
            print('No Running Process found with given text')
            openL2()
            loggedStep = 1  # step Emulator is oppened
            time.sleep(20) # wait 20 secs"""   
    elif loggedStep == 1:  # Check is rdy for run (talvez seja melhor verificar as cores do botao para ficar mais rapido)
        print("Login Step 1")
        checkL2isOpen()
    elif loggedStep == 2:  # Check l2 is rdy to login in
        print("Login Step 2")
        #closeBanners() # detect babbers
        findMyChar()
    elif loggedStep == 3:  # Closing Banners
        print("Login Step 3")
        closeBanners()
    else:
        return False


def closeBanners():
    global loggedStep
    global now
    global text
    if now is None:
        print("Erro to get now in checking l2 crasher")
        time.sleep(7) # skip to next thread execution
        return False
    find = cv2.imread("Resources\closeBanner1.png")
    find2 = cv2.imread("Resources\closeBanner2.png")
    positions = find_matches(now, find)
    positions2 = find_matches(now, find2)
    if len(positions) > 0:
        print("Closing banner")
        x = positions[0][0]
        y = positions[0][1]
        loggedStep = 3  # step waiting for login
        touch(x, y)  # touch in close banner button
        return True
    elif len(positions2) > 0:
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
    elif smartDetectPlay() :
        print("Tap in Play from smart detect")
        loggedStep = 3  # step waiting for login
        touch(1105, 655)  # play game
        return True
    else:
        print("Wait banners")
        return False
# talvez eu precise melhorar, ex se tiver aberto outra tela no jogo


def checkL2Crasher():
    global loggedStep, logged, now,lauch, lauch2
    print("Checking L2 Crashed")
    #icon1 = find_matches(current, lauch)    
    """if checkExist("Resources\clock.png"):  # reward recess point, but I'm logged
        print("Character Logged Recess reward")
        loggedStep = 0
        logged = 1
        touch(571, 601) # touch in claim reward, but can implement a select choice reward
        return True;"""
    positionsLauch = find_matches(now, lauch)
    if len(positionsLauch) > 0:
        print("Lineage crasher 1")
        from .EliteQuest import currentStep  # extracted text
        currentStep = 0
        print("Opening ...")
        logged = 0
        x = positionsLauch[0][0]
        y = positionsLauch[0][1]
        loggedStep = 2  # step waiting for login
        touch(x, y)
        return True
    
    icon2 = find_matches(now, lauch2)
    if len(icon2) > 0:
        print("Lineage crasher 1")
        from .EliteQuest import currentStep  # extracted text
        currentStep = 0
        print("Opening ...")
        logged = 0
        x = icon2[0][0]
        y = icon2[0][1]
        loggedStep = 2  # step waiting for login
        touch(x, y)
        del icon2
        return True
    elif checkExist("Resources\crasher.png"):
        print("Lineage crasher")
        from .EliteQuest import currentStep  # extracted text
        currentStep = 0
        logged = 0
        loggedStep = 1
        touch(800,161)
        del lauch
        time.sleep(2)
        return True
    
    return False


def detectMimeDate():
    # detect mime date and check is 5 minutes ago
    # prevent crash emulator
    return True

def checkisLogged():
    global logged, loggedStep, text
    print("Checking is logged")
    if checkExist("Resources\pot.png"): # todo check pot 100
        print("Character Logged 1")
        loggedStep = 0
        logged = 1
        return True;
    elif checkExist("Resources\pot2.png"): # todo check pot 100
        print("Character Logged 2")
        loggedStep = 0
        logged = 1
        return True;
    elif checkExist('Resources\clock.png'):  # reward recess point
        print("Recess reward")
        loggedStep = 0
        logged = 1
        touch(571, 601) # touch in claim reward, but can implement a select choice reward
        time.sleep(2)
        touch(639, 473) # touch in ok in case total points is 0
        time.sleep(3)
        touch(1104, 116) # touch in claim reward, but can implement a select choice reward
        return True;
    elif checkExist("Resources\pot3.png"):  # offline mode
        print("Character Logged 3")
        loggedStep = 0
        logged = 1
        #touch(800, 735)
        #time.sleep(3)
        #touch(571, 601) # touch in claim reward, but can implement a select choice reward
        return True;
    elif checkExist("Resources\pot4.png"):  # offline mode
        print("Character Logged 4")
        loggedStep = 0
        logged = 1
        #touch(800, 735)
        #time.sleep(3)
        #touch(571, 601) # touch in claim reward, but can implement a select choice reward
        #time.sleep(3)
        #touch(1102, 115)
        return True;
    elif checkExist("Resources\pot5.png"):  # offline mode
        print("Character Logged 5")
        loggedStep = 0
        logged = 1
        #touch(800, 735)
        #time.sleep(3)
        #touch(571, 601) # touch in claim reward, but can implement a select choice reward
        #time.sleep(3)
        #touch(1102, 115)
        return True;
    elif checkExist("Resources\pot6.png"):  # offline mode
        print("Character Logged 6")
        loggedStep = 0
        logged = 1
       # touch(800, 735)
        #time.sleep(3)
        #touch(571, 601) # touch in claim reward, but can implement a select choice reward
        #time.sleep(3)
        #touch(1102, 115)
        return True;
    else:
        checkL2Crasher()
        return False;

# Detect is Ready To login
def findMyChar():
    # talvez precise add os passos atuais nos outros
    global loggedStep
    global text
    if smartDetectLoginAvaiable():
        print("Ready to login 0")
        tapInLogin()  # touch in Find my Character
        return False
    elif text.find('LV') > 0:
        print("Ready to login 2")
        tapInLogin()  # touch in Find my Character
        return False
    elif text.find('Tap') > 0 or text.find('TAP') > 0 or text.find('START') > 0:
        print("Ready to login 3")
        tapInLogin()  # touch in Find my Character
        return False
    elif text.find('Aden Castle Owner') > 0:
        print("Ready to login 3")
        tapInLogin()  # touch in Find my Character
        loggedStep = 2
        return False
    elif text.find('Aden Castle') > 0:
        print("Ready to login 4")
        loggedStep = 2
        tapInLogin()  # touch in Find my Character
        return False
    elif text.find('Lamael') > 0:
        print("Ready to login 5")
        tapInLogin()  # touch in Find my Character
        return False
    elif text.find('Lancer') > 0:
        print("Ready to login 6")
        tapInLogin()  # touch in Find my Character
        return False
    elif text.find('Aria') > 0:
        print("Ready to login 7")
        tapInLogin()  # touch in Find my Character
        return False
    elif text.find('Castle of') > 0:
        print("Ready to login 8")
        tapInLogin()  # touch in Find my Character
        return False
    elif text.find('Castle of Darkness') > 0:
        print("Ready to login 9")
        tapInLogin()  # touch in Find my Character
        return False
    elif text.find('Character Name') > 0:
        print("Tap in Log In 1")
        loggedStep = 3  # step waiting for login
        touch(1025, 285)  # touch in Login in with first character on list
        return True
    elif text.find('Character') > 0:
        print("Tap in Log In 2")
        loggedStep = 3  # step waiting for login
        touch(1025, 285)  # touch in Login in with first character on list
        return True
    elif text.find('Checking if any files were patched') > 0:
        loggedStep = 3  # step waiting for login
        return True
    # se eu add algo que encontra a cor fica mt mais rapido
    elif checkExist("Resources\loaded.png"):
        print("Tap in Log In 3")
        loggedStep = 3  # step waiting for login
        touch(1025, 285)  # touch in Login in with first character on list
        return True
    else:
        print("Not loaded yet !")  
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
    global loggedStep
    global now
    lauch = cv2.imread("Resources\lauch.png")
    current = cv2.imread("now.png")
    if current is None:
        print("Eita poHa Die")
        time.sleep(7) # skip to next thread execution
        return False
    
    positions = find_matches(current, lauch)
    print(text)
    if len(positions) > 0:
        print("Opening ....")
        x = positions[0][0]
        y = positions[0][1]
        loggedStep = 2  # step waiting for login
        touch(x, y)
    elif smartDetectLoginAvaiable() :
        print("Ready to login 0")
        tapInLogin()  # touch in Find my Character
        return False
    elif text.find('Tap') > 0:
        print("Ready to login")
        tapInLogin()  # touch in Find my Character
        return False
    elif text.find('TAP') > 0:
        print("Ready to login")
        tapInLogin()  # touch in Find my Character
        return False
    elif text.find('START') > 0:
        print("Ready to login")
        tapInLogin()  # touch in Find my Character
        return False
    elif text.find('Aden Castle Owner') > 0:
        print("Ready to login")
        tapInLogin()  # touch in Find my Character
        return False
    elif text.find('Aden Castle') > 0:
        print("Ready to login")
        tapInLogin()  # touch in Find my Character
        return False
    elif text.find('Lamael') > 0:
        print("Ready to login")
        touch(788, 501)  # touch in Find my Character
        return False
    elif text.find('Lancer') > 0:
        print("Ready to login")
        tapInLogin()  # touch in Find my Character
        return False
    elif text.find('Aria') > 0:
        print("Ready to login")
        tapInLogin()  # touch in Find my Character
        return False
    elif text.find('Castle of Darkness') > 0:
        print("Ready to login")
        tapInLogin()  # touch in Find my Character
        return False
    elif text.find('Character Name') > 0:
        loggedStep = 3  # step waiting for login
        touch(1025, 285)  # touch in Login in with first character on list
        return True
    elif text.find('Character') > 0:
        loggedStep = 3  # step waiting for login
        touch(1025, 285)  # touch in Login in with first character on list
        return True
    elif checkExist("Resources\loaded.png"):
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
    if countPixelsInPosition(583,645,300,60,[86, 114, 157], 80, 100):
        return True
    else:
        return False 
    """
    from .loginL2 import now  # now
    if now is None:
        print("smart detect login avaiable can't get current screen")
        time.sleep(5)  # skip to next thread execution
        return False
    top = 583
    right = 645
    height = 15
    width = 15
    crop_img = now[top : (top + height) , right: (right + width)]
    sought = [197,206,219]
    imm = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
    result = np.count_nonzero(np.all(imm==sought,axis=2))
    print("LOGIN PIXELS : " + str(result))
    if result > 2 and result < 5 : 
        return True
    else:
        return False  """
    
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