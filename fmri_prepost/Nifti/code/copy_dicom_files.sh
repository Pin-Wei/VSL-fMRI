#!/usr/bin/bash

PROJ_DIR=/media/data2/pinwei/VSL_new/fmri_prepost
SUBJ_DIRS=( /media/data2/pinwei/SL_hippocampus/Dicom_slow/PW??? )
FOLDERS=( F1 F10 FMAP_RL FMAP_RL_P T1 T2 )

for src_dir in ${SUBJ_DIRS[@]}; do
	subj=`basename $src_dir`
	dst_dir=$PROJ_DIR/Dicom/$subj
	
	if [ ! -d $dst_dir ]; then mkdir -p $dst_dir; fi
	
	for folder in ${FOLDERS[@]}; do
		if [ ! -d $dst_dir/$folder ]; then 
			cp -r $src_dir/$folder $dst_dir
			echo "Copied files to $dst_dir/$folder"
		fi
	done
done
