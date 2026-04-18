print("\nLoading packages...")
from psychopy import visual, core, event
import pandas as pd
import numpy as np
import random

from VSL_test_constants import *
import VSL_test_functions as myFunc

Subj_ID = input("\nInput participant's ID number (3d): ")
if Subj_ID[0] == '0': #Rapid event-related
    Tpl_FN = 'PW'+Subj_ID+'//'+Subj_ID+'_triplets.xlsx'
elif Subj_ID[0] == 'l':
    Tpl_FN = 'Slow'+Subj_ID+'//'+Subj_ID+'_triplets.xlsx'
else:
    PREFIX = input("\nInput prefix: ")
    Tpl_FN = PREFIX+Subj_ID+'//'+Subj_ID+'_triplets.xlsx'
Triplets = pd.read_excel('logs//{:}'.format(Tpl_FN), engine='openpyxl')
TID_list = list(Triplets) # triplets' ID list
FN = 'test_result' # default, change if be interrupted

## Setting the environment -----------------------------------------------------
win = visual.Window(monitor='mylaptop', size=DISP_SIZE, color=BGC,
                    fullscr=FULLSCR, allowGUI=False, units=UNIT)

msg = visual.TextStim(win, text='', color=TXTC, font=FONT,
                      height=(TXT_SIZE), wrapWidth=DISP_SIZE[1]*2)
msg.autoLog = True
msg.autoDraw = True

num = visual.TextStim(win, text='', color=TXTC, height=(NUM_SIZE), bold=True) # option numbers
num.autoLog = True

stim = visual.ImageStim(win, image=None, pos=[0, 0], size=STIM_SIZE)
stim.autoLog = True

qm = visual.ImageStim(win, image='stimuli/qm.png', pos=[0, img_yPOS], size=STIM_SIZE)
qm.autoLog = True

arrow = visual.ImageStim(win, image='stimuli/arrow.png', pos=[0, arr_yPOS])

## Setting the questions -------------------------------------------------------

## PART-1: AFC tests ##
## test order: (2-AFC Triplet)x2, (4-AFC Triplet)x2, (2-AFC Pair)x(1st/2nd), (4-AFC Pair)x(1st/2nd)
item_N = [3, 3, 2, 2]
tpl_types = ['Triplet','Triplet','Pair','Pair']
choice_N = [2, 4, 2, 4]
key_list = [KETLIST_2, KETLIST_4, KETLIST_2, KETLIST_4]

## PART-2: Fill in the blank ##
# question types
Q_types = ['(?)BC','A(?)C','AB(?)','(?)B','A(?)','(?)C','B(?)']
tpl_types_2 = ['Triplet','Triplet','Triplet','1st Pair','1st Pair','2nd Pair','2nd Pair']
# labels of the given shapes
img_labels = [[1, 2], [0, 2], [0, 1], [1], [0], [2], [1]] # [[B, C], [A, C], [A, B], [B], [A], [C], [B]]
# label of the target shape (to-be-answered)
t_labels = [0, 1, 2, 0, 1, 1, 2] # [A, B, C, A, B, B, C]
# option numbers
opt_N = 3

## Test START ==================================================================

# Initialize the parameters
Item_type, Que_type, Target_TID, Choices, Pos_Viol, Viol_Deg, Answer, Response, tpl_ID = [], [], [], [], [], [], [], [], 5

# Invisible the mouse
event.Mouse(visible=False)

try:
    ## First part: AFC tests ---------------------------------------------------
    msg.setText(MSG_1)
    win.flip()
    core.wait(0.5)

    msg.setText(TEST_INST_1)
    win.flip()
    event.waitKeys(keyList=['space', 'enter'])

    msg.setText(QUESTION_1)
    msg.pos = MSG_POS
    arrow.autoDraw = True

    for x in range(4): # 2-AFC Triplet, 4-AFC Triplet, 2-AFC Pair, 4-AFC Pair
        POSs = myFunc.setup_positions(pos1=POS1, col_N=item_N[x], row_N=choice_N[x],
                                      c_spacing=150, r_spacing=150)

        for run in range(2): # x2, x2, x(1st/2nd), x(1st/2nd)

            random.shuffle(TID_list)
            while TID_list[0] == tpl_ID:
                random.shuffle(TID_list)
                # Compare the first triplet of the current list
                    # to the last questioned triplet (default=5)
                        # to avoid asking same triplet consecutively.

            for tpl_ID in TID_list:
                target_TIDs = [tpl_ID for count in range(item_N[x])]
                    # (e.g. =[1, 1, 1] when tpl_ID =1 and item_N =3)

                pair_order = (3-item_N[x])*run
                    # Only needed when testing pairs (=0 when item_N=3),
                        # testing the 1st pair in the run-1, 2nd pair in the run-2.

                choices_TIDs, choices_labels, corr_opt = myFunc.create_choices(TID_list, target_TIDs, item_N[x], choice_N[x])
                Answer.append(corr_opt)

                choices_items = myFunc.setup_question(Triplets, choices_TIDs, choices_labels,
                                                      item_N[x], choice_N[x], POSs, -280,
                                                      num, stim, pair_order)
                Choices.append(choices_items)
                win.flip()

                resp = event.waitKeys(keyList=key_list[x])
                # if event.getKeys(keyList=['escape', 'esc']):
                #     raise Exception
                Response.append(int(resp[0]))
                win.flip()
                core.wait(0.3)

                Item_type.append(tpl_types[x])
                Que_type.append(str(choice_N[x]) + '-AFC_' + str(run+1))
                Target_TID.append(tpl_ID)

                pos_viols, viol_deg = myFunc.check_pos_viol(choices_labels, corr_opt, item_N[x])
                Pos_Viol.append(pos_viols)
                Viol_Deg.append(viol_deg)


    arrow.autoDraw = False

    ## Second part: fill in the blank ------------------------------------------
    msg.setText(MSG_2)
    msg.pos = [0, 0]
    win.flip()
    core.wait(0.5)

    msg.setText(TEST_INST_2)
    win.flip()
    event.waitKeys(keyList=['space', 'enter'])

    msg.setText(QUESTION_2)
    msg.pos = MSG_POS
    arrow.autoDraw = True

    # Shuffle the order of question types
    Q_order_tpl = [0, 1, 2]  # '(?)BC', 'A(?)C', 'AB(?)'
    random.shuffle(Q_order_tpl)
    Q_order_pr = [3, 4, 5, 6]  # '(?)B', 'A(?)', '(?)C', 'B(?)'
    random.shuffle(Q_order_pr)
    Q_order = Q_order_tpl + Q_order_pr

    for x in Q_order:
        random.shuffle(TID_list)
        while TID_list[0] == Target_TID[-1]:
            random.shuffle(TID_list)

        for T_ID in TID_list:
            TID_list2 = TID_list.copy()
            TID_list2.remove(T_ID)
            choices_items, choices_labels, corr_opt = myFunc.setup_question_2(Triplets, TID_list2, T_ID, qm, num, stim,
                                                                              img_labels[x], t_labels[x], qm_xPOS[x],
                                                                              img_xPOSs[x], img_yPOS, opt_xPOS, opt_yPOS, opt_N)
            win.flip()
            Answer.append(corr_opt)
            Choices.append(choices_items)

            resp = event.waitKeys(keyList=KETLIST_3)
            # if event.getKeys(keyList=['escape', 'esc']):
            #     raise Exception
            Response.append(int(resp[0]))
            win.flip()
            core.wait(0.3)

            Item_type.append(tpl_types_2[x])
            Que_type.append(Q_types[x])
            Target_TID.append(T_ID)

            pos_viols, viol_deg = myFunc.check_pos_viol(choices_labels, corr_opt, 1)
            Pos_Viol.append(pos_viols)
            Viol_Deg.append(viol_deg)

# ==============================================================================
except:
    print('\n<<< Test escaped >>>\n')
    Choices.pop(-1)
    Answer.pop(-1)
    FN = 'test_interrupted'

finally:
    win.close()
    Data = pd.DataFrame({'Triplet_Pair':Item_type, 'Question_type':Que_type,
                         'Triplet_ID':Target_TID, 'Foils':Choices,
                         'Position_violation':Pos_Viol, 'Violation_degree':Viol_Deg,
                         'Answer':Answer, 'Response':Response})
    # Data.insert(1, 'Triplet_Pair', Data.Item_type.apply(lambda x: 'Triplet' if x==3 else 'Pair'))
    Data.insert(3, 'Target', Data.apply(myFunc.select_target, axis=1))
    Data['correct'] = Data.apply(myFunc.checking_answer, axis=1)

    # Saving to excel
    Data.to_excel('familarity_test//{:}_{:}.xlsx'.format(Subj_ID, FN), index=False)
    print('\nThe data is saved!')
