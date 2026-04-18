#!/usr/bin/tcsh

set BIDS_DIR = /media/data2/pinwei/VSL_new/fmri_exposure/Nifti
set SUBJS_DIR = $BIDS_DIR/derivatives/freesurfer
if ( ! -d $SUBJS_DIR ) mkdir -p $SUBJS_DIR

foreach subj_dir ( $BIDS_DIR/sub-*/ )
	set subj = `basename $subj_dir`
	
	if ( ! -d $SUBJS_DIR/$subj ) then
		recon-all -s $subj -all                  \
			-i $BIDS_DIR/$subj/anat/*T1w.nii.gz	 \
			-T2 $BIDS_DIR/$subj/anat/*T2w.nii.gz \
			-sd $SUBJS_DIR
			# https://surfer.nmr.mgh.harvard.edu/fswiki/recon-all#Arguments

		segmentHA_T2.sh $subj $SUBJS_DIR/$subj/mri/T2.norm.mgz T2+T1 1 $SUBJS_DIR
			# https://surfer.nmr.mgh.harvard.edu/fswiki/HippocampalSubfieldsAndNucleiOfAmygdala
	endif
end