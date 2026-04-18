#!/usr/bin/bash

PROJ_DIR=/media/data2/pinwei/VSL_new/fmri_exposure
SUBJ_DIRS=( \
	/media/data2/pinwei/SL_hippocampus/Dicom/PW??? \
	/media/data2/pinwei/SL_hippocampus/Dicom_slow/PW??? \
)
FOLDERS=( F2 F3 F4 F5 F6 F7 F8 F9 FMAP_RL FMAP_RL_P T1 T2 )

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

