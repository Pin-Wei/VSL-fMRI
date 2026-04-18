from __future__ import annotations

import logging
from typing import Optional

from heudiconv.utils import SeqInfo

lgr = logging.getLogger("heudiconv")


def create_key(
    template: Optional[str],
    outtype: tuple[str, ...] = ("nii.gz",),
    annotation_classes: None = None,
) -> tuple[str, tuple[str, ...], None]:
    if template is None or not template:
        raise ValueError("Template must be a valid format string")
    return (template, outtype, annotation_classes)


def infotodict(
    seqinfo: list[SeqInfo],
) -> dict[tuple[str, tuple[str, ...], None], list[str]]:
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """
    T1w = create_key('sub-{subject}/anat/sub-{subject}_T1w')
    T2w = create_key('sub-{subject}/anat/sub-{subject}_T2w')
    func = create_key('sub-{subject}/func/sub-{subject}_task-VSL_run-{item:02d}_bold')
    fmap_mag = create_key('sub-{subject}/fmap/sub-{subject}_acq-RL_magnitude')
    fmap_phase = create_key('sub-{subject}/fmap/sub-{subject}_acq-RL_phasediff')
    info: dict[tuple[str, tuple[str, ...], None], list[str]] = {
        T1w: [], T2w: [], func: [], fmap_mag: [], fmap_phase: []
    }

    for s in seqinfo:
        """
        The namedtuple `s` contains the following fields:

        * total_files_till_now
        * example_dcm_file
        * series_id
        * dcm_dir_name
        * unspecified2
        * unspecified3
        * dim1
        * dim2
        * dim3
        * dim4
        * TR
        * TE
        * protocol_name
        * is_motion_corrected
        * is_derived
        * patient_id
        * study_description
        * referring_physician_name
        * series_description
        * image_type
        """
        if ('T1' in s.dcm_dir_name):
            info[T1w].append(s.series_id)

        elif ('T2' in s.dcm_dir_name):
            info[T2w].append(s.series_id)

        elif ('bold' in s.protocol_name):
            info[func].append(s.series_id)

        elif ('FMAP_RL' in s.dcm_dir_name):
            if ('M' in s.image_type):
                info[fmap_mag].append(s.series_id)
            elif ('P' in s.image_type):
                info[fmap_phase].append(s.series_id)
                
    return info
