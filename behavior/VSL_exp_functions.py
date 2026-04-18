from psychopy import monitors, misc, visual, core, event
from math import floor
import random
import re

def set_stim_size(mon, DISP_SIZE, E_SCR_DIS, SCR_WIDTH, STIM_DEG):
    '''
    *Convert stimuli size from degree to pixel for the current monitor.
    '''
    mon.setSizePix(DISP_SIZE) # screen size (pix)
    mon.setDistance(E_SCR_DIS) # eye-screen distance (cm)
    mon.setWidth(SCR_WIDTH) # screen width (cm)
    STIM_SIZE = misc.deg2pix(STIM_DEG, mon) # convert the given degree to pixel

    return STIM_SIZE

def create_Triplets(shapes, Tpl_N):
    '''
    *Randomly assign loaded shapes into each triplet.
    *The number of shapes should be able to divide by 3 and match the number of triplets.

    <input>
    - shapes: [list] The file name of the shapes.
    - Tpl_N: [int] The number of triplets.

    <return> Triplets: [dict of lists] The four triplets.
    '''
    Triplets = {}
    random.shuffle(shapes)

    for n in range(len(shapes)):
        Tpl_Key = n%Tpl_N +1
        if Tpl_Key not in Triplets:
            Triplets[Tpl_Key] = []
        Triplets[Tpl_Key].append(shapes[n])

    return Triplets

def labeling_items(Triplets, IMG_FT):
    '''
    *Reversely labeling which triplet and order each item belongs to.

    <inputs>
    - Triplets: [dict of lists] The four triplets.
    - IMG_FT: [str] File type of the images.

    <return> item_label: [dict] {<shape>: [<triplet>, <order>]}
    '''
    shapes_key = re.findall('([\d]+).{}'.format(IMG_FT), str(Triplets.values()))
    item_label = {}
    count = 0
    for x in shapes_key:
        item_label.update({x: [count//3 +1, count%3 +1]})
        count += 1

    return item_label

def create_scan_stream(REPT_SC, shapes):
    '''
    *Shuffle the order of shapes to create 12 trials, repeat this procedure several times.
    *Shapes are NOT allowed to repeat immediately (A-A) or after another item (A-X-A).

    <return>
    - shape_stream: [list] The shape stream (file names) for the scanning phases.
    '''
    shape_stream = []
    random.shuffle(shapes)

    for x in range(REPT_SC):
        for shape in shapes:
            shape_stream.append(shape)
        last = shape_stream[-1]
        sec_last = shape_stream[-2]
        random.shuffle(shapes)
        while (shapes[0]==last) or (shapes[0]==sec_last) or (shapes[1]==last):
            random.shuffle(shapes)

    return shape_stream

def create_exposure_stream(REPT_EXP, Triplets, Tpl_keyList):
    '''
    *Determine the order of triplets first, and then generate the triplet stream.

    <returns>
    - shape_stream: [list] The shape stream (file names) for each exposure phase.
    - Tpl_order: [list] The order in which the triplets will be presented.
    - labels: [list] It is the 1st/2nd/3rd item.
    '''
    Tpl_order, labels, shape_stream = [''], [], []

    random.shuffle(Tpl_keyList)
    for x in range(REPT_EXP):
        for k in Tpl_keyList:
            Tpl_order.append(k) # triplets (1/2/3/4, int)
        last = Tpl_order[-1]
        random.shuffle(Tpl_keyList)
        while Tpl_keyList[0]==last:
            random.shuffle(Tpl_keyList)
    Tpl_order.remove('')

    for Tpl in Tpl_order:
        for idx in range(3):
            labels.append(idx+1) # index (1st/2nd/3rd, int)
            shape_stream.append(Triplets[Tpl][idx]) # shapes (1~12, file name)

    return shape_stream, Tpl_order, labels

def determine_ISIs(iN, ISIs, ISI_Ws):
    '''
    *Create a list of ISIs with fixed content (and shuffle it in each run)
     such that the ISIs vary randomly while the time length of each run remains the same.

    <inputs>
    - iN: [int] Number of intervals/ISIs.
    - ISIs: [list] The material set of the ISI list.
    - ISI_Ws: [list] Weights/Percentages of each ISI material.

    <return> ISI_list: [list] The ISI list.
    '''
    ISI_list = []
    for isi in ISIs: # For each possible ISI
        # Determine the number of the current ISI
        ciN = round(iN*ISI_Ws[ISIs.index(isi)], 0)
        # Add the ISI to the list to meet the determined number
        for c in range(int(ciN)):
            ISI_list.append(isi)
    n = 0
    while len(ISI_list) < iN: # If the length of the ISI list is less than expected,
        ISI_list.append(ISIs[n%3]) # (serially) add ISI to the list.
        n += 1

    return ISI_list

def assign_task_targets(tN, TARG_N):
    '''
    <inputs>
    - tN: Number of trials.
    - TARG_N: Number of targets.

    <return>
    - task: [list] A list of Booleans (0: non-targets, 1: targets)
    '''
    # Create a list of zeros (which indicates non-targets)
    task = [0 for x in range(tN -TARG_N)]
    # Insert the ones (which indicates targets) evenly
    for x in range(TARG_N):
        Tar = random.randint(floor((tN/TARG_N)*x)+1, floor((tN/TARG_N)*(x+1)))
        task.insert(Tar, 1)
            # Naturally, the first trial in each run won't be a task target

    return task

def jigg_stimuli(win, stim, c, STIM_TIME, MOVE_TIME, MOVE_DIS):
    '''
    <inputs>
    - win: [psychopy.visual.Window]
    - stim: [psychopy.visual.ImageStim]
    - c: [psychopy.Clock]
    - STIM_TIME: [float] Duration of the stimuli.
    - MOVE_TIME: [float] Duration of the rapid left/right movement.
    - MOVE_DIS: [float] Distance of the movement to the left/right.

    <return> t0: The onset time of the stimuli (secs)
    '''
    stim.autoDraw = True
    sub_MT = MOVE_TIME/8

    # move to the left:
    stim.pos = [-MOVE_DIS/2, 0]
    t0 = c.getTime() # get timestamp
    win.flip()
    core.wait(sub_MT)
    stim.pos = [-MOVE_DIS, 0]
    win.flip()
    core.wait(sub_MT*2)
    stim.pos = [-MOVE_DIS/2, 0]
    win.flip()
    core.wait(sub_MT)

    # move to the right:
    stim.pos = [MOVE_DIS/2, 0]
    win.flip()
    core.wait(sub_MT)
    stim.pos = [MOVE_DIS, 0]
    win.flip()
    core.wait(sub_MT*2)
    stim.pos = [MOVE_DIS/2, 0]
    win.flip()
    core.wait(sub_MT)

    # move back to the fixation:
    stim.pos = [0, 0]
    win.flip()
    core.wait(STIM_TIME - MOVE_TIME)

    stim.autoDraw = False

    return t0 # return the timestamp

def give_feedback(taskType, respKey, DOT_COLORs, FB_TIME, dot, win):
    '''
    *If correctly responded to a task target (=Hit),
     the color of the fixation dot will change to GREEN.
    *If incorrectly respond to a non-target (=False Alarm) or didn't respond to a task targets (=Miss),
     the color of the fixation dot will change to RED.
    *Otherwise, the color of the fixation dot won't change.
    '''
    if taskType == 1: # for targets
        if respKey is not None: # correctly responsded
            dot.color = DOT_COLORs[2]
            resp_catagory = 1 # Hit
        else:  # incorrect (i.e., didn't responded)
            dot.color = DOT_COLORs[1]
            resp_catagory = 0 # Miss
        dot.draw()
        win.flip()
        core.wait(FB_TIME)
    elif respKey is not None:  # incorrectly give response to non-target
        dot.color = DOT_COLORs[1]
        dot.draw()
        win.flip()
        core.wait(FB_TIME)
        resp_catagory = -1 # False Alarm
    else:
        resp_catagory = None
        core.wait(FB_TIME)
    dot.color = DOT_COLORs[0]
    dot.draw()
    win.flip()

    return resp_catagory

# def calculate_ISI(Run, Sti_On, Sti_Off):
#     '''
#     *Calculate inter-stimulus interval within each run
#      by subtracting the 'shutdown' timestamp of the previous stimuli
#      from the 'onset' timestamp of the current stimuli.
#     *ISI of the last trial is None.
#     '''
#     ISI = []
#     for x in set(Run):
#         tN = Run.count(x)
#         for n in range(tN-1):
#             ISI.append(round(Sti_On[n+1 + tN*(x-1)] - Sti_Off[n + tN*(x-1)], 3))
#         ISI.append(None)
#
#     return ISI

def calculate_ISI(Sti_On, Sti_Off):
    ISI = []
    for x in range(len(Sti_On)-1):
        ISI.append(round((Sti_On[x+1] - Sti_Off[x]), 3))
    ISI.append(None)
    return ISI

def task_response(df):
    return df['Task']*df['Press'] if df['Task']==1 else None

def calculate_dur(df):
    return df['Shut-down']-df['Show-up']

def event_name(df):
    Triplet_dict = {1:'A', 2:'B', 3:'C', 4:'D'}
    Label_dict = {1:'1st', 2:'2nd', 3:'3rd'}
    return Triplet_dict[df['Triplet']]+'-'+Label_dict[df['Label']]
