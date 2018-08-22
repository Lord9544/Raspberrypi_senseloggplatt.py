#!/usr/bin/python


#Lib
import csv
import math
import sys
import time
#import BattStatus
import coretemp
#import I2cTemp
#import Voltage
import Pressure

#Variables

# Calling functions/scripts

Pressure = Pressure.Pressure(1)			# Reading "a0" spi, 10x samples, returning a0/10. 
#print(Pressure)					# Returned variable for usage

coretemp = coretemp.coretemp(1)			# Reading "Cputemp" on raspberry pi "coretemp"
#print(coretemp)					# Returned variable for usage


row0=["Coretemp,Pressure"]
row1=[coretemp,Pressure]

with open ('/data/euroskilt/opc/work/csvSensor/Sensordata.csv', "w") as f:
    thewriter=csv.writer(f, delimiter=',',)

    for x in range(0, 1):

        thewriter.writerow(row0)
        thewriter.writerow(row1)

        time.sleep(1)

        f.close()



