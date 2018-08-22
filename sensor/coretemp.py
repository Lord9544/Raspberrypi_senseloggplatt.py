# Import required modules
import io
import time
import sys
import csv
import signal
import os


def coretemp(n):

# The following code will write the Process ID of this script to a hidden file
    pid = os.getpid()
    PIDfilename = ".PID"
    PIDfile = open(PIDfilename, "wt")
    PIDfile.write(str(pid))
    PIDfile.close()

							
    filename = '/sensor/HistoryData/Coretemp/Coretemplogg.csv'		
    with open(filename, "at") as ofile:					      
        writer = csv.writer(ofile)						
        writer.writerow(("Time", "Temperature"))

        f = open("/sys/class/thermal/thermal_zone0/temp", "r")
        t = f.readline ()
        t = t[0:-4]
        cputemp = t
        
        Time = str(time.strftime('%X'))				
        writer.writerow((Time, cputemp))	    
	
    return(cputemp)
