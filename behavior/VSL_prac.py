print("\nLoading packages...")
from psychopy import visual, core, event
import glob
from math import floor
import random
import pandas as pd
import numpy as np
import re
import time

from VSL_exp_constants import *
import VSL_exp_functions as myFunc

prac_start = time.localtime()
Subj_ID = int(input("\nID number: "))
shapes = glob.glob('stimuli/gray_t(12)/*.jpg')

## Setting up the environment:
win = visual.Window(monitor='mylaptop', size=DISP_SIZE, color=[0, 0, 0],
                    fullscr=FULLSCR, allowGUI=False, units=UNIT)

msg = visual.TextStim(win, text='', pos=(0,0), color=TXTC,
                      height=(FONT_SIZE), wrapWidth=DISP_SIZE[1]*2)
msg.autoDraw = True
msg.autoLog = True

dot = visual.Circle(win, radius=DOT_SIZE, fillColor=DOT_COLORs[0])
dot.autoLog = True

# STIM_SIZE = myFunc.set_stim_size(DISP_SIZE, E_SCR_DIS, SCR_WIDTH, STIM_DEG)
stim = visual.ImageStim(win, image=None, pos=[0,0], size=STIM_SIZE)
stim.autoLog = True

c = core.Clock()

event.Mouse(visible=False) # invisible the mouse
# Experiment start =============================================================
msg.font = FONT_2
msg.setText("歡迎")
win.flip()
core.wait(1)

msg.setText(EXP_INST)
win.flip()
event.waitKeys()

try:
    msg.setText('')
    msg.font = ''
    dot.draw()
    win.flip()
    # core.wait(1)
    jigg = 0

    for s in shapes:
        stim.setImage(s)

        if jigg == 1:
            myFunc.jigg_stimuli(win, stim, c, STIM_TIME, MOVE_TIME, MOVE_DIS)
        else:
            stim.draw()
            win.flip()
            core.wait(STIM_TIME)
        win.flip()

        resp = event.getKeys(keyList=RESP_KEYLIST, timeStamped=c)
        k_resp = [resp[0][0] if resp!=[] else None]

        if k_resp[0] in ESC_KEYLIST:
            raise Exception

        myFunc.give_feedback(jigg, k_resp[0], DOT_COLORs, FB_TIME, dot, win)

        ISI = random.choices(ISIs, weights=ISI_Ws)
        core.wait(ISI[0])

        jigg = np.random.choice([1, 0], p=[0.5, 0.5])

except:
    print('\n<<The experiment is interrupted!>>')

finally:
    win.close()
    prac_end = time.localtime()

    with open('logs//practice//{:03d}_prac.txt'.format(Subj_ID), 'w') as fn:
        fn.writelines('Practice START at '+ time.strftime('%H:%M:%S', prac_start))
        fn.writelines(', END at '+ time.strftime('%H:%M:%S', prac_end))

    # print('\n<<Practice phase is finished.>>')
