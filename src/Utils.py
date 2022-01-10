import argparse
import cv2
import os
import numpy as np
from PIL import Image
import subprocess
from subprocess import check_output
import threading
import time
import re
import psutil
from io import StringIO
import base64
import adbutils
from threading import Thread
# nice live screen
import asyncio
import aiofiles
from ppadb.client_async import ClientAsync as AdbClient
import pytesseract
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
opening = 0
OCR = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = OCR
emulators = [['dnplayer.exe', r'C:\LDPlayer\LDPlayer4.0\dnplayer.exe'], ['Nox.exe', r'C:\Program Files (x86)\nox\bin\Nox.exe','-clone:Nox_0']]
currentEmulator = 1
liveInExecution = 0
invalid = 0

def findImage(pic1, pic2):  # pic1 is the original, while pic2 is the embedding
    dim1_ori = pic1.shape[0]
    dim2_ori = pic1.shape[1]

    dim1_emb = pic2.shape[0]
    dim2_emb = pic2.shape[1]

    v1_emb = pic2[0, 0]
    v2_emb = pic2[0, dim2_emb - 1]
    v3_emb = pic2[dim1_emb - 1, dim2_emb - 1]
    v4_emb = pic2[dim1_emb - 1, 0]

    mask = (pic1 == v1_emb).all(-1)
    found = 0

    if np.sum(mask) > 0:  # Check if a pixel identical to v1_emb
        result = np.argwhere(mask)
        mask = (result[:, 0] <= dim1_ori -
                dim1_emb) & (result[:, 1] <= dim2_ori - dim2_emb)

        if np.sum(mask) > 0:  # Check if the pixel induce a rectangle
            result = result[mask] + [0, dim2_emb - 1]
            mask = [(pic1[tuple(coor)] == v2_emb).all(-1) for coor in result]

            if np.sum(mask) > 0:  # Check if a pixel identical to v2_emb
                result = result[mask] + [dim1_emb-1, 0]
                mask = [(pic1[tuple(coor)] == v3_emb).all(-1)
                        for coor in result]

                if np.sum(mask) > 0:  # Check if a pixel identical to v3_emb
                    result = result[mask] - [0, dim2_emb - 1]
                    mask = [(pic1[tuple(coor)] == v4_emb).all(-1)
                            for coor in result]

                    if np.sum(mask) > 0:  # Check if a pixel identical to v4_emb
                        result = result[mask]
                        result[:, 0] = result[:, 0] - (dim1_emb - 1)
                        result = np.c_[result, result[:, 0] +
                                       dim1_emb, result[:, 1] + dim2_emb]

                        for coor in result:  # Check if the induced rectangle is indentical to the embedding
                            induced_rectangle = pic1[coor[0]                                                     :coor[2], coor[1]:coor[3]]
                            if np.array_equal(induced_rectangle, pic2):
                                found = 1
                                break
    if found == 0:
        return False
    else:
        return True


def _find_matches(haystack, needle):
    myThread = Thread(target=_find_matches(
        haystack, needle), args=(haystack, needle))
    myThread.start()
    myThread.join()


def find_matches(haystack, needle):
    # print(haystack)
    # print(needle)
    try:
        arr_h = np.asarray(haystack)
        try:
            arr_n = np.asarray(needle)
        except ArithmeticError:
            print("Error 3")
            return False
    except ArithmeticError:
        print("Error 3")
        return False

    try:
        y_h, x_h = arr_h.shape[:2]
    except AttributeError:
        print("shape h not found")
        return False
    try:
        y_n, x_n = arr_n.shape[:2]
    except AttributeError:
        print("shape n not found")
        return False

    xstop = x_h - x_n + 1
    ystop = y_h - y_n + 1

    matches = []
    for xmin in range(0, xstop):
        for ymin in range(0, ystop):
            xmax = xmin + x_n
            ymax = ymin + y_n

            arr_s = arr_h[ymin:ymax, xmin:xmax]     # Extract subimage
            arr_t = (arr_s == arr_n)                # Create test matrix
            if arr_t.all():                         # Only consider exact matches
                matches.append((xmin, ymin))

    return matches


def copy():
    subprocess.Popen(
        r"C:\LDPlayer\LDPlayer4.0\adb.exe -s emulator-5554 pull /storage/emulated/0/Download/now.png",
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )


def rightNow():
    subprocess.Popen(
        r"C:\LDPlayer\LDPlayer4.0\adb.exe -s emulator-5554 shell screencap -p /storage/emulated/0/Download/now.png",
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    time.sleep(10)
    copy()
    time.sleep(10)


def swipe(x, y, xx, yy, duration):
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    try:
        d = adb.device()
       # print(d)
        # if len(d) == 0 :
        #    print("Emulator was crashed, try restarting")
        #    restartL2()
        d.swipe(x, y, xx, yy, duration)
        return True
    except IOError:
        print("Swiping error : Device not found,  restarting....")
        restartL2()
        return False


def swipe2(x, y, xx, yy, range):
    subprocess.Popen(
        r"C:\LDPlayer\LDPlayer4.0\adb.exe shell input swipe " +
        str(x) + " " + str(y) + " " + str(xx) +
        " " + str(yy) + " " + str(range),
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )

def addSecs(tm, secs):
    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    return fulldate.time()

def restart():
    process = subprocess.Popen(
        r"C:\LDPlayer\LDPlayer4.0\adb.exe kill-server & C:\LDPlayer\LDPlayer4.0\adb.exe start-server",
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    #output = process.communicate()[0].decode("utf-8")
    process.wait()  # failed to start daemon


def kill():
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == 'dnplayer.exe':
            proc.kill()
            from src.loginL2 import logged
            logged = 0
        elif proc.name() == 'Nox.exe':
            proc.kill()
            from src.loginL2 import logged
            logged = 0


def touch(x, y):
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    try:
        d = adb.device()
        d.click(x, y)
        return True
    except IOError:
        print("Device not found, restarting....")
        restartL2()
        return False


def touch2(x, y):
    process = subprocess.Popen(
        r"C:\LDPlayer\LDPlayer4.0\adb.exe -s emulator-5554 shell input tap " +
        str(x) + " " + str(y),
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    process.wait()


def loopFindMyChar():
    stop_threads = False
    if stop_threads == False:
        print("Running")
    else:
        print("Stop")

    t1 = threading.Timer(15, loopFindMyChar)
    t1.start()
    findMyChar()
    # if stop_threads == False:
    #   t1.join()
    # else :


def waitFindMyChar():
    threading.Timer(30, waitFindMyChar).start()
    findMyChar()


def findMyChar():
    global stop_threads
    now = cv2.imread("now.png")
    find = cv2.imread("Resources\isready.png")
    result = find_matches(now, find)
    if len(result) > 0:
        print("LOGIN")
    else:
        stop_threads = True
        print("Waiting game loading")


def readb64(base64_string):
    sbuf = StringIO()
    sbuf.write(base64.b64decode(base64_string))
    pimg = Image.open(sbuf)
    return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)


def restartL2():
    print("Restarting : " + str(emulators[currentEmulator][0]))
    if process_exists(emulators[currentEmulator][0]):
        kill()
        
    print(emulators[currentEmulator][1])
    #os.startfile(emulators[currentEmulator][1])
    subprocess.Popen([emulators[currentEmulator][1],emulators[currentEmulator][2]])
    time.sleep(20)


async def _save_screenshot(device):
    result = screenAliaisCAP(device)  # device.screencap()
    file_name = f"now.png"
    async with aiofiles.open(f"{file_name}", mode='wb') as f:
        await f.write(result)

    return file_name


async def _live():
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = await client.devices()
    for device in devices:
        print(device.serial)

    result = await asyncio.gather(*[_save_screenshot(device) for device in devices])
    print(result)


def _liveScreen():
    asyncio.run(_live())


def screenAliaisCAP(d):
    stream = d.shell("screencap /sdcard/now.png")
    return stream


def extractText(im):
    #if os.path.isfile('now.png') == False:
    #    return False
    #im = cv2.imread("now.png")  # Image.open("now.png")
    if im is None:
        return ''
    else:
        assert not isinstance(im, type(None)), 'image not found'
        try:
            text = pytesseract.image_to_string(im, lang='eng')
            return text
        except RuntimeError as timeout_error:
            return ''


def extractTextFromResize(top, right, width, height):
    if os.path.isfile('now.png') == False:
        return False

    pytesseract.pytesseract.tesseract_cmd = OCR
    im = cv2.imread("now.png")
    if im is None:
        return ''
    else:
        assert not isinstance(im, type(None)), 'image not found'
        crop_img = im[top: (top + height), right: (right + width)]
        try:
            text = pytesseract.image_to_string(crop_img, lang='eng')
            return text
        except RuntimeError as timeout_error:
            return ''


# falta 2 coisas
# verificar se o arquivo é inferior a 10kb e reiniciar emulador, mas so reiniciar se tiver mais de 1m de diferenca
# bolar um jeito de consumir menos memoria


def liveScreen():
    global opening, liveInExecution, invalid
    if liveInExecution == 1:
        return False
    else:
        liveInExecution = 1
        try:
            adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
            devices = adb.devices()
            if len(devices) == 0:  
                if process_exists(emulators[currentEmulator][0]) == False:
                    os.startfile(emulators[currentEmulator][1])
                    time.sleep(20) 
                invalid += 1
                print("Emulator Crashed #"+str(invalid))
                if invalid > 15:  # 2 minutes
                    invalid = 0
                    liveInExecution = 0
                    restartL2()

                liveInExecution = 0
                return False

            if len(devices) == 0 and os.path.isfile('./now.png') == False and opening == 0:
                opening += 1
                print("no connected")
                liveInExecution = 0
                if opening > 10:
                    restartL2()
                    return True
                else:
                    return False
            try:
                d = adb.device()
                exist = d.shell('echo "Hello world" > /sdcard/now.png')
                print(exist)
                d.shell("rm /sdcard/now.png")
                stream = d.shell("screencap /sdcard/now.png", stream=True)
                time.sleep(1)
                # print(stream)
                with stream:
                    # print(stream)
                    # stream.send("\003") # send Ctrl+C
                    stream.read_until_close()

                if os.path.isfile('./now.png'):
                    try:
                        os.remove("now.png")
                    except IOError:
                        print("File not exist")
                d.sync.pull("/sdcard/now.png", "now.png")  # pulling image
                time.sleep(1)
                # time.sleep(2)
                exists = os.path.isfile('./now.png')
                opening = 0
                liveInExecution = 0
                if exists == False:
                    del exists
                    invalid = 0
                    restartL2()
                else:
                    del exists
                    size = os.path.getsize("now.png")
                    if size < 1000:
                        invalid += 1
                        print("Invalid screen #"+str(invalid))
                        if invalid > 30:  # 3 minutes
                            restartL2()
                            invalid = 0
                            return False

                return True
            except IOError:
                liveInExecution = 0
                print("Error Device not found, restarting....")
                restartL2()
                return False
        except IOError:
            liveInExecution = 0
            print("Error")
            return False


def liveScreen2():
    process = subprocess.Popen(
        r"C:\LDPlayer\LDPlayer4.0\adb.exe -s emulator-5554 shell screencap -p /storage/emulated/0/Download/now.png & C:\LDPlayer\LDPlayer4.0\adb.exe -s emulator-5554 pull /storage/emulated/0/Download/now.png",
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    print(process.stdout)
    try:
        output = process.communicate(timeout=10)[0].decode("utf-8")
        process.wait()
        print("Capturing video screenshot")
        print(output)
        size = os.path.getsize("now.png")
        if size < 500000:  # image invalid
            print(output)
            now = cv2.imread("now.png")
            open_l2 = cv2.imread("Resources/open_l2.png")
            found = findImage(now, open_l2)
            if found :
                return True
            else:
                restart()  # restart adb device
                return False

        checkNotification()
        if 'device not found' in output:
            restart()  # restart adb device
            return True
        else:
            return False
    except Exception:
        return False


def checkNotification():
    now = cv2.imread("now.png")
    lauch = cv2.imread("Resources\notification.png")
    positions = find_matches(now, lauch)
    if len(positions) > 0:
        x = positions[0][0]
        y = positions[0][1]
        print("L2 notifier sikp")
        touch(x, y)


def checkL2isOpen():
    now = cv2.imread("now.png")
    lauch = cv2.imread("Resources\lauch.png")
    positions = find_matches(now, lauch)
    if len(positions) > 0:
        x = positions[0][0]
        y = positions[0][1]
        print("L2 was crasher opening it")
        touch(x, y)
        waitFindMyChar()
    else:
        print("L2 Runing")


def process_exists(processName):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''
    listOfProcessObjects = []
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
       
    print(listOfProcessObjects)
    if len(listOfProcessObjects) > 0 :
        return True 
    else:
        return False


def countPixelsInPosition(top, right, width, height, color, min, max, Print = False):
    from .loginL2 import now  # now
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
def countPixelsInPosition_NOW(top, right, width, height, color, min, max, now, Print = False):
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

def checkExist_NOW(now, pic):
    #from .loginL2 import now  # extracted text
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
    
def findImageByPosition(top, right, width, height, now, pic2):  # pic1 is the original, while pic2 is the embedding
    pic1 = now[top : (top + height) , right: (right + width)]
    
    cv2.imwrite(str(top)+"-"+str(height) + "_test.png", pic1)
    dim1_ori = pic1.shape[0]
    dim2_ori = pic1.shape[1]

    dim1_emb = pic2.shape[0]
    dim2_emb = pic2.shape[1]

    v1_emb = pic2[0, 0]
    v2_emb = pic2[0, dim2_emb - 1]
    v3_emb = pic2[dim1_emb - 1, dim2_emb - 1]
    v4_emb = pic2[dim1_emb - 1, 0]

    mask = (pic1 == v1_emb).all(-1)
    found = 0

    if np.sum(mask) > 0:  # Check if a pixel identical to v1_emb
        result = np.argwhere(mask)
        mask = (result[:, 0] <= dim1_ori -
                dim1_emb) & (result[:, 1] <= dim2_ori - dim2_emb)

        if np.sum(mask) > 0:  # Check if the pixel induce a rectangle
            result = result[mask] + [0, dim2_emb - 1]
            mask = [(pic1[tuple(coor)] == v2_emb).all(-1) for coor in result]

            if np.sum(mask) > 0:  # Check if a pixel identical to v2_emb
                result = result[mask] + [dim1_emb-1, 0]
                mask = [(pic1[tuple(coor)] == v3_emb).all(-1)
                        for coor in result]

                if np.sum(mask) > 0:  # Check if a pixel identical to v3_emb
                    result = result[mask] - [0, dim2_emb - 1]
                    mask = [(pic1[tuple(coor)] == v4_emb).all(-1)
                            for coor in result]

                    if np.sum(mask) > 0:  # Check if a pixel identical to v4_emb
                        result = result[mask]
                        result[:, 0] = result[:, 0] - (dim1_emb - 1)
                        result = np.c_[result, result[:, 0] +
                                       dim1_emb, result[:, 1] + dim2_emb]

                        for coor in result:  # Check if the induced rectangle is indentical to the embedding
                            induced_rectangle = pic1[coor[0]                                                     :coor[2], coor[1]:coor[3]]
                            if np.array_equal(induced_rectangle, pic2):
                                found = 1
                                break
    if found == 0:
        return False
    else:
        return True