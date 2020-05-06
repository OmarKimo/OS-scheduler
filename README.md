# OS scheduler
It's an implementation for an Operating systems scheduler which produce schedules of certain processes based on some scheduling alogorithms which are:
1. Non-Preemptive Highest Priority First. (HPF)
2. First Come First Served. (FCFS)
3. Round Robin with fixed time quantum. (RR)
4. Preemptive Shortest Remaining Time Next. (SRTN)

The application is divided into two modules:
* Process generator: generates the processes to be scheduled.
* Scheduler: produces the schedules based on the chosen algorithm and demonstrates these schedules by visual graphs.
