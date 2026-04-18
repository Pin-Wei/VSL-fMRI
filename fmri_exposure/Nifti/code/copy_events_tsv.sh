#!/usr/bin/bash

TOP_DIR=/media/data2/pinwei/VSL_new
PROJ_DIR=$TOP_DIR/fmri_exposure
SUBJ_DIRS=( $TOP_DIR/behavior/logs/PW??? $TOP_DIR/behavior/logs/Slow??? )

sudo chmod -R 777 $PROJ_DIR/Nifti

for src_dir in ${SUBJ_DIRS[@]}; do
	subj=`basename $src_dir`
	sid=${subj: -3}
	dst_dir=$PROJ_DIR/Nifti/sub-${sid}/func
	file_paths=( $src_dir/sub-*_task-*_run-*_events.tsv )
	r_count=0
	
	for fp in ${file_paths[@]}; do
		fn=`basename $fp`
		run=$(echo $fn | grep -oE "run-[0-9]+" | sed s/run-//)
		r_num=$((10#$run))
		
		if [[ $r_num != 1 && $r_num != 10 ]]; then
			r_count=$(( $r_count + 1 ))
			run=`printf %02d $r_count`
			fn_new=sub-${sid}_task-VSL_run-${run}_events.tsv
			
			cp $fp $dst_dir
			mv $dst_dir/$fn $dst_dir/$fn_new
			echo "Copied files to $dst_dir/$fn_new"
		fi
	done
done


