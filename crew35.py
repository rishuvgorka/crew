import csv
import math
import copy
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import matplotlib.pyplot as plt
import time
import sys
import time
import matplotlib
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import datetime
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import argparse

#startTime = time.time()

# --------------------------------------------- PARSE Command Line Input -----------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("inputFileLocation", type=str, help="Provide the location of the input file."
)

args = parser.parse_args()
inputFileLocation = args.inputFileLocation

#Crew Control Jurisdiction
csv_file = "jurisdiction.csv"
# Reading back the lists from the CSV file
with open(csv_file, mode='r') as file:
    reader = csv.reader(file)
    retrieved_lists = [row for row in reader]

# Extracting the lists
cc1 = [str(line) for line in retrieved_lists[0]]
cc2 = [str(line) for line in retrieved_lists[1]]
# Crew Controls

crewControl = [str(line) for line in retrieved_lists[2]]

# Reading parameters


csv_file = "InputParameters.csv"#Provided by users

# Dictionary to store type-value pairs
data = {}

# Reading the CSV file
with open(csv_file, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Storing each type and its value in a dictionary
        key = row['Type']
        value = row['Values']
        data[key] = int(value)

# Assign values to variables dynamically
for key, value in data.items():
    globals()[key] = value


#Crew Control Jurisdiction
#cc1 = ['MKPR','MKPR UP', 'MKPR DN','SAKP','DDSC','DDSC DN','DDSC SDG', 'PVGW','PBGW','PBGW UP','PBGW DN','PVGW UP','PVGW DN','MKPD', 'MKPD ', 'SAKP 3RD']
#cc2 = ['SVVR','SVVR DN ','MUPR','MUPR DN','MUPR 4TH','MUPR 3RD SDG','KKDA DN', 'KKDA UP','IPE','IPE 3RD','VND','MVPO','MVPO DN','NZM','NIZM', 'KKDA', 'MUPR DN SDG']
# Crew Controls

#crewControl = ['KKDA', 'PVGW']

class Services:
    def __init__(self, attrs):
        """object denotinig the a trip from one station to other station"""
        self.servNum = attrs[0] # we give this number; 0 to 927
        self.trainNum = int(attrs[1]) # 701 to 736
        self.startStn = attrs[2]
        self.startTime = hhmm2mins(attrs[3]) # from hh:mm to min
        self.endStn = attrs[4]
        self.endTime = hhmm2mins(attrs[5]) # # from hh:mm to min
        self.dir = attrs[6] # up or down (up means towards MKPR)
        self.servDur = int(attrs[7]) # minutes
        self.stepbackTrainNum = attrs[9]
        self.servAdded = False # not added YET into any duty
        self.breakDur = 0 # in int minutes
        self.tripDur = 0 # in int minutes

def min2hhmm(mins):
    """ changes the time from minutes to hh:mm
        gives hh:mm string and takes integer minutes 0 to 1440"""
    if True:
        h = mins//60
        mins = mins - (h*60)
        if len(str(h)) == 1: h = "0" + str(h)
        if len(str(mins)) == 1: mins = "0" + str(mins)
        return str(h) + ":" + str(mins)

def hhmm2mins(hhmm):
    """ changes the time from hh:mm to minutes
        take hh:mm string and gives integers minutes 0 to 1440"""
    if True:
        hrs = hhmm[:2]
        min = hhmm[-2:]
        mins = int(hrs)*60 + int(min)
        return mins
    
def fetchData(data = inputFileLocation):
    """take the file generated from pre-processing as input and read the data 
       and store it as a object for further processing"""
    servicesLst = []
    tempService = []
    with open(data, "r") as output:
        reader = csv.reader(output)
        for i,row in enumerate(reader):
           if i == 0: continue # ignore header
           tempService.append(row)
        # # 4th and 6th (starting from 1st) need to go from hh:mm to mins
        for i in range(0, len(tempService)):
            temp = (Services(tempService[i])) # create Service object with Service number and a list of its attributes
            toAppendTF = temp.trainNum in range(701,710) # for debugging..
            #toAppendTF = True # comment this for selective appending (for debugging, etc..)
            if toAppendTF: servicesLst.append(temp) # a list of all Services
    return servicesLst


def canAppend2(lst, service2, services):
    """this function checks whether a service can be append in the current duty
       or not and it also checks that the constraints should be followed"""
    startEndStnTF = lst[-1].endStn == service2.startStn # checks duty end station and serv start station
    startEndTimeTF = 0 <= (service2.startTime - lst[-1].endTime) <= 15
    startEndStnTFafterBreak = lst[-1].endStn[:4] == service2.startStn[:4] #chechks only station, without cosidering direction
    startEndTimeWithin = short_break <= (service2.startTime - lst[-1].endTime) <= 120
    #startEndStnTFafterBreak = newDuty.dutyEndStn[:4] == service.startStn[:4] #chechks only station, without cosidering direction
    if lst[-1].stepbackTrainNum == "No StepBack":
        startEndRakeTF = int(lst[-1].trainNum) == int(service2.trainNum) # checks if same rake or not
    else: 
        startEndRakeTF = int(lst[-1].stepbackTrainNum) == int(service2.trainNum)
    
    contTimeDur = 0
    timeDur = 0
    if startEndRakeTF:
        if startEndStnTF and startEndTimeTF:
            timeDur = service2.endTime - lst[0].startTime  #Duty HRS
            trainNum = service2.trainNum
            for service in reversed(lst):
                if service.stepbackTrainNum == "No StepBack":
                    if service.trainNum == trainNum:
                        trainNum = service.trainNum
                        contTimeDur = service2.endTime - service.startTime
                elif int(service.stepbackTrainNum) == trainNum:
                    trainNum = service.trainNum
                    contTimeDur = service2.endTime - service.startTime
                else:  
                    break
                # for service in lst:
                #     if (service.trainNum == service2.trainNum):

                #         contTimeDur = service2.endTime - service.startTime
                #         break
            if contTimeDur <= Continuous_Driving_time and timeDur <= Duty_hours:
                return True
            else: return False
        else: return False

    elif startEndTimeWithin and lst[-1].endStn[:4] in crewControl:
        if startEndStnTFafterBreak:
            timeDur = service2.endTime - lst[0].startTime
            if timeDur <= Duty_hours:
                return True
            else: return False
        else: return False

    else: return False


def allotService(services, start , result):
    """this function take the list of services and input and start making all the
       possible combinations of duties, after a duty set is made it will only print that
       duty which follows all the constraints"""
    #output = []
    total = 0
 
    if start == len(services):
        if result:
            if (result[0].startStn in cc1 and result[-1].endStn in cc1) or (result[0].startStn in cc2 and result[-1].endStn in cc2):
            # output.append(result)
                BreakDur = []
                tripsDur = []
                breakInSameJur,morningDriveDur,firstBreak = False,False,False
                for i in range(len(result)-1):
                    if (result[i+1].startTime - result[i].endTime) >=short_break:
                        tripsDur.append(result[i].endTime - result[0].startTime-sum(tripsDur) - sum(BreakDur))
                        BreakDur.append(result[i+1].startTime - result[i].endTime)
                        if not firstBreak:
                            firstBreak = True
                            if result[0].startStn not in crewControl:
                                if (result[i].endTime - result[0].startTime) >= 90:
                                    morningDriveDur = True
                            else:
                                morningDriveDur = True
                        if ((result[0].startStn in cc1 and result[i].endStn in cc1) or (result[0].startStn in cc2 and result[i].endStn in cc2)) and not breakInSameJur:
                            breakInSameJur = True
                tripsDur.append(result[-1].endTime - result[0].startTime - sum(BreakDur) - sum(tripsDur))
                durMore,breakStsfy = False,False
                for i in range(len(tripsDur)-1):
                    if durMore and breakStsfy:
                        durMore,breakStsfy = False,False
                    if tripsDur[i] >= 120 and not durMore and not breakStsfy:
                        durMore = True
                        if BreakDur[i] >=long_break:
                             breakStsfy = True
                longBreak = False
                totalBreakDur = long_break <= sum(BreakDur) <= 120
                for brake in BreakDur:
                    if brake >= long_break:
                        longBreak = True
                if 1410 <= result[-1].endTime:
                    dutyDurTF = (result[-1].endTime - result[0].startTime) <= 405
                elif result[0].startTime <= 360:   
                    dutyDurTF = (result[-1].endTime - result[0].startTime) <= 405 
                else:
                    dutyDurTF = (result[-1].endTime - result[0].startTime) <= Duty_hours
                #dutyDurTF = result[-1].endTime - result[0].startTime
                # if dutyDur <= 150:
                #     longBreak = True #If duty hours les than 2 1/2 hrs, no requirement of break
                #if (dutyDur <= 120 or (120 < dutyDur <= 300 and totalBreakDur >= 35) or (dutyDur >= 300 and totalBreakDur >= 50)) and totalBreakDur <= 60:
                if breakInSameJur and morningDriveDur and dutyDurTF and (result[-1].endTime - result[0].startTime - sum(BreakDur)) <= Driving_duration and longBreak and totalBreakDur and not(durMore^breakStsfy):
                    #output.append(result[::])
                    for i in result:
                        #trip=i[-1].endTime - i[0].startTime
                        #for service in i:
                        if i == result[-1]:
                           print(i.servNum)
                        else:
                           print(i.servNum, end= ",")
                    return 
                    #print()
                return 
            return 
        return 

    #services.sort(key=lambda serv: serv.startTime)
    if not result:
        result.append(services[start])
        #print(services[start])
        allotService(services,start+1,result)
        result.pop()
    
    else:
        if canAppend2(result, services[start], services):
            result.append(services[start])
            allotService(services,start+1,result)
            result.pop()

    allotService(services,start+1,result)

    return


servicesLstOrig = fetchData()
servicesLstOrig.sort(key=lambda serv: serv.startTime) 
result = []
total_combinations = allotService(servicesLstOrig, 0, result)
#print("Total combinations:", total_combinations)
