from psychopy import visual
import random
import re
import numpy as np

def setup_positions(pos1, col_N, row_N, c_spacing, r_spacing):
    '''
    <inputs>
    - pos1: [x,y] The starting position.
    - col_N, row_N: [int] The number of columns/rows.
    - c_spacing, r_spacing: [int] Column/row spacing distance.

    <return> A list of [x,y] positions.
    '''
    Positions = []
    for R in range(row_N): # append by rows
        for C in range(col_N):
            Positions.append([pos1[0]+c_spacing*C, pos1[1]-r_spacing*R])
    return Positions

def create_choices(TID_list, target_TID, item_N, choice_N):
    '''
    <inputs>
    - TID_list: [list] The shuffled triplets' key list.
    - target_TID: [list] A list of target-triplet's key.

    <return>
    - choices_TIDs: [list of lists] List of triplets' key of each choices.
    - choices_labels: [list of lists] List of item label (of triplet) of each choices.
    - corr_opt: [int] The number of the correct option.
    '''
    # *Foil is created by randomly combining items in different triplets
    choices_TIDs, choices_labels = [], []
    while len(choices_TIDs) < choice_N-1: # number of Foils
        foil = random.sample(TID_list, k=item_N) # random sampling without duplication
        if foil not in choices_TIDs:
            choices_TIDs.append(foil)
            choices_labels.append(random.choices([0, 1, 2], k=3))

    corr_opt = random.randint(1, choice_N) # the correct option
    choices_TIDs.insert(corr_opt-1, target_TID)
    choices_labels.insert(corr_opt-1, [0, 1, 2])

    return choices_TIDs, choices_labels, corr_opt

def setup_question(Triplets, choices_TIDs, choices_labels, item_N, choice_N, POSs, opt_xPOS, num, stim, pair_order):
    c = 0 # count
    choices_items = [[]]

    for m in range(choice_N):
        num.setText('('+ str(c//item_N +1) +')') # option numbers
        num.pos = [opt_xPOS, POSs[c][1]]
        num.draw()

        for n in range(item_N):
            item = Triplets[choices_TIDs[m][n]][choices_labels[m][n+pair_order]]
            choices_items[c//item_N].append(int(re.findall('([\d]+).[\w]{3}$', item)[0]))
            stim.setImage(item)
            stim.pos = POSs[c]
            stim.draw()
            c += 1

        choices_items.append([])
    del choices_items[-1] # the final '[]'

    return choices_items

def create_choices_2(TID_list, T_ID, t_label, opt_N):

    choices_TIDs = random.sample(TID_list, k=opt_N-1) # foils
    corr_opt = random.randint(1, opt_N) # target
    choices_TIDs.insert(corr_opt-1, T_ID)
    choices_labels = [random.randint(0, 2) for x in range(opt_N-1)]
    choices_labels.insert(corr_opt-1, t_label)
    choices_labels_ = [[x] for x in choices_labels]

    return choices_TIDs, choices_labels_, corr_opt

def setup_question_2(Triplets, TID_list, T_ID, qm, num, stim, img_labels, t_label, qm_xPOS, img_xPOSs, img_yPOS, opt_xPOS, opt_yPOSs, opt_N):
    '''
    <inputs>
    - T_ID: [int] Target triplet's key.
    - qm, num, stim: [object]*
    - img_labels: [list of int] Label(s) of the given shapes in the question.
    - t_label: [int] Label of the target (where qm is placed) in each question type
    - opt_N: [int] Number of options/choices.
    '''
    choices_TIDs, choices_labels, corr_opt = create_choices_2(TID_list, T_ID, t_label, opt_N)
    choices_items = []

    # Draw the question mark
    qm.pos = [qm_xPOS, img_yPOS]
    qm.draw()

    # Draw ImageStim of the question
    for n in range(len(img_labels)):
        stim.setImage(Triplets[T_ID][img_labels[n]])
        stim.pos = [img_xPOSs[n], img_yPOS]
        stim.draw()

    # Draw options' number and ImageStim
    for n in range(opt_N):
        num.setText('('+ str(n+1) +')') # option numbers
        num.pos = [opt_xPOS, opt_yPOSs[n]]
        num.draw()

        item = Triplets[choices_TIDs[n]][choices_labels[n][0]]
        stim.setImage(item)
        stim.pos = [opt_xPOS +130, opt_yPOSs[n]]
        stim.draw()
        choices_items.append([int(re.findall('([\d]+).[\w]{3}$', item)[0])])

    return choices_items, choices_labels, corr_opt

def check_pos_viol(choices_labels, corr_opt, item_N):
    pos_viols, viol_degs = [], []
    ref_labels = choices_labels.pop(corr_opt-1)
    # ref_labels = choices_labels[corr_opt-1]
    for foil_labels in choices_labels:
        pos_is_diff = [1 if foil_labels[x]!=ref_labels[x] else 0 for x in range(item_N)]
        pos_viols.append(pos_is_diff)
        viol_degs.append(np.average(pos_is_diff))
        viol_deg = round(np.average(viol_degs), 2)

    return pos_viols, viol_deg

def select_target(df):
    return df['Foils'].pop(df['Answer']-1)

def checking_answer(df):
    return 1 if df['Response'] == df['Answer'] else 0
