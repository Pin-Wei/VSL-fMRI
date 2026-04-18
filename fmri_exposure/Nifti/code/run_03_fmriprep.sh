#!/usr/bin/tcsh

set BIDS_DIR = /media/data2/pinwei/VSL_new/fmri_exposure/Nifti
set FS_DIR   = $BIDS_DIR/derivatives/freesurfer
set PREP_DIR = $BIDS_DIR/derivatives/fmriprep
set POST_DIR = $BIDS_DIR/derivatives/post_aroma
set WORK_1   = $BIDS_DIR/../work/fmriprep
set WORK_2   = $BIDS_DIR/../work/post_aroma

foreach dir ( $PREP_DIR $POST_DIR $WORK_1 $WORK_2 )
	if ( ! -d $dir ) mkdir -p $dir
end

set FS_LICENSE = "/usr/local/freesurfer/license.txt"

if ( $#argv == 0 ) then
    set SUBJ_DIRS = ( $BIDS_DIR/sub-*/ )
else if ( $#argv > 1 ) then
    echo "Error: Too many arguments provided."
    exit 1
else if ( "$1" !~ [0-9]* ) then
    echo "Error: Argument should be a subject ID number."
    exit 1
else
	set sid = `printf %03d $1`
	set SUBJ_DIRS = ( $BIDS_DIR/sub-${sid}/ )
endif

foreach subj_dir ( ${SUBJ_DIRS[*]} )
	set subj = `basename $subj_dir`
	set sid = `echo $subj | sed "s/sub-//g"`
	
	if ( ! -d $PREP_DIR/$subj ) then
	
		docker run -it --rm                              \
			-v ${BIDS_DIR}:/data:ro                      \
			-v ${PREP_DIR}:/out                          \
			-v ${WORK_1}:/work                           \
			-v ${FS_LICENSE}:/opt/freesurfer/license.txt \
			nipreps/fmriprep:latest                      \
				/data /out participant                   \
				--participant-label $sid                 \
				--skip_bids_validation                   \
				--output-spaces T1w MNI152NLin2009cAsym MNI152NLin6Asym:res-02 \
				--fs-subjects-dir ${FS_DIR}              \
				--ignore fieldmaps                       \
				--stop-on-first-crash                    \
				--nthreads 10                            \
				--omp-nthreads 10                        \
				-w /work
				# https://www.nipreps.org/apps/docker/#running-a-niprep-with-a-lightweight-wrapper
	
		docker run -it --rm              \
			-v ${BIDS_DIR}:/data:ro      \
			-v ${PREP_DIR}:/prep         \
			-v ${POST_DIR}:/out          \
			-v ${WORK_2}:/work           \
			nipreps/fmripost-aroma:main  \
				/data /out participant   \
				--participant-label $sid \
				-t "srttprob"            \
				--skip_bids_validation   \
				-d fmriprep=/prep        \
				--nthreads 10            \
				--omp-nthreads 10        \
				-w /work
				# https://fmripost-aroma.readthedocs.io/latest/usage.html
				
	endif
end