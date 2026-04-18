#!/usr/bin/bash

PROJ_DIR=/media/data2/pinwei/VSL_new/fmri_prepost
VER=$1
MSG="Please specify the version of execution (1: first time, 2: after modifying heuristic.py)."

if [ -z "$VER" ]; then
    echo "Error: missing argument."
	echo $MSG
	exit 1
fi

case $VER in
	1) 
		for subj_dir in $PROJ_DIR/Dicom/PW??? ; do
			subj=`basename $subj_dir`
			sid=`echo $subj | sed "s/PW//g"`

			docker run -it --rm                        \
				-v ${PROJ_DIR}:/base                   \
				nipy/heudiconv:latest                  \
					-d /base/Dicom/PW{subject}/*/*.IMA \
					-o /base/Nifti/                    \
					-f convertall                      \
					-s $sid                            \
					-c none                            \
					--overwrite
			
		done

		if [ -f $PROJ_DIR/Nifti/code/heuristic.py ]; then 
			cp $PROJ_DIR/Nifti/.heudiconv/$sid/info/heuristic.py .
			cp $PROJ_DIR/Nifti/.heudiconv/$sid/info/dicominfo.tsv .
		fi
		if [ -f $PROJ_DIR/Nifti/code/heuristic.py ]; then sudo rm -r $PROJ_DIR/Nifti/.heudiconv; fi
		;;
	2) 
		for subj_dir in $PROJ_DIR/Dicom/PW??? ; do
			subj=`basename $subj_dir`
			sid=`echo $subj | sed "s/PW//g"`
			
			docker run -it --rm                        \
				-v ${PROJ_DIR}:/base                   \
				nipy/heudiconv:latest                  \
					-d /base/Dicom/PW{subject}/*/*.IMA \
					-o /base/Nifti                     \
					-f /base/Nifti/code/heuristic.py   \
					-s $sid                            \
					-c dcm2niix -b                     \
					--overwrite

		done
		;;
	*)
		echo "Error: invalid argument."
		echo $MSG
		exit 1
		;;
esac