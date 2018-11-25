import numpy as np
from Scheduler import *
from tkinter import *
import tkinter
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.ticker as ticker

def Generator(nameOfFile):
    inputLines = []
    # try to open the input file
    try:
        with open(nameOfFile) as f:
                for line in f: inputLines.append(line)
    except FileNotFoundError:
        messagebox.showerror("Error!", "File does not exist!")
        return
    # take the expected parameters from the input file
    cntProcesses = int(inputLines[0])
    miuArrival, sigmaArrival = map(float , inputLines[1].split())
    miuBurst, sigmaBurst = map(float , inputLines[2].split())
    gammaPriority = float(inputLines[3])
    # generate the arrival times, burst times, and priorities of the processes
    arrivalTimes = np.random.normal(miuArrival, sigmaArrival, cntProcesses)
    burstTimes = np.random.normal(miuBurst, sigmaBurst, cntProcesses)
    priorities = np.random.poisson(gammaPriority, cntProcesses)
    # fix the values
    arrivalTimes = np.round(arrivalTimes, 2)
    arrivalTimes = np.absolute(arrivalTimes)
    burstTimes = np.round(burstTimes, 2)
    burstTimes = np.absolute(burstTimes)
    priorities = np.int_(priorities)
    # create the output file and write to it
    outFile = open('output.txt', 'w')
    print(cntProcesses, file=outFile)
    for i in range(cntProcesses):
        print(i+1, arrivalTimes[i], burstTimes[i], priorities[i], file = outFile)


def readProcesses():
    inputLines = []
    try:
        with open('output.txt') as f:
                for line in f: inputLines.append(line)
    except FileNotFoundError:
        messagebox.showerror("Error!", "File does not exist!")
        return (None, None)
    processes = []
    cntProcesses = int(inputLines[0])
    for i in range(cntProcesses):
        nums = inputLines[i+1].split(' ')
        processes.append( Process(int(nums[0]), float(nums[1]), float(nums[2]), int(nums[3])) )
    processes.sort(key = lambda x: x.arrivalTime)
    idx = {}
    for i in range(cntProcesses): idx[ processes[i].id ] = i
    return (processes, idx)

def DrawGraph(window, algorithm, start, period, id):
        window.geometry("1000x500")
        #fig = Figure(figsize = (5, 4), dpi = 100, edgecolor = 'blue')
        #subplot = fig.add_subplot(111)
        #ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x / 1000))
        #subplot.yaxis.set_major_formatter(ticks_y)
        #subplot.xaxis.set_major_formatter(ticks_y)
        
        #subplot.bar(x = start, height = id, width = period, color = ('purple'), align = "edge")
        #canvas = FigureCanvasTkAgg(fig, master = window)
        #canvas.draw()
        #canvas.get_tk_widget().grid(row = 8, column = 1, sticky = 'w')
        figure = Figure(figsize = (5, 5), dpi = 100)
        subplot = figure.add_subplot(111)
        subplot.set_title("Scheduling Processes with " + algorithm)
        subplot.set_xlabel("Time")
        subplot.set_ylabel("Process_ID")
        subplot.bar(start,id,period,align='edge')
        canvas = FigureCanvasTkAgg(figure, master=window)
        canvas.get_tk_widget().grid(row=10, column=1)
        toolbarframe = Frame(window)
        toolbarframe.grid(row=102, column=1)
        toolbar = NavigationToolbar2Tk(canvas, toolbarframe)
        toolbar.update()

