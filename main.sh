#!/bin/bas

START_TIME=$SECONDS

# Check if an input argument is provided
if [ -z "$1" ]; then
    echo "Error: No input file's location provided."
    exit 1
fi
startingTime=$(date '+%d-%m-%Y_%H%M')

#new directory every time the script is run, can be identified with date and time
mkdir "output_$startingTime"
mkdir "output_$startingTime/inFiles"
mkdir "output_$startingTime/mainLoop"
mkdir "output_$startingTime/svvrLoop"
mkdir "output_$startingTime/mainLoop/tmFiles"
mkdir "output_$startingTime/svvrLoop/tmFiles"
mkdir "output_$startingTime/finaloutput"

source venv/bin/activate

#pre-procesing
python3 42trains_initialpreprocessing.py "$1" output_$startingTime/inFiles/
python3 stepback_preprocess.py output_$startingTime/inFiles/

# first generate all duties
python3 crew35.py output_$startingTime/inFiles/mainLoop.csv > output_$startingTime/mainLoop/tmFiles/setOfDuties.csv

wc -l output_$startingTime/mainLoop/tmFiles/setOfDuties.csv
echo "(above number of) duties generated: big superset"

# Generating model
python3 MathematicalModel.py output_$startingTime/inFiles/mainLoop.csv output_$startingTime/mainLoop/tmFiles/
echo "mathematical model is executed successfully and model is solved."
echo "i.e. NL file (output_$startingTime/tmFiles/Model1.nl) (integer/linear programming input file) generated."
echo "solution of solver is stored in solution.csv (output_$startingTime/tmFiles/solution.csv)"


echo "now using solver's output to get roster and tripchart files"
python3 solToRoster.py output_$startingTime/inFiles/ output_$startingTime/mainLoop/tmFiles/ output_$startingTime/finaloutput/
echo "bash scipt executed successfully for main Loop."

python3 svvrCrew.py output_$startingTime/inFiles/svvrLoop.csv > output_$startingTime/svvrLoop/tmFiles/setOfDuties.csv

python3 MathematicalModel.py output_$startingTime/inFiles/svvrLoop.csv output_$startingTime/svvrLoop/tmFiles/

python3 svvrRoster.py output_$startingTime/inFiles/ output_$startingTime/svvrLoop/tmFiles/ output_$startingTime/finaloutput/

echo "bash script executed succesfully for SVVR loop."

ELAPSED_TIME=$(($SECONDS - $START_TIME))
echo "Time taken for the whole process: $ELAPSED_TIME seconds"
deactivate
