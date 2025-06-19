# Crew Scheduling Automation for DMRC

This repository contains a system to automate the generation of crew duty rosters for train operations for Line 7 (Pink Line) of Delhi Metro Rail Corporation. It uses mathematical modeling, preprocessing of operational data, and optimization algorithms to significantly reduce the time and effort required in manual crew scheduling.

## 📌 Project Overview

The goal is to allocate train services to crew members while satisfying several operational constraints such as:
- Jurisdiction restrictions
- Step-back train logic
- Sign-on/off times and crew change rules
- Duty hour limitations
- Service continuity and rake handling

The system is built in modular Python scripts that handle different aspects of crew scheduling — from preprocessing raw data to generating optimal duty charts using mathematical programming.

---

## 📁 Folder Structure

crew/
├── crew35.py # Alternate version of crew generation logic
├── svvrCrew.py # Core crew scheduling logic with plotting support
├── svvrRoster.py # Generates final rosters for crew
├── stepback_preprocess.py # Merges services based on step-back logic
├── solToRoster.py # Converts optimization solution to readable duty roster
├── MathematicalModel.py # Pyomo-based optimization model to minimize crew count
├── 42trains_initialpreprocessing.py # Preprocessing timetable Excel to CSV
├── main.sh # Execution script (shell)
├── LICENSE

---

## 🧮 Dependencies

Install the following dependencies before running:

```bash
pip install pandas numpy matplotlib plotly seaborn pyomo

You also need a solver supported by Pyomo like:
MIP (e.g., mbnb)

🚀 How to Run
Each script has command-line arguments for flexible execution. Here's the general flow:

1. Preprocessing
 - python 42trains_initialpreprocessing.py <input_excel> <output_folder>
 - python stepback_preprocess.py <output_folder>
2. Generate Duties
 - python svvrCrew.py <preprocessed_file>
3. Optimize Duty Allocation
 - python MathematicalModel.py <input_file> <temp_folder>
4. Generate Final Roster
 - python solToRoster.py <input_file> <temp_folder> <output_folder>

You may also use the main.sh shell script to run the full pipeline.

📊 Features
Automatic merging of compatible services (step-back and non-step-back)

Constraints-based duty generation

Uses optimization to minimize crew

Generates exportable CSV rosters and trip chart.

📃 License
This project is licensed under the terms of the LICENSE file.

✍️ Author
Rishuv Gorka
IIT Bombay | Crew Scheduling Automation | Delhi Metro Optimization

