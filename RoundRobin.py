from Scheduler import *

def RoundRobin(processes, contextSwitchingTime, quantum):
    if not len(processes):
        messagebox.showerror('There are not any processes to process!')
        return
    curTime = 0.0
    idx = 0             # it indicates the index of last non-scheduled or non-arrived process
    running = []
    switched = None     # to indicate that I haven't finished a process after a quantum
    while True:
        flag = False    # to check if I add any process
        if not switched and not len(running) and idx < len(processes):   # save time and jump to the time when the CPU will be running
            curTime = max(curTime, processes[idx].arrivalTime) + contextSwitchingTime  # If curTime has already a value => maximize
        for i in range(idx, len(processes)):     # check for arrived processes
            if processes[i].arrivalTime <= curTime:
                idx = i + 1
                running.append(processes[i])
                flag = True
            else:
                break
        if switched:
            running.append(switched)
            if flag or len(running) > 1:    # only switch to another process if there any
                curTime += contextSwitchingTime
                # curTime was changed so repeat the search operation for arrived processes above
                for i in range(idx, len(processes)):     # check for arrived processes
                    if processes[i].arrivalTime <= curTime:
                        idx = i + 1
                        running.append(processes[i])
                    else:
                        break
        # I finished scheduling all processes
        if not len(running) and idx >= len(processes):
            break
        # from the conditions above, I'm sure that there're at least a process in the running queue
        process = running[0]    # pick the first process in the queue
        running.pop(0)          # remove it from the queue [we'll only add it in future if not finished by 'switched' variable]
        if quantum >= process.ETF: # if I can finish this process within quantum
            if process.startTime == -1.0:
                process.setStartTime(curTime)
            process.setFinishTime(curTime + process.ETF)
            process.addPeriods(curTime, process.finishTime)
            curTime += process.ETF + contextSwitchingTime
            process.editETF(process.ETF)
            switched = None
        else:
            if process.startTime == -1.0:
                process.setStartTime(curTime)
            process.setFinishTime(curTime + quantum)
            process.addPeriods(curTime, curTime + quantum)
            curTime += quantum      # we'll increment the contextSwitchingTime only if we switch
            process.editETF(quantum)
            switched = process
    return processes

