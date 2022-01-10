#!/usr/bin/env python
"""
    Example of (almost) all Elements, that you can use in PySimpleGUI.
    Shows you the basics including:
        Naming convention for keys
        Menubar format
        Right click menu format
        Table format
        Running an async event loop
        Theming your application (requires a window restart)
        Displays the values dictionary entry for each element
        And more!

    Copyright 2021 PySimpleGUI
"""
from enum import auto
import tkinter as tk
from PIL import Image, ImageTk
import sys
import adbutils
from sys import maxsize
import threading
from tkinter.constants import TRUE
import PySimpleGUI as sg
import os
import subprocess
from ppadb.client import Client as AdbClient
import time
import cv2
import numpy as np
from src.TowerOfInsolence import loopTowerOfInsolence
from src.HallOfGreed import loopHallOfGreed
from src.Utils import checkL2isOpen
from src.Utils import rightNow
from src.Utils import swipe
from src.loginL2 import openL2
from src.Utils import liveScreen
from src.loginL2 import loopLoggin
from src.Utils import restart
from src.Comissions import loopComissions
from src.Utils import touch
from src.DailyDungeon import loopDailyDungeon
from src.ScrollQuest import loopScrollQuest
from src.SummoningCircle import loopSummoningCircle
from src.TempleGuardian import loopTempleGuardian
from src.Farming import loopFarming
from src.EliteQuest import loopEliteQuest
from src.AlahurAkbar import loopAlahurAkbar
import random
import psutil
from shutil import copyfile
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from PIL import Image, ImageTk
import io
sell = datetime.now()
daily = 0
# duplicate dies
backing = 0


def on_click(event=None):
    # `command=` calls function without argument
    # `bind` calls function with one argument
	print(event.x)
	print(event.y)
    #print("image clicked")

def addSecs(tm, secs):
    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    return fulldate.time()


def doLoginCharacter():
    # find my character
    touch(975, 620)
    time.sleep(5)
    # touch first character
    touch(1277, 351)
    time.sleep(90)
    # close banners
    print("Close banners")
    touch(1566, 40)
    time.sleep(5)
    touch(1512, 29)
    time.sleep(5)
    touch(1512, 29)
    time.sleep(5)
    touch(1512, 29)
    time.sleep(5)
    touch(1512, 29)
    time.sleep(5)
    print("Play")
    # touch play
    touch(1350, 820)
# @todo Verificar tela de recarregar que aparece do nada e fecha-la
def backToFarm():
    print("Back to farm")
    touch(637, 480)  # click in OK
    time.sleep(1)
    touch(637, 480)  # click in OK
    time.sleep(1)
    touch(1153, 530) # tap in spot revival
    time.sleep(5)
    # close alert
    #touch(1239, 250) # tap in close alert
    #time.sleep(5)
    # click on map
    touch(1172, 92)
    time.sleep(5)
    # click on spot
    if random.randint(0, 100) < 50:
        touch(423, 291)  # 505, 581 # campo 700, 560   elite  797, 659
    else:
        touch(466, 342)  # 508, 558 # campo 700, 230   #elite 736, 672
    # 530 undead  423, 291 | 466, 342
    time.sleep(23)  # 43
    # set auto
    touch(1089, 850)
    
def checkFull():
    global sell
    now = datetime.now()
    now_plus_10 = sell + timedelta(0, 5 * 60)
    print("===========================")
    print(sell)
    print(now_plus_10)
    print(now)
    if datetime.timestamp(now) > datetime.timestamp(now_plus_10):
        print("Ta na hora de vender")
        restart()
        sell = now
        touch(1237, 38)
        # start sell
        time.sleep(10)
        # bulk sale
        touch(1280, 850)
        time.sleep(2)
        # sell
        touch(1500, 850)
        time.sleep(2)
        # confirm
        touch(960, 610)
        time.sleep(2)
        # close
        touch(790, 580)
        time.sleep(2)
        # back
        touch(1560, 49)

    print("===========================")
    # image = cv2.imread("now.png")
    # full = cv2.imread("Resources\isfull.png")
    # isFull = find_image(image,full)
    # print(isFull)
    # if(isFull == "Die"):
    # print("Full")
    # touch(1237,38)
    # else :
    # print("No Full")


def connectADB():
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    d = adb.device()
    print(d.serial)
    stream = d.shell("screencap /sdcard/png.png", stream=True)
    time.sleep(3) # record for 3 seconds
    print(stream)
    #with stream:
    #    stream.send("\003") # send Ctrl+C
    #    stream.read_until_close()

    start = time.time()
    print("Video total time is about", time.time() - start)
    d.sync.pull("/sdcard/png.png", "s.png") # pulling video

    #d.click(158, 150)
    #serial = d.shell("input tap 158 150")
    #myDevice = adb.devices()[0]
    #print(serial)
    

def checkEmulatorIsOpen(name):
    if os.path.isfile('./now.png') : 
        try:
            os.remove("now.png")
        except IOError:
            print("File not exist")
            
    loopLoggin()
    loopSummoningCircle()
    #loopDailyDungeon() # DONE
    #loopTowerOfInsolence()  # DONE
    loopTempleGuardian() # DONE
    #loopEliteQuest()
    loopScrollQuest() #
    loopFarming()


def get_img_data(f, maxsize=(1200, 850), first=False):
    """Generate image data using PIL
    """
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:                     # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)


def make_window(theme):
    sg.theme(theme)
    menu_def = [['&Application', ['E&xit']],
                ['&Help', ['&About']]]
    right_click_menu_def = [[], ['Nothing', 'More Nothing', 'Exit']]

    # Table Data
    data = [["John", 10], ["Jen", 5]]
    headings = ["Name", "Score"]
    cave = cv2.imread("Resources\map.png")
    from src.Farming import EliteDungeonList
    from src.Farming import Decks
    
    input_layout = [[sg.Menu(menu_def, key='-MENU-')],
                    [sg.Text('Farm Mode')],
              
                    [sg.Text('Quests')],
                    [sg.Checkbox('Main Quests', default=True,
                                 k='-MainQuests-'),
                    sg.Checkbox('Daily Quests', default=True,
                                k='-DailyQuests-'),
                    sg.Checkbox('Weekly Quests', default=True,
                                k='-WeeklyQuests-'),
                    sg.Checkbox('Scroll Quests', default=True,
                                k='-ScrollQuests-')],
                    [sg.Text('Dungeons')],
                    [sg.Checkbox('Hall of Greed      ', default=True,
                                 k='-HallOfGreedDungeons-'),
                     sg.Checkbox('Daily Dungeons', default=True,
                                 k='-DailyDungeons-'),
                    sg.Checkbox('Tower Of Insolence  ', default=True,
                     k='-TowerOfInsolence-'),
                    sg.Checkbox('Extraction Pit', default=True,
                                k='-ExtractionPit-')],
                    [sg.Checkbox('Temple Guardian', default=True,
                                 k='-TempleGuardian-'),
                    sg.Checkbox('Adena Vault     ', default=True,
                                k='-AdenaVault-'),
                    sg.Checkbox('Trials Of Experience', default=True,
                     k='-TrialsOfExperience-'),
                    sg.Checkbox('Summoning Circle', default=True,
                                k='-SummoningCircle-')],
                    # [sg.Input(key='-INPUT-')],
                    # [sg.Slider(orientation='h', key='-SKIDER-'), sg.Image(data=sg.DEFAULT_BASE64_LOADING_GIF, enable_events=True, key='-GIF-IMAGE-'),],
                    # [sg.Checkbox('Checkbox', default=True, k='-CB-')],
                    [sg.Text('Reset Time')],
                    [sg.Spin([i for i in range(0, 23)], initial_value=6,
                             k='-SPIN-'), sg.Spin([i for i in range(0, 59)], initial_value=30,
                                                  k='-SPIN2-'), sg.Text('Spin')],
                    [sg.Button('Run', size=(12, 2), button_color=('white', 'green'), font=('Robot', 12)),
                     sg.Button('Stop', size=(12, 2), button_color=(
                         'white', 'grey'), font=('Robot', 12)),
                     ]]

    asthetic_layout = [
                        [sg.T('Farm Mode')],
                        [
                            sg.Radio('Elite Monsters', "RadioDemo", default=True, size=(10, 1), k='-R1-'),
                            sg.Radio('Normal Monsters', "RadioDemo", default=True, size=(15, 1), k='-R2-'),
                            sg.Radio('World Dungeon', "RadioDemo", default=True, size=(15, 1), k='-R3-'),
                        ],
                        #[sg.Image(data=sg.DEFAULT_BASE64_ICON,  k='-IMAGE-')],
                        [sg.Text('Elite Farm 1',size=(32,1)),
                         sg.Text('Position X',size=(7,1)),
                         sg.Text('Position Y',size=(7,1)),
                         sg.Text('Spot',size=(8,1)),
                         sg.Text('Deck',size=(8,1))
                        ],
                        [
                            sg.Combo(EliteDungeonList,default_value=EliteDungeonList[31],key='farm1',readonly=True),
                            sg.I(key='-FE1x-', do_not_clear=True, size=(8,1)),
                            sg.I(key='-FE1y-', do_not_clear=True, size=(8,1)),
                            sg.Button('Open Map',key='MAP1'),
                            sg.Combo(Decks,default_value=Decks[1],key='-deck1-',readonly=True),
                            ],
                        [sg.Text('Elite Farm 2',size=(32,1)),sg.Text('Position X',size=(7,1)),
                         sg.Text('Position Y',size=(7,1)),
                         sg.Text('Spot',size=(8,1)),
                         sg.Text('Deck',size=(8,1))],
                        [
                            sg.Combo(EliteDungeonList,default_value=EliteDungeonList[31],key='farm2',readonly=True),
                            sg.I(key='-FE2x-', do_not_clear=True, size=(8,1)),
                            sg.I(key='-FE2y-', do_not_clear=True, size=(8,1)),
                            sg.Button('Open Map',key='-MAP2-'),
                            sg.Combo(Decks,default_value=Decks[1],key='-deck2-',readonly=True),
                            ],
                        [sg.Text('Elite Farm 3',size=(32,1)),sg.Text('Position X',size=(7,1)),
                         sg.Text('Position Y',size=(7,1)),
                         sg.Text('Spot',size=(8,1)),
                         sg.Text('Deck',size=(8,1))],
                        [
                            sg.Combo(EliteDungeonList,default_value=EliteDungeonList[31],key='farm3',readonly=True),
                            sg.I(key='-FE3x-', do_not_clear=True, size=(8,1)),
                            sg.I(key='-FE3y-', do_not_clear=True, size=(8,1)),
                            sg.Button('Open Map',key='-MAP3-'),
                            sg.Combo(Decks,default_value=Decks[1],key='-deck3-',readonly=True),
                        ],
                        [sg.Text('Elite Farm 4',size=(32,1)),sg.Text('Position X',size=(7,1)),
                         sg.Text('Position Y',size=(7,1)),
                         sg.Text('Spot',size=(8,1)),
                         sg.Text('Deck',size=(8,1))],
                        [
                            sg.Combo(EliteDungeonList,default_value=EliteDungeonList[30],key='farm4',readonly=True),
                            sg.I(key='-FE4x-', do_not_clear=True, size=(8,1)),
                            sg.I(key='-FE4y-', do_not_clear=True, size=(8,1)),
                            sg.Button('Open Map',key='-MAP4-'),
                            sg.Combo(Decks,default_value=Decks[1],key='-deck4-',readonly=True),
                        ],
                        [sg.Text('Elite Farm 5',size=(32,1)),sg.Text('Position X',size=(7,1)),
                         sg.Text('Position Y',size=(7,1)),
                         sg.Text('Spot',size=(8,1)),
                         sg.Text('Deck',size=(8,1))],
                        [
                            sg.Combo(EliteDungeonList,default_value=EliteDungeonList[30],key='farm5',readonly=True),
                            sg.I(key='-FE5x-', do_not_clear=True, size=(8,1)),
                            sg.I(key='-FE5y-', do_not_clear=True, size=(8,1)),
                            sg.Button('Open Map',key='-MAP5-'),
                            sg.Combo(Decks,default_value=Decks[1],key='-deck5-',readonly=True),
                        ],
                       [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='-PROGRESS BAR-'), sg.Button('Test Progress bar')]]

    logging_layout = [[sg.Text("Anything printed will display here!")], [
        sg.Output(size=(60, 35), font='Courier 8')]]

    graphing_layout = [[sg.Text("Anything you would use to graph will display here!")],
                       [sg.Graph((200, 200), (0, 0), (200, 200),
                                 background_color="black", key='-GRAPH-', enable_events=True)],
                       [sg.T('Click anywhere on graph to draw a circle')],
                       [sg.Table(values=data, headings=headings, max_col_width=25,
                                 background_color='black',
                                 auto_size_columns=True,
                                 display_row_numbers=True,
                                 justification='right',
                                 num_rows=2,
                                 alternating_row_color='black',
                                 key='-TABLE-',
                                 row_height=25)]]

    specalty_layout = [[sg.Text("Any \"special\" elements will display here!")],
                       [sg.Button("Open Folder")],
                       [sg.Button("Open File")]]

    theme_layout = [[sg.Text("See how elements look under different themes by choosing a different theme here!")],
                    [sg.Listbox(values=sg.theme_list(),
                                size=(20, 12),
                                key='-THEME LISTBOX-',
                                enable_events=True)],
                    [sg.Button("Set Theme")]]

    layout = []
    layout += [[sg.TabGroup([[sg.Tab('Main Menu', input_layout),
                              sg.Tab('Farm Setting', asthetic_layout),
                              # sg.Tab('Profile', graphing_layout),
                              # sg.Tab('System Setting', specalty_layout),
                              sg.Tab('Theming', theme_layout),
                              sg.Tab('Progress', logging_layout)]], key='-TAB GROUP-')]]

    return sg.Window('Lineage Revolution Bot by MagoxNegro', layout, right_click_menu=right_click_menu_def)


def find_image(pic1, pic2):  # pic1 is the original, while pic2 is the embedding

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
                            induced_rectangle = pic1[coor[0]:coor[2], coor[1]:coor[3]]
                            if np.array_equal(induced_rectangle, pic2):
                                found = 1
                                break
    if found == 0:
        return('Living')
    else:
        return('Die')


def main():
    window = make_window(sg.theme())
    autoload = False
    try:
        if sys.argv[1] == '-a':
            autoload = True
            checkEmulatorIsOpen("dnplayer.exe")
    except IndexError:
        autoload = False
        
    #print(autoload)
    
    #print('Number of arguments: {}'.format(len(sys.argv)))
    #print('Argument(s) passed: {}'.format(str(sys.argv)))
    # This is an Event Loop
    while True:
        event, values = window.read(timeout=100)
        # keep an animation running so show things are happening
        # window['-GIF-IMAGE-'].update_animation(sg.DEFAULT_BASE64_LOADING_GIF, time_between_frames=100)
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            print('============ Event = ', event, ' ==============')
            print('-------- Values Dictionary (key=value) --------')
            for key in values:
                print(key, ' = ', values[key])
        if event in (None, 'Exit'):
            print("[LOG] Clicked Exit!")
            os.system("taskkill /F /IM adb.exe")
            break
        elif event == 'About':
            print("[LOG] Clicked About!")
            sg.popup('PySimpleGUI Demo All Elements',
                     'Right click anywhere to see right click menu',
                     'Visit each of the tabs to see available elements',
                     'Output of event and values can be see in Output tab',
                     'The event and values dictionary is printed after every event')
        elif event == 'MAP1':
            os.system('python3 init.py')
            #sg.popup('PySimpleGUI Demo All Elements','init.py',keep_on_top=True)
        elif event == 'Run':
            print("[LOG] Clicked Popup Button!")
            checkEmulatorIsOpen("dnplayer.exe")
            print("[LOG] Dismissing Popup!")
        elif event == 'Stop':
            print("[LOG] Pausando BOT")
            current_system_pid = os.getpid()
            ThisSystem = psutil.Process(current_system_pid)
            ThisSystem.terminate()
        elif event == 'Test Progress bar':
            print("[LOG] Clicked Test Progress Bar!")
            progress_bar = window['-PROGRESS BAR-']
            for i in range(1000):
                print("[LOG] Updating progress bar by 1 step ("+str(i)+")")
                progress_bar.UpdateBar(i + 1)
            print("[LOG] Progress bar complete!")
        elif event == "-GRAPH-":
            graph = window['-GRAPH-']       # type: sg.Graph
            graph.draw_circle(values['-GRAPH-'],
                              fill_color='yellow', radius=20)
            print("[LOG] Circle drawn at: " + str(values['-GRAPH-']))
        elif event == "Open Folder":
            print("[LOG] Clicked Open Folder!")
            folder_or_file = sg.popup_get_folder('Choose your folder')
            sg.popup("You chose: " + str(folder_or_file))
            print("[LOG] User chose folder: " + str(folder_or_file))
        elif event == "Open File":
            print("[LOG] Clicked Open File!")
            folder_or_file = sg.popup_get_file('Choose your file')
            sg.popup("You chose: " + str(folder_or_file))
            print("[LOG] User chose file: " + str(folder_or_file))
        elif event == "Set Theme":
            print("[LOG] Clicked Set Theme!")
            theme_chosen = values['-THEME LISTBOX-'][0]
            print("[LOG] User Chose Theme: " + str(theme_chosen))
            window.close()
            window = make_window(theme_chosen)

    window.close()
    exit(0)


if __name__ == '__main__':
    main()
