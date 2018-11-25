from Scheduler import *
from tkinter import messagebox

def SRTN(processes, contextSwitchingTime):
    if not len(processes):
        messagebox.showerror('There are not any processes to process!')
        return
    curTime = 0.0
    running = []
    idx = 0         # it indicates the index of last non-scheduled or non-arrived process
    flag = False    # to indicate if there are any processes which haven't arrived yet
    switched = 0    # to indicate the id of process I switched from
    while True:
        flag = False 
        if not len(running) and idx < len(processes):  # save time and jump to the time when the CPU will be running
            curTime = max(curTime, processes[idx].arrivalTime)  # If curTime has already a value => maximize
        for i in range(idx, len(processes)):
            if processes[i].arrivalTime <= curTime:
                idx = i + 1
                running.append(processes[i])
            else:
                flag = True
                break
        running.sort(key = lambda x : x.ETF)    # sort to have the process with the least ETF first
        if not len(running) and idx >= len(processes):  # if I have scheduled all processes
            break
        if switched and len(running) and running[0].id != switched: 
            # If I switched from running process and it didn't terminate, update curTime then repeat the search
            curTime += contextSwitchingTime
            for i in range(idx+1, len(processes)):
                if processes[i].arrivalTime <= curTime:
                    idx += 1
                    running.append(processes[i])
                else:
                    flag = True
                    break
            running.sort(key = lambda x : x.ETF)    # sort to have the process with the least ETF first
        process = running[0]
        if idx >= len(processes) or curTime + process.ETF <= processes[idx].arrivalTime: # if I'm sure that I can end this process without future interrupt
            if process.startTime == -1.0:
                process.setStartTime(curTime)
            process.setFinishTime( curTime + process.ETF )
            process.editETF(process.ETF)
            process.addPeriods(curTime, process.finishTime)
            curTime = process.finishTime + contextSwitchingTime
            running.pop(0)
            switched = 0
        else:
            if process.startTime == -1.0:
                process.setStartTime(curTime)
            process.editETF(processes[idx].arrivalTime - curTime)
            process.addPeriods(curTime, processes[idx].arrivalTime)
            curTime = processes[idx].arrivalTime
            switched = process.id
    return processes

