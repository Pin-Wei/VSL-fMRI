# Visual Statistical Learning (VSL) Task
These scripts are used to run the VSL task performed by participants during fMRI scans. The experiment investigates how the human brain incidentally learns temporal regularities between abstract visual stimuli.

### Task Overview
- **Stimuli**: Twelve solid black abstract geometric shapes.
- **Structure**: These shapes are organized into four "triplets" (sequences of three shapes). While the triplets appear in a pseudo-randomized stream, the internal order of shapes within a triplet remains fixed ($TP = 1$).
- **Cover Task (Jiggle Detection)**: To ensure attention without explicitly informing participants of the patterns, they perform a "jiggle detection" task.
    - **Targets**: Approximately 10% of stimuli will "jiggle" (shake left and right).
    - **Response**: Participants must press the "1" key as quickly as possible upon detecting a jiggle.
    - **Feedback**: The fixation dot changes color based on performance: Green for success, and Red for missed targets or incorrect presses.

### Experimental Design
The fMRI session consists of 10 runs:
1. **Pre-exposure Run**: Establishes a baseline representation of individual shapes.
2. **8 Exposure Runs**: The primary learning phase where triplets are presented repeatedly.
3. **Post-exposure Run**: Measures representational changes after learning.
*We later uses a "Slow" event-related design for the pre- and post-exposure runs (Stimulus: 3s, ISI: 9s) to better estimate hemodynamic responses.*

## Procedure & Execution Guide
0. Prepare a Python environment with all necessary packages installed (you may create it using `mamba env create -f environment.yml`)
1. **Practice Phase** (Laptop A)
Before entering the scanner, participants complete a practice session to familiarize themselves with the jiggle detection task using a separate set of stimuli.
    1. Open terminal, activate the environment (e.g., `conda activate py3.9`), navigate to the directory where the script is located, and enter `ipython`.
    2. Execute `run VSL_prac.py`, and then enter the 3-digit Subject ID when prompted.
3. **Formal fMRI Task** (Laptop B)
After the initial 20-minute anatomical scan, proceed with the functional runs.
    1. Open terminal, activate the environment, navigate to the directory where the script is located, and enter `ipython`.
    2. Execute `run VSL_exp_run_slow.py <Subject_ID> <Run_Number>`.
    *Note: Allow the participant to rest between runs. They will verbally confirm when they are ready to proceed via the intercom.*
4. **Behavioral Post-test** (Laptop A)
Once the MRI session is complete, transfer the log files (the xxx_triplets.xlsx file) from Laptop B's log folder to Laptop A's log folder.
    1. Open terminal, activate the environment, navigate to the directory where the script is located, and enter `ipython`.
    2. Execute `run VSL_test.py`, and then enter the 3-digit Subject ID and folder prefix (`PW` or `Slow`) when prompted.
5. Post-Experiment Interview
Conduct a brief interview regarding the participant's awareness of the triplets and their strategies. 

### Directory structure
```
behavior/
├── VSL_exp_run.py            # Main rapid event-related experiment (one run per call)
├── VSL_exp_run_slow.py       # Slow event-related variant (fixed 9 s ISI for scan runs)
├── VSL_exp_constants.py      # Timings, colors, display sizes, instructions (used by both)
├── VSL_exp_functions.py      # Helpers: triplet assignment, stream generation, jitter, feedback, ISI calc
├── VSL_prac.py               # Short practice run (no fMRI trigger)
├── VSL_test.py               # Post-experiment familiarity test (AFC + fill-in-the-blank)
├── VSL_test_constants.py     # Layout / instructions for the familiarity test
├── VSL_test_functions.py     # Helpers for the familiarity test (choices, scoring)
├── Trigger.py                # Simulates the fMRI trigger (sends '5' every 2 s)
├── Generate_ISIs.py          # Rebuilds sc_ISI_unshuffled.csv / exp_ISI_unshuffled.csv
├── sc_ISI_unshuffled.csv     # 35 ISIs (1/3/5 s) for pre/post-exposure scan runs
├── exp_ISI_unshuffled.csv    # 71 ISIs (1/3/5 s) for exposure runs
├── Reconstruct_results.py    # Aggregates per-subject jigg-task + familiarity-test results
├── Report_jiggle_Hit.py      # Collects hit-rate summary across subjects
├── Tpl_sort_scores.py        # Per-subject triplet-level familiarity scores
├── copy_files.sh             # Copies experiment + logs between archive paths
├── stimuli/
|   ├── arrow.png             # Arrow used in the familiarity test
|   ├── qm.png                # Question mark used in the familiarity test
|   └── png/1.png … 12.png    # The 12 abstract shape stimuli
├── log/                      # Log files created at runtime
|   ├── practice/
|   |   └── <SID>_prac.txt
|   └── PW<SID>/ 
|       ├── <SID>_jigg_task.xlsx
|       ├── <SID>_logs.txt
|       ├── <SID>_sc_stream.csv
|       ├── <SID>_triplets.xlsx
|       └── <SID>_task-vsl_run-<RUN>_events.tsv
└── familarity_test           # Behavioral Post-test outputs
    └── <SID>_test_result.xlsx
```
