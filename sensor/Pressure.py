import spidev
import time
import io
import sys
import csv
import signal
import os

def Pressure(n):

    class MCP3208:
        def __init__(self, spi_channel=0):
                self.spi_channel = spi_channel
                self.conn = spidev.SpiDev(0, spi_channel)
                self.conn.max_speed_hz = 1000000 # 1MHz

        def __del__( self ):
                self.close

        def close(self):
                if self.conn != None:
                        self.conn.close
                        self.conn = None

        def bitstring(self, n):
                s = bin(n)[2:]
                return '0'*(8-len(s)) + s

        def read(self, adc_channel=0):
                # build command
                cmd  = 128 # start bit
                cmd +=  64 # single end / diff
                if adc_channel % 2 == 1:
                        cmd += 8
                if (adc_channel/2) % 2 == 1:
                        cmd += 16
                if (adc_channel/4) % 2 == 1:
                        cmd += 32

                # send & receive data
                reply_bytes = self.conn.xfer2([cmd, 0, 0, 0])

                #
                reply_bitstring = ''.join(self.bitstring(n) for n in reply_bytes)
                # print reply_bitstring

                # see also... http://akizukidenshi.com/download/MCP3204.pdf (page.20)
                reply = reply_bitstring[5:19]
                return int(reply, 2)
            
    spi = MCP3208(0)

    count = 0
    a0 = 0

    # The following code will write the Process ID of this script to a hidden file
    pid = os.getpid()
    PIDfilename = ".PID"
    PIDfile = open(PIDfilename, "wt")
    PIDfile.write(str(pid))
    PIDfile.close()

    filename = '/sensor/HistoryData/Pressure/Pressurelogg.csv'
    with open(filename, "at") as ofile:					      
        writer = csv.writer(ofile)						
        writer.writerow(("Time", "Pressure"))
        
        while True:
            count += 1
            a0 += spi.read(0)

            if count == 10:
                a0 = a0/10
		a0 = (0.066667*a0)-16.6
		if a0 <= 0:
		    a0 = 1
                if count >= 10:
                    Time = str(time.strftime('%X'))				
                    writer.writerow((Time, a0))
                    break
                count = 0

    return(a0)
