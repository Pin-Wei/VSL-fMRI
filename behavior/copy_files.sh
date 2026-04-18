#!/usr/bin/bash

SRC_DIR=/media/data2/pinwei/SL_hippocampus/behavioral_data
DST_DIR=/media/data2/pinwei/VSL_new/behavior

FILES_PATHS=( \
	$SRC_DIR/VSL_*.py                             \
	$SRC_DIR/stimuli/*.png                        \
	$SRC_DIR/stimuli/png/*.png                    \
	$SRC_DIR/Trigger.py                           \
	$SRC_DIR/*ISI*                                \
	$SRC_DIR/Tpl_sort_scores.py                   \
	$SRC_DIR/Reconstruct_results.py               \
	$SRC_DIR/Report_jiggle_Hit.py                 \
	$SRC_DIR/familarity_test/*_test_result.xlsx   \
	$SRC_DIR/logs/*/*_jigg_task.xlsx              \
	$SRC_DIR/logs/*/*_logs.txt                    \
	$SRC_DIR/logs/*/*_sc_stream.csv               \
	$SRC_DIR/logs/*/*_triplets.xlsx               \
	$SRC_DIR/logs/*/sub-*_task-*_run-*_events.tsv \
)

for fp in ${FILES_PATHS[@]}; do
	dsc_dir=$(dirname "$fp" | sed "s|$SRC_DIR|$DST_DIR|")
	fn=$(basename "$fp")
	if [[ ! -d $dsc_dir ]]; then mkdir -p $dsc_dir; fi
	if [[ ! -f $dsc_dir/$fn ]]; then 
		cp $fp $dsc_dir
		echo "Copied files to $dsc_dir/$fn"
	fi
done
