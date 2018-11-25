from ProcessGenerator import *
from Scheduler import *
from RoundRobin import *
from SRTN import *
from FCFS import *
from HPF import *
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import Entry, scrolledtext, messagebox, StringVar, filedialog, Menu, Label, Frame
from tkinter.ttk import Combobox

# create blank window
window = Tk()
window.title("OS Scheduler")
#window.configure(background='white')

# setting window size
window.geometry('700x200')

# get input using entry class
#input_file = Entry(window)
# use the grid function as usual to add it to the window
#input_file.grid(column = 350, row = 200)

# set focus to entry widget -> can write text right away
#input_file.focus()


# set the value of the Label to string
#labelText = StringVar()
#labelFileName = Label(window, textvariable = labelText, height = 4)
#labelFileName.grid(row = 1, column = 1)
#path = StringVar(None)
#fileName = Entry(window, textvariable = path, width = 50)
#fileName.grid(row = 1, column = 2)


# Specify file types (filter file extensions)
inputFileName = ""
fileName = Entry(window, width = 80, state = 'disabled')
fileName.grid(row = 0, column = 1, sticky = E+W+S+N)

def openfile():
    inputFileName = filedialog.askopenfilename(filetypes = (("Text files","*.txt"), ("all files","*.*")))
    fileName.config(state = 'normal')
    fileName.delete(0, END)
    fileName.insert('end', inputFileName)
    fileName.config(state = 'disabled')
    Generator(inputFileName)

openfiles = Button(window, text = "Choose the input file", bg = "light slate gray", fg = "black", command = openfile)
openfiles.grid(row = 0, column = 0)

# create a label widget with font size
cst = Label(window, text = "Enter Context Switching Time")
cst.grid(row = 1, column = 0)

cstIn = Entry(window)
cstIn.grid(row = 1, column = 1)

# create a label widget with font size
quantumLabel = Label(window, text = "Enter quantum [if Round Robin]")
quantumLabel.grid(row = 2, column = 0)

quantumIn = Entry(window)
quantumIn.grid(row = 2, column = 1)


algosLabel = Label(window, text="Choose scheduling algorithm")
algosLabel.grid(row = 3, column = 0)

map = {
        'FCFS': 0, 
        'HPF': 1,
        'RR': 2,
        'SRTN': 3
}

algos = ['FCFS', 'HPF', 'RR', 'SRTN']
choose = Combobox(window, state = 'readonly')
choose['values'] = algos
choose.current(0)
choose.grid(row = 3, column = 1)

def run():
    chosen = choose.get()
    contextSwitchingTime = cstIn.get()
    if contextSwitchingTime == "":
        contextSwitchingTime = 0.0
    else:
        contextSwitchingTime = float(contextSwitchingTime)
    quantum = quantumIn.get()
    if quantum == "":
        quantum = 0.0
    else:
        quantum = float(quantum)
    processes, idxMap = readProcesses()
    if not processes or not idxMap:
        return
    if map[chosen] == 0:
        processes = FCFS(processes, contextSwitchingTime)
    elif map[chosen] == 1:
        processes = HPF(processes, contextSwitchingTime)
    elif map[chosen] == 2:
        processes = RoundRobin(processes, contextSwitchingTime, quantum)
    else:
      processes = SRTN(processes, contextSwitchingTime)
    printsStats(processes, idxMap, map[chosen])
    allPeriods = FetchAllPeriods(processes)
    DrawGraph(window, chosen, allPeriods[0], allPeriods[1], allPeriods[2])

btn = Button(window, text = "run", bg = "white", fg = "green", command = run, font = ("Arial",20))
btn.grid(row = 4, column = 0)

# if you forget to call the mainloop function, nothing will appear to the user
window.mainloop()