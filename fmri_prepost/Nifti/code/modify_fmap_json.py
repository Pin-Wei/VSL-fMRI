#!/usr/bin/env python

# This script modifies the phasediff.json files in the fmap directories of a BIDS dataset.
# It adds the "IntendedFor" field, which lists the functional NIfTI files that the fieldmap is intended to correct
# and the "B0FieldIdentifier" field to specify the type of fieldmap.

# This script has to be run as root 
# Usage: sudo python modify_fmap_json.py

# Should be run before running fMRIprep

import os
import json
import glob

fmap_jsons = glob.glob(os.path.join("..", "sub-*", "fmap", "*_phasediff.json"))
fmap_jsons = sorted(fmap_jsons)

for fmap_json in fmap_jsons:
    subj = os.path.basename(fmap_json).split("_")[0] 
    func_niis = glob.glob(os.path.join("..", subj, "func", "*.nii*"))
    func_niis = sorted(func_niis)

    with open(fmap_json) as f:
        fmap_data = json.load(f)

    fmap_data["IntendedFor"] = func_niis
    fmap_data["B0FieldIdentifier"] = "phasediff_fmap0"

    with open(fmap_json, "w") as f:
        json.dump(fmap_data, f, indent=2, sort_keys=True)

    for func in func_niis:
        func_json = func.replace(".nii.gz", ".json")

        with open(func_json) as f:
            func_data = json.load(f)

        func_data["B0FieldSource"] = "phasediff_fmap0"

        with open(func_json, "w") as f:
            json.dump(func_data, f, indent=2, sort_keys=True)

    print(f"Updated json files for {subj}.")

