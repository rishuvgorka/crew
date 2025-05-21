import pandas as pd
import csv
import sys

import argparse

# --------------------------------------------- PARSE Command Line Input -----------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("inputFileLocation", type=str, help="Provide the location of the input file."
)
parser.add_argument("tempLocation",type=str, help="Provide the location to store the temporary files")
parser.add_argument("outputLocation",type=str, help="Provide the location to store the final output files")
args = parser.parse_args()
inputFileLocation = args.inputFileLocation
tempLocation = args.tempLocation
outputLocation = args.outputLocation

ijk=0
tookServices = []
dutiesDict = {}

with open(f"{tempLocation}solution.csv", 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        dutiesDict[ijk] = [int(value) for value in row]
        tookServices += [int(value) for value in row]
        ijk += 1

print(len(tookServices), ijk)

df = pd.read_csv(f"{inputFileLocation}mainLoop.csv")#input services
df1 = pd.read_csv(f"{inputFileLocation}InitialServices.csv")
servicesAll = [df.iloc[i,0] for i in range(len(df)) ]



"""
for service in servicesAll:
    if service not in tookServices:
        dutiesDict[ijk] = [service]
        ijk += 1
"""
print(ijk,"yoyooy")

def hhmm2mins(hhmm):
    if True:
        hrs = hhmm[:2]
        min = hhmm[-2:]
        mins = int(hrs)*60 + int(min)
        return mins
    
def min2hhmm(mins):
    """ gives hh:mm string and takes integer minutes 0 to 1440"""
    if True:
        h = mins//60
        mins = mins - (h*60)
        if len(str(h)) == 1: h = "0" + str(h)
        if len(str(mins)) == 1: mins = "0" + str(mins)
        return str(h) + ":" + str(mins)
    
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

svvrRake = [int(num) for num in retrieved_lists[3]]

def printRoster(dutiesDict, outputFile):
    # global verbose, worstDT
    sameCC = 0
    KKDA_no, PBGW_no, dist = 201,501,1
    
    with open(outputFile, mode='w', newline='') as file:
        writer = csv.writer(file)
        #header = [f"{ordinal(i)} Service" for i in range(1, 20 + 1)]
        #writer.writerow(["Duty No", "Sign On Time", "Sign On Loc", "Sign Off Loc", "Sign Off Time", "Driving Hrs", "Duty Hrs"] + header)
        writer.writerow(["Duty No", "Sign On Time", "Sign On Loc", "Sign Off Loc", "Sign Off Time", "Driving Hrs", "Duty Hrs", "Same Jurisdiction","Rake Num", "Start Stn", "Start Time", "End Stn", "End Time","Service Duration", "Break","StepBack Rake"])


        for index, servSet in dutiesDict.items():
                #print(servSet.breaksTaken,servSet.breaksRemaining,index)
                servSet1 = []
                for ax in servSet:
                    for ss in range(len(df)):
                        if ax == df.iloc[ss,0]:
                            servSet1.append([df.iloc[ss,1],df.iloc[ss,2],df.iloc[ss,3],df.iloc[ss,4],df.iloc[ss,5],df.iloc[ss,6],df.iloc[ss,7],df.iloc[ss,9]])
                

                # dutyDur = min2hhmm(hhmm2mins(servSet1[-1][4]) - hhmm2mins(servSet1[0][2]) + 25)
                # drivingTimes.append(servSet.totalDriveDur)
                # dutyHrs.append(servSet.dutyHrs)
                dutyNo = 0
                if (servSet1[0][1] in cc1 and servSet1[-1][3] in cc1):
                    dutyNo = PBGW_no
                    PBGW_no += 1
                elif (servSet1[0][1] in cc2 and servSet1[-1][3] in cc2):
                    dutyNo = KKDA_no
                    KKDA_no += 1
                else:
                    dutyNo = dist
                    dist += 1
                if servSet1[0][1] in crewControl:
                    signOnTime = min2hhmm(hhmm2mins(servSet1[0][2]) - 15)
                else:
                    signOnTime = min2hhmm(hhmm2mins(servSet1[0][2]) - 25)
                # signOnDur = servSet.signOn()[1]
                signOnLoc = servSet1[0][1]
                if servSet1[-1][3] in crewControl:
                    signOffTime = min2hhmm(hhmm2mins(servSet1[-1][4]) + 10)
                else:
                    signOffTime = min2hhmm(hhmm2mins(servSet1[-1][4]) + 20)
                
                dutyDur = min2hhmm(hhmm2mins(signOffTime) - hhmm2mins(signOnTime))
                driveDur = hhmm2mins(servSet1[-1][4])-hhmm2mins(servSet1[0][2])
                signOffLoc = servSet1[-1][3]
                if (servSet1[0][1] in cc1 and servSet1[-1][3] in cc1) or (servSet1[0][1] in cc2 and servSet1[-1][3] in cc2):
                    sameJuris = "Yes"
                    sameCC += 1
                else: sameJuris = "No"

                breaks = []

# Iterate over the sublists
                for i in range(len(servSet1) - 1):  # Iterate until the second to last sublist
                    diff = hhmm2mins(servSet1[i + 1][2]) - hhmm2mins(servSet1[i][4])  # Calculate the difference
                    breaks.append(diff)
                    if diff>=30:
                        driveDur -= diff
                driveDur = min2hhmm(driveDur)
# Rishuv
                First_Serv = True
                brake = 0
                for service in servSet1:
                    if brake == len(servSet1) - 1:
                        new_header = [service[0] , service[1] ,service[2] ,service[3], service[4] , service[6] , 0, service[7]]
                    else:
                        new_header = [service[0] , service[1] ,service[2] ,service[3], service[4] , service[6] , breaks[brake], service[7]]
                        brake += 1
                    if First_Serv:
                        writer.writerow([dutyNo, signOnTime,signOnLoc, signOffLoc, signOffTime, driveDur, dutyDur, sameJuris] + new_header)    
                        First_Serv = False
                    else:
                        #writer.writerow([dutyNo, signOnTime,signOnLoc, signOffLoc, signOffTime, driveDur, dutyDur, sameJuris] + new_header)
                        writer.writerow([dutyNo, "","", "", "", "", "",""] + new_header)    
                writer.writerow(["","" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"" ,"",""])
    print("same Juris % = ", sameCC/len(dutiesDict))

def ordinal(number): # useful for printing tripChart 
    if 10 <= number % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')
    return str(number) + suffix

def customSort(sheet):
    apex1,apex2 = 0,0
    
    # Find the first non-empty string
    while apex1 < len(sheet) and sheet[apex1][27] == " ":
        apex1 += 1
    while apex2 < len(sheet) and sheet[apex2][4] == " ":
        apex2 += 1
    sheet[:apex1] = sorted(sheet[:apex1], key=lambda x: (x[23],x[8]))
    j = 0

    while(j<=apex1):
        if sheet[apex1][23] == " ":
            sheet.insert(j,sheet[apex1])
            j += 1
            apex1 += 1
            sheet.pop(apex1)
        elif sheet[j][23] == " ":
            if sheet[apex1][8] == " ":
                sheet.insert(j,sheet[apex1])
                j += 1
                apex1 += 1
                sheet.pop(apex1)
            elif sheet[j][8] > sheet[apex1][8]:
                sheet.insert(j,sheet[apex1])
                j += 1
                apex1 += 1
                sheet.pop(apex1)
            else:
                j += 1
        elif sheet[j][23]>sheet[apex1][23]:
            sheet.insert(j,sheet[apex1])
            j += 1
            apex1 += 1
            sheet.pop(apex1)
        else:
            j += 1

    i = 0
    while(i<=apex2):
        if sheet[apex2][23] == " ":
            if sheet[i][23]>sheet[apex2+1][23]:
                sheet.insert(i,sheet[apex2])
                i += 1
                apex2 += 1
                sheet.pop(apex2)
            else:
                i += 1
        elif sheet[i][23] == " ":
            if sheet[i][23] > sheet[apex2][23]:
                sheet.insert(i,sheet[apex2])
                i += 1
                apex2 += 1
                sheet.pop(apex2)
            else:
                i += 1
        elif sheet[i][23]>sheet[apex2][23]:
            sheet.insert(i,sheet[apex2])
            i += 1
            apex2 += 1
            sheet.pop(apex2)
        else:
            i += 1
    
def svvrChart(dutiesDict, op):
    trainDuty = {}
    KKDA_no, PBGW_no, dist = 201,501,1
    dutyNo = 0

    for dutyNum, servSet in dutiesDict.items():
        servSet1 = []
        for ax in servSet:
            for ss in range(len(df)):
                if ax == df.iloc[ss,0]:
                    for serv in range(len(df1)):
                        if float(df1.iloc[serv,0]) == df.iloc[ss,12] or df1.iloc[serv,0] == df.iloc[ss,11]:
                            servSet1.append([df1.iloc[serv,1],df1.iloc[serv,2],df1.iloc[serv,3],df1.iloc[serv,4],df1.iloc[serv,5],df1.iloc[serv,6],df1.iloc[serv,7]])

        if (servSet1[0][1] in cc1 and servSet1[-1][3] in cc1):
            dutyNo = PBGW_no
            PBGW_no += 1
        elif (servSet1[0][1] in cc2 and servSet1[-1][3] in cc2):
            dutyNo = KKDA_no
            KKDA_no += 1
        else:
            dutyNo = dist
            dist += 1

        for service in servSet1:
            trainNum = service[0]               
            if trainNum not in trainDuty:
                trainDuty[trainNum] = list()
            trainDuty[trainNum].append([dutyNo] + service[1:])  
    """
    with open(op, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        header = [f"{ordinal(i)} person" for i in range(1, 40 + 1)]
        writer.writerow(['Train No.'] + header)
        # Write data
        for trainNum, dutySet in trainDuty.items():
            dutySet.sort(key=lambda x:x[2])
            writer.writerow([trainNum] + dutySet)

    sys.exit()
    """
    for trainNum, dutySet in trainDuty.items(): 
        dutySet.sort(key=lambda x:x[2])
    
    if True:
        sheet = []
        for trainNum, dutySet in trainDuty.items():
            i,j = 0,len(dutySet)-1
            if trainNum in svvrRake:
                print(trainNum)
                line = []
                line.append(trainNum)
                line.append(dutySet[i][1])
                line.append(dutySet[i][2])
                i += 1

                if dutySet[i][1] == "MKPR":
                    pass
                elif dutySet[i][1] == "PVGW DN":
                    line.append(" ")
                    line.append(" ")
                elif dutySet[i][1] == "KKDA DN":
                    line.append(" ")
                    line.append(" ")
                    line.append(" ")
                    line.append(" ")
                elif dutySet[i][0] == "MUPR":
                    line.append(" ")
                    line.append(" ")
                    line.append(" ")
                    line.append(" ")
                    line.append(" ")
                    line.append(" ")
                else:
                    for k in range(6):
                        line.append(" ")
                    line.append(dutySet[i-1][2])
                    line.append(dutySet[i-1][0])
                while (dutySet[i][1] != "SVVR"):
                    line.append(dutySet[i][2])
                    line.append(dutySet[i][0])
                    i+=1
                line.append(dutySet[i-1][4])
                line.append(dutySet[i-1][3])
                line.append(trainNum)
                line.append(dutySet[i][2])
                line.append(dutySet[i][0])
                line.append(dutySet[i][4])
                i+=1
                for k in range(8):
                    line.append(" ")
                line.append(trainNum)
                sheet.append(line)
                while(dutySet[j][1] != "SVVR"):
                    print(dutySet[j][1])
                    j -= 1
                while(i<j):
                    line=[]
                    line.append(trainNum)
                    for k in range(8):
                        line.append(" ")
                    line.append(dutySet[i][2])
                    line.append(dutySet[i][0])
                    line.append(dutySet[i][4])
                    line.append(dutySet[i][3])
                    line.append(trainNum)
                    i+=1
                    line.append(dutySet[i][2])
                    line.append(dutySet[i][0])
                    line.append(dutySet[i][4])
                    i+=1
                    for k in range(8):
                        line.append(" ")
                    line.append(trainNum)
                    sheet.append(line)
                    
                line =[]
                line.append(trainNum)
                for k in range(8):
                    line.append(" ")
                line.append(dutySet[j-1][2])
                line.append(dutySet[j-1][0])
                line.append(dutySet[j-1][4])
                line.append(dutySet[j-1][3])
                line.append(trainNum)
                while(dutySet[j][1] != dutySet[-1][1]):
                    line.append(dutySet[j][2])
                    line.append(dutySet[j][0])
                    j += 1

                while(len(line)<23):
                    line.append(" ")
                line.append(dutySet[-1][3])
                line.append(dutySet[-1][4])
                line.append(trainNum)
                sheet.append(line)
                continue

    sheet.sort(key= lambda x:x[9])
    with open(op, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        header = ["TRAIN NO." ," ", " ", "MKPR", "DUTY NO.", "PVGW DN", "DUTY NO.", "KKDA DN", "DUTY NO." ,"MUPR","DUTY NO.", "SVVR", "REVERSAL FROM", "TRAIN NO.", "SVVR","DUTY NO.", "MU    PR", "DUTY NO.","KKDA UP","DUTY NO.", "PVGW UP","DUTY NO.","MKPR", " ", " ", "TRAIN NO."]
        writer.writerow(header)
        for row in sheet:
            writer.writerow(row)



def printChart(dutiesDict, op):
    trainDuty = {}
    KKDA_no, PBGW_no, dist = 201,501,1
    dutyNo = 0

    for dutyNum, servSet in dutiesDict.items():
        servSet1 = []
        for ax in servSet:
            for ss in range(len(df)):
                if ax == df.iloc[ss,0]:
                    for serv in range(len(df1)):
                        if float(df1.iloc[serv,0]) == df.iloc[ss,12] or df1.iloc[serv,0] == df.iloc[ss,11]:
                            servSet1.append([df1.iloc[serv,1],df1.iloc[serv,2],df1.iloc[serv,3],df1.iloc[serv,4],df1.iloc[serv,5],df1.iloc[serv,6],df1.iloc[serv,7]])

        if (servSet1[0][1] in cc1 and servSet1[-1][3] in cc1):
            dutyNo = PBGW_no
            PBGW_no += 1
        elif (servSet1[0][1] in cc2 and servSet1[-1][3] in cc2):
            dutyNo = KKDA_no
            KKDA_no += 1
        else:
            dutyNo = dist
            dist += 1

        for service in servSet1:
            trainNum = service[0]               
            if trainNum not in trainDuty:
                trainDuty[trainNum] = list()
            trainDuty[trainNum].append([dutyNo] + service[1:])  
    """
    with open(op, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        header = [f"{ordinal(i)} person" for i in range(1, 40 + 1)]
        writer.writerow(['Train No.'] + header)
        # Write data
        for trainNum, dutySet in trainDuty.items():
            dutySet.sort(key=lambda x:x[2])
            writer.writerow([trainNum] + dutySet)

    sys.exit()
    """
    for trainNum, dutySet in trainDuty.items(): 
        dutySet.sort(key=lambda x:x[2])
    
    if True:
        sheet = []
        for trainNum, dutySet in trainDuty.items():
            print(trainNum) 
            i,j = 0,len(dutySet)-1
            if trainNum in svvrRake:
                #continue
                
                if dutySet[0][5] == "DN":
                    line = []
                    line.append(trainNum)
                    line.append(dutySet[i][1])
                    line.append(dutySet[i][2])
                    line.append(dutySet[i][0])
                    i += 1

                    if dutySet[i-1][3] == "MKPR":
                        while (dutySet[i][3] != "KKDA DN" and dutySet[i][5] =="DN"):
                            line.append(dutySet[i][2])
                            line.append(dutySet[i][0])
                            i+=1
                        line.append(dutySet[i][2])
                        line.append(dutySet[i][0])
                        line.append(dutySet[i][4])
                        line.append("Refer to SVVR TRIPCHART further")
                    elif dutySet[i-1][3] == "PVGW DN":
                        line.append(" ")
                        line.append(dutySet[i-1][0])
                        line.append(dutySet[i][2])
                        line.append(dutySet[i][0])
                        i += 1
                        line.append(dutySet[i][2])
                        line.append(dutySet[i][0])
                        line.append(dutySet[i][4])
                        line.append("Refer to SVVR TRIPCHART further")
                    elif dutySet[i-1][3] == "IPE":
                        line.append(" ")
                        line.append(dutySet[i-1][0])
                        line.append(" ")
                        line.append(dutySet[i-1][0])
                        line.append(dutySet[i][2])
                        line.append(dutySet[i][0])
                        line.append(dutySet[i][4])
                        line.append("Refer to SVVR TRIPCHART further")
                    elif dutySet[i-1][3] == "KKDA DN":
                        line.append(" ")
                        line.append(dutySet[i-1][0])
                        line.append(" ")
                        line.append(dutySet[i-1][0])
                        line.append(" ")
                        line.append(dutySet[i-1][0])
                        line.append(dutySet[i-1][4])
                        line.append("Refer to SVVR TRIPCHART further")
                  
                    line.append(" ")
                    line.append(" ")
                    line.append(" ")
                    line.append(" ")
                    line.append(trainNum)
                    while(len(line)<31):
                        line.append(" ")
                    line.append(trainNum)
                    sheet.append(line)
                    i += 1

                if i == len(dutySet):
                    continue
                line =[]
                while(dutySet[j][1] != "KKDA UP"):
                    #print(dutySet[j][1])
                    j -= 1
                line.append(trainNum)
                for k in range(15):
                    line.append(" ")
                line.append(trainNum)
                for k in range(4):
                    line.append(" ")
                while(dutySet[j][1] != dutySet[-1][1]):
                    if dutySet[j][1] == "MKPR":
                        line.append(dutySet[j][2])
                        j+=1
                        continue
                    line.append(dutySet[j][2])
                    line.append(dutySet[j][0])
                    j += 1
                if dutySet[j][1] == "MKPR":
                    line.append(dutySet[j][2])
                elif dutySet[j][1] =="IPE":
                    line.append(dutySet[j][2])
                    line.append(dutySet[j][0])
                while(len(line)<28):
                    line.append(" ")
                line.append(dutySet[-1][3])
                line.append(dutySet[-1][0])
                line.append(dutySet[-1][4])
                line.append(trainNum)
                sheet.append(line)
                continue
            #for mainloop trains
            while(dutySet[j][1] != "MKPR"):
                j -= 1
            while i < len(dutySet):
                line = []
                if i == 0:
                    if dutySet[i][1] != "MKPR":
                        line.append(trainNum)
                        line.append(dutySet[i][1])
                        line.append(dutySet[i][2])
                        line.append(dutySet[i][0])
                        i += 1
                        if dutySet[i][5] =="DN":
                            if dutySet[i][1] == "MKPR":
                                pass
                            elif dutySet[i][1] == "PVGW DN":
                                line.append(" ")
                                line.append(" ")
                            elif dutySet[i][1] == "IPE":
                                line.append(" ")
                                line.append(" ")
                                line.append(" ")
                                line.append(" ")    
                            elif dutySet[i][1] == "KKDA DN":
                                line.append(" ")
                                line.append(" ")
                                line.append(" ")
                                line.append(" ")
                                line.append(" ")
                                line.append(" ")
                                               
                            while (dutySet[i][1] != "MUPR"):
                                line.append(dutySet[i][2])
                                line.append(dutySet[i][0])
                                i+=1
                    
                            if dutySet[i][3] == "SVVR":
                                line.append(dutySet[i][2])
                                line.append(dutySet[i][0])
                                line.append(dutySet[i][4])
                                line.append(dutySet[i][3])
                                line.append(trainNum)
                                i+=1
                            elif dutySet[i][3] == "KKDA UP":
                                line.append(dutySet[i-1][4])
                                line.append(" ")
                                line.append(" ")
                                line.append(dutySet[i-1][3])
                                line.append(trainNum)
                                line.append(" ")
                                line.append(" ")

                            while(dutySet[i][1] != "MKPR"):
                                line.append(dutySet[i][2])
                                line.append(dutySet[i][0])
                                i += 1
                            if i == len(dutySet)-1:
                                line.append(dutySet[i][2])
                                line.append(dutySet[i][3])
                                line.append(dutySet[i][0])
                                line.append(dutySet[i][4])
                                line.append(trainNum)
                            else:
                                i -= 1
                                line.append(dutySet[i][4])
                                line.append(" ")
                                line.append(" ")
                                line.append(" ")
                                line.append(trainNum)

                        elif dutySet[i][5] == "UP":
                            line.append(" ")
                            line.append(" ")
                            line.append(" ")
                            line.append(" ")
                            line.append(" ")
                            line.append(" ")
                            line.append(" ")
                            line.append(" ")
                            line.append(" ")
                            line.append(" ")
                            line.append(" ")
                            line.append(" ")
                            line.append(trainNum)
                            if dutySet[i][1] == "SVVR":
                                pass
                            elif dutySet[i][1] == "MUPR":
                                line.append(" ")
                                line.append(" ")
                            elif dutySet[i][1] == "KKDA UP":
                                line.append(" ")
                                line.append(" ")
                                if dutySet[i-1][1] == "MUPR":
                                    line.append(dutySet[i-1][2])
                                    line.append(dutySet[i-1][0])
                                else:
                                    line.append(" ")
                                    line.append(" ")
                            elif dutySet[i][1] == "IPE":
                                line.append(" ")
                                line.append(" ")
                                line.append(" ")
                                line.append(" ")
                                line.append(" ")
                                line.append(" ")
                            elif dutySet[i][1] == "PVGW UP":
                                line.append(" ")
                                line.append(" ")
                                line.append(" ")
                                line.append(" ")
                                line.append(" ")
                                line.append(" ")
                                line.append(" ")
                                line.append(" ")
                            else:
                                print("Invalid")
                            while dutySet[i][1] != "MKPR":
                                line.append(dutySet[i][2])
                                line.append(dutySet[i][0])
                                i += 1
                            if i == len(dutySet)-1 and dutySet[i][3] =="MKPD":
                                line.append(dutySet[i][2])
                                line.append(dutySet[i][3])
                                line.append(dutySet[i][0])
                                line.append(dutySet[i][4])
                                line.append(trainNum)
                            else:
                                i -= 1
                                line.append(dutySet[i][4])
                                line.append(" ")
                                line.append(" ")
                                line.append(" ")
                                line.append(trainNum)
                    else:
                        line.append(trainNum)
                        line.append(dutySet[i][1])
                        line.append(" ")
                        line.append(dutySet[i][0])

                if i < j and dutySet[i][1] == "MKPR":
                    if i != 0:
                        line.append(trainNum)
                        line.append(" ")
                        line.append(" ")
                        line.append(" ")
                    while(dutySet[i][1] != "MUPR"):
                        line.append(dutySet[i][2])
                        line.append(dutySet[i][0])
                        i+=1
                    
                    if dutySet[i][3] == "SVVR":
                        line.append(dutySet[i][2])
                        line.append(dutySet[i][0])
                        line.append(dutySet[i][4])
                        line.append(dutySet[i][3])
                        line.append(trainNum)
                        i+=1
                    elif dutySet[i][3] == "KKDA UP":
                        line.append(dutySet[i-1][4])
                        line.append(" ")
                        line.append(" ")
                        line.append(dutySet[i-1][3])
                        line.append(trainNum)
                        line.append(" ")
                        line.append(" ")

                    while(dutySet[i][1] != "MKPR"):
                        line.append(dutySet[i][2])
                        line.append(dutySet[i][0])
                        i += 1
                    if i == len(dutySet)-1 and dutySet[i][3] == "MKPD":
                        line.append(dutySet[i][2])
                        line.append(dutySet[i][3])
                        line.append(dutySet[i][0])
                        line.append(dutySet[i][4])
                        line.append(trainNum)
                    else:
                        i -= 1
                        line.append(dutySet[i][4])
                        line.append(" ")
                        line.append(" ")
                        line.append(" ")
                        line.append(trainNum)    
                elif i == len(dutySet) - 1 and dutySet[i][1] == "MKPR":
                    line.append(trainNum)
                    line.append(" ")
                    line.append(" ")
                    line.append(" ")
                    line.append(dutySet[-1][2])
                    line.append(dutySet[-1][0])
                    for k in range(0,22):
                        line.append(" ")
                    line.append(dutySet[-1][3])
                    line.append(dutySet[-1][0])
                    line.append(dutySet[-1][4])
                    line.append(trainNum) 
                elif i>=j and i<len(dutySet)-1:
                    line.append(trainNum)
                    line.append(" ")
                    line.append(" ")
                    line.append(" ")
                    if dutySet[-2][5] == "UP":
                        while(dutySet[i][1] != "MUPR"):
                            line.append(dutySet[i][2])
                            line.append(dutySet[i][0])
                            i+=1
                    
                        if dutySet[i][3] == "SVVR":
                            line.append(dutySet[i][2])
                            line.append(dutySet[i][0])
                            line.append(dutySet[i][4])
                            line.append(dutySet[i][3])
                            line.append(trainNum)
                            i+=1
                        elif dutySet[i][3] == "KKDA UP":
                            line.append(dutySet[i-1][4])
                            line.append(" ")
                            line.append(" ")
                            line.append(dutySet[i-1][3])
                            line.append(trainNum)
                            line.append(" ")
                            line.append(" ")

                        while(dutySet[i][1] != dutySet[-1][1]):
                            line.append(dutySet[i][2])
                            line.append(dutySet[i][0])
                            i += 1
                        if dutySet[i][1] == "MUPR":
                            line.append(dutySet[i][2])
                            line.append(dutySet[i][0])
                        while(len(line)<28):
                            line.append(" ")
                        line.append(dutySet[-1][3])
                        line.append(dutySet[-1][0])
                        line.append(dutySet[-1][4])
                        line.append(trainNum)
                    elif dutySet[-2][5] == "DN":
                        if dutySet[-2][1] == "MUPR":
                            while(dutySet[i][1] != "MUPR"):
                                line.append(dutySet[i][2])
                                line.append(dutySet[i][0])
                                i+=1
                      
                            if dutySet[i][3] == "SVVR":
                                line.append(dutySet[i][2])
                                line.append(dutySet[i][0])
                                line.append(dutySet[i][4])
                                line.append(dutySet[i][3])
                                line.append(trainNum)
                                i+=1
                                line.append(dutySet[i][2])
                                line.append(dutySet[i][0])
                                while(len(line)<28):
                                    line.append(" ")
                                line.append(dutySet[i][3])
                                line.append(dutySet[i][0])
                                line.append(dutySet[i][4])
                                line.append(trainNum)
                                sheet.append(line)
                                i += 1
                                continue   
                            elif dutySet[i][3] == "KKDA UP":
                                line.append(dutySet[i-1][4])
                                line.append(" ")
                                line.append(" ")
                                line.append(dutySet[i-1][3])
                                line.append(trainNum)
                                line.append(" ")
                                line.append(" ")

                        while(dutySet[i][1] != dutySet[-1][1]):
                            line.append(dutySet[i][2])
                            line.append(dutySet[i][0])
                            i += 1
                        if dutySet[i][1] == "MUPR":
                            line.append(dutySet[i][2])
                            line.append(dutySet[i][0])
                        while(len(line)<28):
                            line.append(" ")
                        line.append(dutySet[-1][3])
                        line.append(dutySet[-1][0])
                        line.append(dutySet[-1][4])
                        line.append(trainNum)
                        
                sheet.append(line)
                i += 1

    sheet.sort(key= lambda x:(x[4],x[27]))
    customSort(sheet)
    with open(op, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        header = ["TRAIN NO." ,"Induction Station", "Induction Time","DUTY NO.", "MKPR", "DUTY NO.", "PVGW DN", "DUTY NO.","IPE", "DUTY NO.", "KKDA DN", "DUTY NO." ,"MUPR","DUTY NO.", "SVVR", "REVERSAL FROM", "TRAIN NO.", "SVVR","DUTY NO.", "MUPR", "DUTY NO.","KKDA UP","DUTY NO.","IPE", "DUTY NO.", "PVGW UP","DUTY NO.","MKPR", "Stabling Station ", "DUTY NO.", "Stabling Time", "TRAIN NO."]
        writer.writerow(header)
        for row in sheet:
            writer.writerow(row)

def verification(dutiesDict, op):
    trainDuty = {}
    KKDA_no, PBGW_no, dist = 201,501,1
    dutyNo = 0

    for dutyNum, servSet in dutiesDict.items():
        servSet1 = []
        for ax in servSet:
            for ss in range(len(df)):
                if ax == df.iloc[ss,0]:
                    for serv in range(len(df1)):
                        if float(df1.iloc[serv,0]) == df.iloc[ss,12] or df1.iloc[serv,0] == df.iloc[ss,11]:
                            servSet1.append([df1.iloc[serv,1],df1.iloc[serv,2],df1.iloc[serv,3],df1.iloc[serv,4],df1.iloc[serv,5],df1.iloc[serv,6],df1.iloc[serv,7]])

        if (servSet1[0][1] in cc1 and servSet1[-1][3] in cc1):
            dutyNo = PBGW_no
            PBGW_no += 1
        elif (servSet1[0][1] in cc2 and servSet1[-1][3] in cc2):
            dutyNo = KKDA_no
            KKDA_no += 1
        else:
            dutyNo = dist
            dist += 1

        for service in servSet1:
            trainNum = service[0]               
            if trainNum not in trainDuty:
                trainDuty[trainNum] = list()
            trainDuty[trainNum].append([dutyNo] + service[1:])  
    """
    with open(op, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        header = [f"{ordinal(i)} person" for i in range(1, 40 + 1)]
        writer.writerow(['Train No.'] + header)
        # Write data
        for trainNum, dutySet in trainDuty.items():
            dutySet.sort(key=lambda x:x[2])
            writer.writerow([trainNum] + dutySet)

    sys.exit()
    """
    for trainNum, dutySet in trainDuty.items(): 
        dutySet.sort(key=lambda x:x[2])
    
    if True:
        sheet = []
        for trainNum, dutySet in trainDuty.items():
            for duty in dutySet:
                sheet.append([trainNum,duty[1],duty[2],duty[3],duty[4],duty[0]])
        sheet.sort(key=lambda x:x[0])
        with open(op, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            header = ["Rake Num", "Start Stn", "Start Time", "End Stn", "End Time", "Duty Num"]
            writer.writerow(header)
            writer.writerow(sheet[0])
            for i in range(1,len(sheet)):
                if sheet[i][0] != sheet[i-1][0]:
                    writer.writerow([" "," "," "," "," "," "])
                writer.writerow(sheet[i])




printRoster(dutiesDict, f"{outputLocation}RosterDMRC.csv")
print("Roster generated and saved in ouFiles")
verification(dutiesDict, f"{outputLocation}mainLoopVerification.csv")
print("verification file is generated")
printChart(dutiesDict, f"{outputLocation}tripChart.csv")
print("Main Loop Tripchart generated and saved in ouFiles")

