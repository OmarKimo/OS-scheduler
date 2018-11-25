import numpy as np

defaultPrecision = 2

class Process:
    def __init__(self, id, arrivalTime, burstTime, priority):
        # "ETF" stands for Estimated Time of Finish
        self.id, self.arrivalTime, self.burstTime, self.priority, self.ETF = int(id), float(arrivalTime), float(burstTime), int(priority), float(burstTime)
        self.startTime = -1.0
        self.finishTime = -1.0
        self.periods = []

    def __lt__(self, other):
        if self.priority == other.priority:
            return self.id < other.id
        return self.priority > other.priority

    def addPeriods(self, start, end):
        # merge periods if applicable
        if len(self.periods) and start == self.periods[len(self.periods) - 1][1]:
            start = self.periods[len(self.periods) - 1][0]
            self.periods.pop(len(self.periods) - 1)
        self.periods.append((start, end))

    def setStartTime(self, time):
        self.startTime = time
    
    def setFinishTime(self, time):
        self.finishTime = time

    def editETF(self, minus):
        self.ETF = round(self.ETF - minus, defaultPrecision)
    
    def getWaitTime(self):
        return round(self.TAT() - self.burstTime, defaultPrecision) # or self.startTime - self.arrivalTime

    def TAT(self):
        return round((self.finishTime - self.arrivalTime), defaultPrecision)

    def WTAT(self):
        return round((self.finishTime - self.arrivalTime) / self.burstTime, defaultPrecision)

    def printMySelf(self, outFile):
        print("Process #", self.id, ":", "waiting time =", self.getWaitTime(), "turnaround time =", self.TAT(), "weighted turnaround time =", self.WTAT(), file = outFile)

def FetchAllPeriods(processes):
    allPeriods = []
    for i in range(len(processes)):
        for period in processes[i].periods: allPeriods.append( (period, processes[i].id) )
    allPeriods.sort(key = lambda x: x[0][0])
    idList = []
    periodList = []
    startList = []
    for element in allPeriods:
        idList.append(element[1])
        periodList.append(element[0][1] - element[0][0])
        startList.append(element[0][0])
    return (startList, periodList, idList)

def printsStats(processes, idxMap, algorithm):
    fileName = ""
    if algorithm == 0:
        fileName = "FCFS_Stats.txt"
    elif algorithm == 1:
        fileName = "HPF_Stats.txt"
    elif algorithm == 2:
        fileName = "RoundRobin_Stats.txt"
    else:
        fileName = "SRTN_Stats.txt"
    statsFile = open(fileName, "w")
    AvgTAT = 0.0
    AvgWTAT = 0.0
    for i in range(len(processes)):
        process = processes[  idxMap[i+1] ]      # print the statistics of the process that have an id equal (i+1)
        process.printMySelf(statsFile)
        AvgTAT += process.TAT()
        AvgWTAT += process.WTAT()
    print("Average Turnaround Time =", round(AvgTAT / len(processes), defaultPrecision), "Average Weighted Turnaround Time =", round(AvgWTAT/len(processes), defaultPrecision), file = statsFile)
    