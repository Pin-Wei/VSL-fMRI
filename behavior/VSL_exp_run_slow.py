print("\nLoading packages...")

from psychopy import visual, core, event, monitors
from math import floor
from glob import glob
import pandas as pd
import random
import re
import sys
import time
import os

from VSL_exp_constants import *
import VSL_exp_functions as myFunc

# Subj_ID = int(input("\nID number: ")) # Input participant's ID number
Subj_ID = int(sys.argv[1])
PATH = 'logs//Slow{:03d}//'.format(Subj_ID)
if not os.path.isdir(PATH):
    os.mkdir(PATH)

R = int(sys.argv[2]) # Append number of run on the commandline arguments
c = core.Clock()
c.reset()
time_info = time.localtime()

if R==1:
    # loading the 12 stimulus
    shapes = glob('stimuli/png/*.{}'.format(IMG_FT))
    shapes = [x for x in shapes if re.findall('([\d]+).[\w]{3}$', x) != []]

    # Create 4 triplets for each participant
    Triplets = myFunc.create_Triplets(shapes, 4)
    item_label = myFunc.labeling_items(Triplets, IMG_FT) # {'shape ID': [Tpl_ID, label],...}

    ## Save the triplets to file
    pd.DataFrame.from_dict(Triplets).to_excel(PATH +'{:03d}_triplets.xlsx'.format(Subj_ID), index=False)

    # Create a (same) shape stream for the pre/post-exposure phase
    scan_stream = myFunc.create_scan_stream(REPT_SC, shapes)
    sc_Tpl_order, sc_labels = [], []
    for x in re.findall('([\d]+).{}'.format(IMG_FT), ''.join(scan_stream)):
        sc_Tpl_order.append(item_label[x][0])
        sc_labels.append(item_label[x][1])

    ## Save the scanning stream to file
    sc_stream_DF = pd.DataFrame({'Shape':scan_stream,
                                 'Triplet':sc_Tpl_order,
                                 'Label':sc_labels})
    sc_stream_DF.to_csv(PATH +'{:03d}_sc_stream.csv'.format(Subj_ID), index=False)
    MODE = 'w'

else:
    Triplets = pd.read_excel(PATH +'{:03d}_triplets.xlsx'.format(Subj_ID), engine='openpyxl').to_dict(orient='list')
    sc_stream_DF = pd.read_csv(PATH +'{:03d}_sc_stream.csv'.format(Subj_ID)).to_dict(orient='list')
    MODE = 'a'

# Setting the environment ------------------------------------------------------
mon = monitors.Monitor('mylaptop') # create a monitor object

win = visual.Window(monitor=mon, size=DISP_SIZE, color=BGC,
                    fullscr=FULLSCR, allowGUI=False, units=UNIT)

msg = visual.TextStim(win, text='', pos=(0,0), color=TXTC,
                      height=(FONT_SIZE), wrapWidth=DISP_SIZE[1]*2)
msg.autoDraw = True
msg.autoLog = True

dot = visual.Circle(win, radius=DOT_SIZE, lineColor=None, fillColor=DOT_COLORs[0])
dot.autoLog = True

# STIM_SIZE = myFunc.set_stim_size(mon, DISP_SIZE, E_SCR_DIS, SCR_WIDTH, STIM_DEG)
stim = visual.ImageStim(win, image=None, pos=[0,0], size=STIM_SIZE)
stim.autoLog = True

# Invisible the mouse
event.Mouse(visible=False)

# Initialize the parameters
Tpl_Key, Tpl_Seq, Item, Trig_Time, Sti_On, Sti_Off, Task, Press, RT, Hit = [], [], [], [], [], [], [], [], [], []
Tpl_keyList = list(Triplets.keys()) # [1, 2, 3, 4]

# Experiment START =============================================================
try:
    if R==1: # pre-exposure phase
        msg.setText("Welcome")
        win.flip()
        core.wait(1)

        msg.setText(EXP_INST) # instruction
        msg.font = FONT_2
        win.flip()
        event.waitKeys(keyList=['space'])

    # Generate the shape stream
        shape_stream = scan_stream
        Tpl_order = sc_Tpl_order
        labels = sc_labels
        ISI_list = [9 for x in range(3*4*REPT_SC)]

    elif R==10: # post-exposure phase
        shape_stream = sc_stream_DF['Shape']
        Tpl_order = sc_stream_DF['Triplet']
        labels = sc_stream_DF['Label']
        ISI_list = [9 for x in range(3*4*REPT_SC)]

    else: # exposure phase
        shape_stream, Tpl_order, labels = myFunc.create_exposure_stream(REPT_EXP, Triplets, Tpl_keyList)
        ISI_list = list(pd.read_csv('exp_ISI_unshuffled.csv',header=None, squeeze=True))

    msg.setText('')
    msg.font = FONT_1
    dot.draw()
    win.flip()

    # Determine the targets
    tN = len(shape_stream)
    task = myFunc.assign_task_targets(tN, int(tN//TARG_PER)) # (number of trials, number of targets)

    # Shuffle the order of the ISI_list
    if R not in [1, 10]:
        random.shuffle(ISI_list)
        ISI_list.append(1)

    # c.reset()

    # Start each trial ---------------------------------------------------------
    for x in range(len(shape_stream)):
        # Update image stimuli
        item = shape_stream[x]
        stim.setImage(item)

        # Wait for trigger
        event.waitKeys(keyList=TRIG_KEYLIST)
        trig_time = c.getTime()

        # Present the stimuli
        if (task[x] == 1): # target
            t0 = myFunc.jigg_stimuli(win, stim, c, (STIM_TIME-STIM_corr_j),
                                     MOVE_TIME, MOVE_DIS)
        else: # non-target
            stim.draw()
            t0 = c.getTime()
            win.flip()
            core.wait(STIM_TIME-STIM_corr_nj)

        # Erase the stimuli
        if R in [1, 10]:
            core.wait(SLOW)
        t1 = c.getTime()
        win.flip()

        # Capture the response
        resp = event.getKeys(keyList=RESP_KEYLIST, timeStamped=c)
        k_resp = [resp[0][0] if resp!=[] else None]
        t_resp = [resp[0][1] if resp!=[] else None]

        # Interrupt the experiment if pressed 'esc'
        if k_resp[0] in ESC_KEYLIST:
            raise Exception

        # Give feedback
        resp_catagory = myFunc.give_feedback(task[x], k_resp[0], DOT_COLORs, FB_TIME, dot, win)
        Hit.append(resp_catagory)

        # Save logs
        if (R==1) or (R==10):
            Tpl_Key.append(Tpl_order[x])
        else:
            Tpl_Key.append(Tpl_order[x//3])
        Tpl_Seq.append(labels[x])
        Item.append(int(re.findall('([\d]+).[\w]{3}$', item)[0]))
        Trig_Time.append(trig_time)
        Sti_On.append(t0) # timestamp when stimuli is appear
        Sti_Off.append(t1) # timestamp when stimuli is disappear
        Task.append(task[x]) # whether each stimuli is jiggled or not (1:True /0:False)
        Press.append(1 if k_resp[0] is not None else 0)
        RT.append(t_resp[0]-t0 if t_resp[0] is not None else None) # reaction time

        # Inter-stimulus interval
        core.wait(ISI_list[x] -FB_TIME -ISI_corr)

    last_event = time.localtime()

    if R not in [1, 10]:
        event.waitKeys(keyList=TRIG_KEYLIST)
        event.waitKeys(keyList=TRIG_KEYLIST)
        event.waitKeys(keyList=TRIG_KEYLIST)

    msg.setText('第 {} 回合已完成'.format(R))
    msg.font = FONT_2
    win.flip()
    core.wait(1)

# Experiment END ===============================================================

except:
    msg.setText("Quiting the experiment...")
    win.flip()
    core.wait(1)
    print('\nThe experiment is interrupted!')

finally:
    win.close()

    ISI = myFunc.calculate_ISI(Sti_On, Sti_Off) # Calculate real ISI
    if len(ISI_list) >= len(ISI):
        ISI_list = ISI_list[:len(ISI)]
    # else:
    #     ISI_list.append(None)
    Data = pd.DataFrame({'Triplet':Tpl_Key, 'Label':Tpl_Seq, 'Item':Item,
                         'Trigger':Trig_Time, 'Show-up':Sti_On, 'Shut-down':Sti_Off,
                         'ISI':ISI, 'Theoretical-ISI':ISI_list,
                         'Task':Task, 'Press':Press, 'RT':RT})
    Data['Hit'] = Data.apply(myFunc.task_response, axis=1) # Identify hit trials

    # Save an excel log file
    with pd.ExcelWriter(PATH +'{:03d}_{:}.xlsx'.format(Subj_ID, TASK), engine='openpyxl',
                        mode=MODE, if_sheet_exists='new') as writer:
        Data.to_excel(writer, sheet_name='RUN_{}'.format(R), index=False)

    # Save event_onset.tsv files
    Onset = Data['Show-up']-Data['Trigger'][0]
    Duration = Data.apply(myFunc.calculate_dur, axis=1)
    Event = Data.apply(myFunc.event_name, axis=1)
    # Triplet_dict = {1:'A', 2:'B', 3:'C', 4:'D'}
    # Label_dict = {1:'1st', 2:'2nd', 3:'3rd'}
    # Event1 = Data.Triplet.apply(lambda x: Triplet_dict[x])
    # Event2 = Data.Label.apply(lambda x: Label_dict[x])
    EventOnset = pd.DataFrame({'onset':Onset, 'duration':Duration,
                               'trial_type':Event,
                               # 'trial_type-triplet':Event1, 'trial_type-label':Event2,
                               'task':Task, 'stim_file':Item})
    EventOnset = EventOnset[EventOnset['task']==0]
    EventOnset = EventOnset.drop('task', axis=1)
    EventOnset.to_csv(PATH +'//sub-{:03d}_task-slowVSL_run-{:02d}_events.tsv'.format(Subj_ID, R), sep='\t', index=False)

    with open (PATH +'{:03d}_runTime.txt'.format(Subj_ID), MODE) as fn3:
        if R==1:
            fn3.writelines(time.strftime('%Y/%m/%d %z', time_info))
            fn3.writelines(', subject ID: {:03d}'.format(Subj_ID))
        fn3.writelines('\n\n'+ time.strftime('%H:%M:%S', time_info))
        fn3.writelines(' start RUN-{}'.format(R))
        fn3.writelines('\nstimuli event end at '+ time.strftime('%H:%M:%S', last_event))

    print('\nThe data is saved!')
