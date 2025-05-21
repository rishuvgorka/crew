#import plotly.express as px
#import plotly.graph_objects as go
#import matplotlib.pyplot as plt
import pyomo.environ as pyo
from pyomo.core import ConcreteModel
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition
import math
from datetime import timedelta
import csv
import pandas as pd
import random
#import highspy
import argparse
import sys
# --------------------------------------------- PARSE Command Line Input -----------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("inputFileLocation", type=str, help="Provide the location of the input file."
)
parser.add_argument("tempLocation",type=str, help="Provide the location to store the temporary files")
args = parser.parse_args()
inputFileLocation = args.inputFileLocation
tempLocation = args.tempLocation

df = pd.read_csv(inputFileLocation)

services = [df.iloc[i,0] for i in range(len(df)) ]

#dutiesDF = pd.read_csv("/home/22m1513/fileforModel.csv")

service_assignments = {}




# Create an empty dictionary with keys and empty lists
servicesInPath = {key: [] for key in services}

# Open the CSV file in binary mode
with open(f"{tempLocation}setOfDuties.csv", 'rb') as file:
    # Read the file content as bytes
    file_content = file.read()
    
    # Replace null bytes with an empty string
    file_content = file_content.replace(b'\x00', b'')
    
    # Convert the modified content back to a string
    file_content = file_content.decode('utf-8')
    
    # Use StringIO to create a file-like object for csv.reader
    from io import StringIO
    file_like_object = StringIO(file_content)
    
    # Create a CSV reader
    reader = csv.reader(file_like_object)
    
    # Iterate over each row and filter out NULL values
    for index, row in enumerate(reader):
        # Filter out NULL values (assuming NULL is represented as the string 'NULL')
        filtered_row = [int(value) for value in row if value != 'NULL' and value != '']
        #filtered_row = [int(value) if value != '' else None for value in row if value != 'NULL']


        
        # if 3 <= len(filtered_row) <= 6:
        #     prob = random.random() < 0.1
        # else: prob = True
        # #Store the filtered row in the dictionary if it's not empty
        # if filtered_row and prob:
        if filtered_row:
            for ii in filtered_row:

                servicesInPath[ii].append(index)
                
            # if len(filtered_row) > 1:
                service_assignments[index] = filtered_row

x = len(service_assignments)
"""
for i in services:
    # randomServicesAssignments[x] = [i] 
    service_assignments[x] = [i]
    servicesInPath[i].append(x)
    x += 1
"""
num_services = len(services)
num_drivers = len(service_assignments)
print(num_drivers)
#service_assignments - key:duty_number, value:set of service numbers in this duty
for xyz in range(1):
    servicesInDuties = []
    for index,services1 in service_assignments.items():
        for service in services1:
            if service not in servicesInDuties:
                servicesInDuties.append(service)
        if len(servicesInDuties) == num_services: 
            break
    if num_services != len(servicesInDuties):
        print(f"Total No. of services are not appended in iteration, total number of services:{num_services},number of services appended:{len(servicesInDuties)}")
        servicesInDuties.sort()
        print(servicesInDuties)
        continue

    madhavModel = ConcreteModel()
    madhavModel.fPath = pyo.Var([path for path in service_assignments.keys()], domain=pyo.Binary) #Reals, bounds=(0,1))
    madhavModel.fServ = pyo.Var([ser for ser in services], domain=pyo.Reals, bounds=(0,1))

    def objectiveRule(model):
        minimumPath = sum(model.fPath[path] for path in service_assignments.keys())
        return minimumPath 

    madhavModel.OBJ = pyo.Objective(rule=objectiveRule, sense=pyo.minimize)
    madhavModel.ConsList = pyo.ConstraintList()
    for ser in services:
        madhavModel.ConsList.add(madhavModel.fServ[ser] == 1)

# for edge in services:
#       pathIdsContainingServ = []
#       for path in service_assignments.keys():
#         for ee in service_assignments[path]:
#           if ee==edge:
#             pathIdsContainingServ.append(path)
#             print(path)
#       madhavModel.ConsList.add(sum(madhavModel.fPath[pathId] for pathId in pathIdsContainingServ) == madhavModel.fServ[edge])

    for edgeService,edgepaths in servicesInPath.items():
        madhavModel.ConsList.add(sum(madhavModel.fPath[pathId] for pathId in edgepaths) ==  madhavModel.fServ[edgeService])
    madhavModel.write(f"{tempLocation}Model.nl", format = 'nl')

    print("Solving Model")
    # opt=SolverFactory("gurobi_direct")
    # result=opt.solve(madhavModel)
    optSolver = SolverFactory('mbnb', executable="mbnb")
    #optSolver.options['--time_limit'] = 15000
    optSolver.options['--branch_dir'] = 1
    optSolver.options['--brancher'] = 'maxvio'
    optSolver.options['--set_lp_method'] = 0
    optSolver.options['--sppheur'] = 1
    optSolver.options['--log_level'] = 3
    optSolver.options['--obj_gap_percent'] = 5
    result = optSolver.solve(madhavModel, tee=True)

    print('Solver status:', result.solver.status)
    print('Solver termination condition:',result.solver.termination_condition)


    if result.solver.termination_condition != "infeasible":
    #     pass
        varVal = []
        totalDuties = 0
        with open(f"{tempLocation}solution.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for variable in madhavModel.fPath:
                #print(str(variable),madhavModel.fPath[variable].value)
                if abs(madhavModel.fPath[variable].value-1) <= 1e-6:
                    writer.writerow(service_assignments[int(variable)])
                    #print(madhavModel.fPath[variable],'=', service_assignments[int(variable)-1])
                    totalDuties += 1
    #     #     #print(madhavModel.fPath[variable],'=',int(madhavModel.fPath[variable].value))
        print("Total Duties: ",totalDuties)

    else:
        print("Infeasible solution found in iteration:")
