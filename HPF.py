from Scheduler import *

def HPF(processes, contextSwitchingTime):
    if not len(processes):
        messagebox.showerror('There are not any processes to process!')
        return
    running = []
    curTime = 0.0
    idx = 0         # it indicates the index of last non-scheduled or non-arrived process
    while True:
        if not len(running) and idx < len(processes):               # save time and jump to the time when the CPU will be running
            curTime = max(curTime, processes[idx].arrivalTime) + contextSwitchingTime     # If curTime has already a value => maximize
        for i in range(idx, len(processes)):
            if processes[i].arrivalTime <= curTime:
                running.append(processes[i])
                idx = i + 1
            else:
                break
        running.sort()  # the __lt__ [less than] operator in the Process class will make use here ^_^
        # I finished scheduling all processes
        if not len(running) and idx >= len(processes):
            break
        # from the conditions above, I'm sure that there're at least a process in the running queue
        process = running[0]
        running.pop(0)
        if process.startTime == -1.0:
            process.setStartTime(curTime)
        process.setFinishTime( process.startTime + process.burstTime )
        process.addPeriods(curTime, process.finishTime)
        process.editETF(process.ETF)
        curTime += process.burstTime + contextSwitchingTime
    return processes
