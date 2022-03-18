import os
import cv2
import threading
from datetime import date, timedelta, datetime
from .Utils import restart

thread = None
now = None
def FrozenThread():
    global thread
    if thread is not None and thread.isAlive():
        thread.join()

    thread = threading.Timer(60.0, doThread)  # every 7 minutes
    thread.daemon = True
    thread.setName("Frozen Thread")
    thread.start()
    # thread.join()


def doThread():
    global now
    print("* FROZEN THREAD *")
    if os.path.isfile('now.png') == True:
        now = cv2.imread("now.png")
        if now is None:
            return False
        size = os.path.getsize("now.png")
        if size < 200:
            print("problem with current screen : " + str(size))

        assert not isinstance(now, type(None)), 'image not found'
        checkDate()
    print("*************")


def checkDate():
    dat = datetime.fromtimestamp(os.stat("./now.png").st_ctime)
    print("Modified")
    print(dat)
    now_plus = dat + timedelta(0, 2 * 60)
    if datetime.timestamp(now_plus) < datetime.timestamp(dat):
        print("Error in created date")
        restart()
