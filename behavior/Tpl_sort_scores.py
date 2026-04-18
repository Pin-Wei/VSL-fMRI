#!/usr/bin/env python
# coding: utf-8

import os
import re
import glob
import numpy as np
import pandas as pd

fd = '/media/data1/pinwei/SL_hippocampus/behavioral_data/familarity_test'
# fd = 'familarity_test'
path_list = sorted(glob.glob(os.path.join(fd, '*_test_result.xlsx')))
subj_list = sorted([re.findall('([\d]+)', path)[0] for path in path_list])

tpl_score_4each1, sorted_tpl_4each1, sorted_score_4each1 = {}, {}, {}

for sid, fpath in zip(subj_list, path_list):
    tpl_score_4each1[sid] = {}
    data = pd.read_excel(fpath, engine='openpyxl')

    for t, tpl in enumerate(['A', 'B', 'C', 'D']):
        tpl_score_4each1[sid][tpl] = sum(data[data['Triplet_ID'] == t+1]['correct'])

    sorted_tuple = sorted(tpl_score_4each1[sid].items(), key=lambda x: x[1], reverse=True)
    sorted_tpl = [tpl for tpl, score in sorted_tuple]
    sorted_tpl_4each1[sid] = sorted_tpl
    sorted_score = [score for tpl, score in sorted_tuple]
    sorted_score_4each1[sid] = sorted_score

tpl_score_4each1 = pd.DataFrame(tpl_score_4each1).T
tpl_score_4each1["STD"] = tpl_score_4each1.T.apply(np.std)
tpl_score_4each1.to_csv(os.path.join(fd, 'Score_foreach_triplet.csv'))

pd.DataFrame(sorted_tpl_4each1).T.to_csv(os.path.join(fd, 'Triplets_sortby_score.csv'), header=False)
pd.DataFrame(sorted_score_4each1).T.to_csv(os.path.join(fd, 'Sorted-score_foreach_triplet.csv'), header=False)

