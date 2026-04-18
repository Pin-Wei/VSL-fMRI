# -*- coding: utf-8 -*-

## the Display size should match the Monitor resolution ##
# Monitor resolution
import ctypes
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
MON_RES = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
# Display size
DISP_SIZE = MON_RES

# unit of the Window
UNIT = 'pix'
# Full screen or not
FULLSCR = True

# Background color
BGC = (0, 0, 0)

# Text color
TXTC = [-1,-1,-1]
# Text size
TXT_SIZE = 40
# Text font
FONT = u'DFKai-SB' # 標楷體
# Text position
MSG_POS = [0, 400]

# Stimuli size (default, pix)
STIM_SIZE = 130
# Size of option number
NUM_SIZE = 50

# position of the first item
POS1 = [-150, 130]
# position of the Arrow
arr_yPOS = 250
# position of the Question Mark
qm_xPOS = [-150, 0, 150, -70, 80, -70, 80] # (?)BC, A(?)C, AB(?), (?)B, A(?), (?)C, B(?)
# x-position of the items in the question
img_xPOSs = [[0, 150], [-150, 150], [-150, 0], [80], [-70], [80], [-70]]
# y-position of the items in the question
img_yPOS = 140
# x-position of the items in the options
opt_xPOS = -180
# y-position of the items in the options
opt_yPOS = [-50, -200, -350]

# Allowed keys ('esc' is kept as an abnormal response)
KETLIST_2 = ['1','2','escape', 'esc']
KETLIST_4 = ['1','2','3','4','escape', 'esc']
KETLIST_3 = ['1','2','3','escape', 'esc']

# Instructions (Chinese ver.) --------------------------------------------------
MSG_1 = '<< 第一階段，32題 >>'

TEST_INST_1 = '''
              \n方才您觀看了一連串的幾何圖形
              \n在大部分的階段中，這些圖形的呈現順序並不完全是隨機的

              \n在接下來的每個問題裡
              \n請您按鍵盤上的數字鍵，選擇最像是會一起 (先後) 出現的圖形組合
              \n選項上方的箭頭表示圖形呈現的時間順序

              \n**不知道答案的話，請您用直覺盡可能猜測**

              \n[按下空白鍵後開始測驗]
              '''
QUESTION_1 = '\n\n請按鍵盤上的數字鍵，選擇最像是會一起 (先後) 出現圖形組合。'

MSG_2 = '<< 第二階段，28題  >>'  

TEST_INST_2 = '''
              \n在接下來的每個問題裡，都會呈現一組幾何圖形
              \n而序列中的其中一個圖形會被置換成問號
              \n
              \n請您選擇問號處最可能出現的圖形
              \n請按鍵盤上的數字鍵進行選擇
              \n
              \n**不知道答案的話，請您用直覺盡可能猜測**
              \n
              \n
              \n[按下空白鍵後開始測驗]
              '''
QUESTION_2 = '\n\n請按鍵盤上的數字鍵，選擇問號處最可能出現的圖形。'

## Instructions (English ver.) -------------------------------------------------
# MSG_1 = ''
#
# TEST_INST_1 = '''
#               \nNow you will be tested on the order of the shapes you just saw.
#               \nIn each question, you will see few patterns of shapes.
#               \nYour goal is to choose the pattern that appeared together in the first phase of the experiment.
#               \nPlease make your choice by pressing the number keys on the keyboard.
#               \n
#               \n*If you do not know the answer - try to guess.
#               \n
#               \n[ Press 'space' to start the test ]
#               '''
#
# QUESTION_1 = '''\nPlease choose the pattern that appeared together in the first part (in the same order).
#                 \nPress the number corresponding to the option to give the answer.'''
#
# MSG_2 = ''
#
# TEST_INST_2 = '''
#               \nNow you will be shown a pattern of shapes, with one shape missing.
#               \nThe missing shape will be marked with a question mark.
#               \nYour goal is to choose the correct shape (from the options below) that completes the pattern.
#               \nPlease make your choice by pressing the number keys on the keyboard.
#               \n
#               \n*If you do not know the answer - try to guess.
#               \n
#               \n[ Press 'space' to start the test ]
#               '''
#
# QUESTION_2 = '''\nPlease choose a shape to complete the pattern.
#                 \nPress the number corresponding to the option to give the answer.'''
