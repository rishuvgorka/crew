# Crew Scheduling Automation for DMRC

This repository contains a system to automate the generation of crew duty rosters for train operations for Line 7 (Pink Line) of Delhi Metro Rail Corporation. It uses mathematical modeling, preprocessing of operational data, and optimization algorithms to significantly reduce the time and effort required in manual crew scheduling.

## 📌 Project Overview
This system automates the complex process of crew scheduling for railway operations by:
- Processing timetable data into service segments
- Generating valid duty combinations that comply with operational rules
- Optimizing crew assignments using mathematical programming
- Producing comprehensive rosters and trip charts

While satisfying several operational constraints such as:
- Jurisdiction restrictions
- Step-back train logic
- Sign-on/off times and crew change rules
- Duty hour limitations
- Service continuity and rake handling

The system is built in modular Python scripts that handle different aspects of crew scheduling — from preprocessing raw data to generating optimal duty charts using mathematical programming.



## 📁 Folder Structure
```text
crew/
├── main.sh                     # Master script
├── 42trains_initialpreprocessing.py  # Timetable processor
├── stepback_preprocess.py      # Step-back service handler
├── crew35.py                   # Main loop generator
├── svvrCrew.py                 # SVVR loop generator
├── MathematicalModel.py        # Optimizer
├── solToRoster.py              # Main output generator
├── svvrRoster.py               # SVVR output generator
├── jurisdiction.csv            # Control boundaries
├── InputParameters.csv         # Operational parameters
└── README.md                   # This file

```

## 🧮 Dependencies

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `plotly`
- `pyomo`

Install the above dependencies before running:

```bash
pip install pandas numpy matplotlib plotly seaborn pyomo
```
You also need a solver supported by Pyomo like:
MIP (e.g., mbnb)

## 🚀 How to Run
Each script has command-line arguments for flexible execution. Here's the general flow:

1. Preprocessing
```bash
 - python 42trains_initialpreprocessing.py <input_excel> <output_folder>
 - python stepback_preprocess.py <output_folder>
```
2. Generate Duties
```bash
 - python svvrCrew.py <preprocessed_file>
```
3. Optimize Duty Allocation
```bash
 - python MathematicalModel.py <input_file> <temp_folder>
```
4. Generate Final Roster
```bash
 - python solToRoster.py <input_file> <temp_folder> <output_folder>
```

You may also use the main.sh shell script to run the full pipeline.
```bash
bash main.sh <input_excel>
```
If you wanna push the task in the background then use:
```bash
nohup bash main.sh <input_excel> >log.txt 2>&1 &
```
Here `log.txt` stores the log or the output printed in the terminal of the above command.

## System Architecture
```mermaid
graph TD
    A[Input Timetable] --> B[42trains_initialpreprocessing.py]
    B --> C[InitialServices.csv]
    C --> D[stepback_preprocess.py]
    D --> E[Main Loop/SVVR Loop CSVs]
    E --> F[crew35.py/svvrCrew.py]
    F --> G[Set of Duties]
    G --> H[MathematicalModel.py]
    H --> I[Optimized Solution]
    I --> J[solToRoster.py/svvrRoster.py]
    J --> K[Final Outputs]
```

## 📊 Features
Automatic merging of compatible services (step-back and non-step-back)

Constraints-based duty generation

Uses optimization to minimize crew

Generates exportable CSV rosters and trip chart.

## 📃 License
This project is licensed under the terms of the LICENSE file.

## ✍️ Author
Rishuv Gorka
IIT Bombay | Crew Scheduling Automation | Delhi Metro Optimization

