#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd

top_dir = ".." # os.path.join("")
vsl_task_dir = os.path.join(top_dir, "my_VSL")
log_summ_file = os.path.join(vsl_task_dir, "logs", "jigg_task_perf_all.xlsx")

subjList = list(pd.read_csv('subjList.txt', header=None)[0])
subj_list = [ "{:03d}".format(int(subj.replace("sub-", ""))) for subj in subjList ]

run_list = [ "RUN_{:}".format(x) for x in range(1, 11) ]

log_summ = {}
HitRate_perSubj_acrossRuns = {}
HitRate_perRun_acrossSubjs = {}

for subj in subj_list:
    log_summ[subj] = pd.read_excel(log_summ_file, sheet_name=subj, 
                                   engine="openpyxl", index_col=0)
    HitRate_perSubj_acrossRuns[subj] = log_summ[subj].mean()["Hit_mean"]

for run in run_list:
    HitRate_list = [ log_summ[subj].T[run]["Hit_mean"] for subj in subj_list ]
    HitRate_perRun_acrossSubjs[run] = np.array(HitRate_list).mean()

HitRate_perRun_list = list(HitRate_perRun_acrossSubjs.values())
HitRate_perSubj_list = list(HitRate_perSubj_acrossRuns.values())

HitRate_perRun_mean = np.array(HitRate_perRun_list).mean()
HitRate_perSubj_mean = np.array(HitRate_perSubj_list).mean()