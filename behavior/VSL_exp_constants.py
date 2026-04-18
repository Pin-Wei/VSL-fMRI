# -*- coding: utf-8 -*-
RUNS = 10 # number of run
REPT_SC = 3 # number of repeation in scanning (pre/post-exposure) runs
REPT_EXP = 6 # number of repeation in exposure runs
TARG_PER = 10 # percentage of target within each run
TASK = 'jigg_task'

## Monitor resolution
# from win32api import GetSystemMetrics
import ctypes
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
# MON_RES = [GetSystemMetrics(0), GetSystemMetrics(1)]
MON_RES = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
## Display size
DISP_SIZE = MON_RES # the Display size should match the Monitor resolution

## Full screen or not
FULLSCR = True
## unit of the Window
UNIT = 'pix'
## file type of the stimuli image
IMG_FT = 'png'

## Background color
BGC = (-0.25, -0.25, -0.25) # dark gray
## Text color
TXTC = (-1, -1, -1) # black
## Fixation (=task feedback) color
DOT_COLORs = [(-0.5, -0.5, -0.5), (1, 0, 0), (0, 1, 0)] # ['', 'red', 'green']

## Stimuli size
STIM_SIZE = DISP_SIZE[1]*0.24
# STIM_SIZE = 460.8 # Display size= [2560, 1920]
## E_SCR_DIS = 40 # eye-screen distance (cm)
## SCR_WIDTH = 33 # screen width (cm)
## STIM_DEG = 6.8 # degree

## Fixation (=task feedback) size
DOT_SIZE = STIM_SIZE/24
# DOT_SIZE = 19.2 # Display size= [2560, 1920]

## Text size
FONT_SIZE = DOT_SIZE*4
# FONT_SIZE = 76.8 # Display size= [2560, 1920]

## Font
FONT_1 = ''
FONT_2 = u'DFKai-SB' # 標楷體

## Duration of the Stimuli (sec)
STIM_TIME = 1.0
# STIM_corr_j = 0.017755 # time correction for the targets (jiggled items)
STIM_corr_j = 0.1190
# STIM_corr_nj = 0.004667 # time correction for the non-targets
STIM_corr_nj = 0.0075
SLOW = 2.0

## Inter-Stimulus Intervals (sec)
ISIs = [1, 3, 5]
# ISI_Ws = [0.4, 0.4, 0.2]
ISI_Ws = [4/7, 2/7, 1/7] # weights of each ISI
# ISI_corr = 0.0074
ISI_corr = 0.5

## Duration of the Feedback
FB_TIME = 0.8
## Duration of the rapid left/right movement (sec)
MOVE_TIME = 0.2
## Distance of the movement to the left/right (pix)
MOVE_DIS = DOT_SIZE*3

## Allowed keys
TRIG_KEYLIST = ['5', 'num_5']
RESP_KEYLIST = ['1', 'num_1', '2', '3', '4',
                'escape', 'esc', 'e']
ESC_KEYLIST = ['escape', 'esc', 'e']

## Instruction
EXP_INST = '''
           \n您將在電腦螢幕上看到一系列的幾何圖形
           \n這些圖形會一個接著一個出現
           \n其中，有一些圖形會快速晃動一下
           \n針對這類型的刺激，請以最快的速度按下數字"1"鍵做反應
           \n
           \n注意：本作業結束後會有測驗，請仔細觀看每一個圖形
           \n
           \n[按下空白鍵以開始實驗]
           '''
# EXP_INST = '''
#            \nOn the screen, you will see a series of shapes, one after the other.
#            \nSome of the shapes will jitter rapidly, please press number key '1' to response to those shapes as soon as possible.
#            \n
#            \nAt the meanwhile, please watch the stream of shapes carefully,
#            \nas you will later be tested.
#            \n
#            \n[ Press any key to start the experiment ]
#            '''
