# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 11:55:40 2016

@author: pedromachado
"""

import serial
import time
import sys
import os
from subprocess import call
import struct
import numpy as np1
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import struct
import random
import binascii
import numpy as np

cycles=3500
Vm=-60.0
C=1400.0
step=0.005



#-------------------------------------------------------------Main Part of the Code---------------------------------------
# DO NOT CHANGE
stByte = 255
reset = 238
# Simulation and model config/initialisation
#cyclesMSB=23
#cyclesLSB=112
cycles=struct.pack('>H',cycles)
Vm=struct.pack('>f',Vm)
C=struct.pack('>f',C)
step=struct.pack('>f',step)

port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=0)
print ("connected to: " + port.portstr)
fp=open('ASER.hex', 'wb+')
fp.close()
port.write(bytes([reset]))
time.sleep(1);
txTime=time.time()
#start byte
port.write(bytes([stByte]))
port.write(cycles)
port.write(Vm)
port.write(C)
port.write(step)
npi=True
last_time=time.time()
print("Receiving data from the FPGA...")
txTime=time.time()
while npi:
    line =port.read(7) # should block, not take anything less than 1500 bytes
    if line:
        fp=open('ASER.hex', 'ab+')  
        #print (str(count)+" "+str(binascii.hexlify(line)))   
        fp.write(line)
        fp.close()
        last_time=time.time()
    now=time.time()
    if now-last_time>1.0:
        npi=False    
port.close()
txTime=round(time.time()-txTime,4)
print("Received in ", str(txTime), "s")
print("All Data was received with success!")
print ("Port closed with success!")  

file1 = open('ASER.hex',"rb") 
blocksize = 450000000 #56.25 MB
#reads from that block from the file and concatenates the values into string
with file1:
    block = file1.read(blocksize)
    rawHex = ""
    for ch in block:
        # [2:] helps get rid of 0x and zfill(2) makes sure that the hex are represented into two hex numbers
         rawHex += hex(ch)[2:].zfill(2)
rawHex=binascii.a2b_hex(rawHex)
#print(rawHex)
#counter to take note of number of iterations
counter = 0
#opening a file to write the output
file2 = open('ASER.csv',"w+")
file2.close()
#file2.write('----Timestamp----   ')
#file2.write(' ----Value-----------   ')
#file2.write('       ----Spike------\n')
#there might be more than one set of hex information
#so it iterates as it breaks the numbers into a group of 7 bytes
file2 = open('ASER.csv',"a+")
for i in range (0,len(rawHex),7):
    timestamp=struct.unpack('>H',rawHex[i:i+2])[0]
    value=struct.unpack('>f',rawHex[i+2:i+6])[0]
    file2.write('%s'%timestamp)
    file2.write(';')
    file2.write('%s'%value)
    file2.write(';')
    file2.write('\n')
file2.close()
#once the file is completely read, the output file is closed and the opeartion is finished
print("Data anaysed.")    
#print("Check log.txt file to see the output")
#call(["cat", "log.csv"])


stim = 4
stim_start1 = 100
stim_end1 = 600
stim_start2 = 1200
stim_end2 = 1700
stim_start3 = 2300
stim_end3 = 2800
stimulus=np.zeros(cycles-1)
for i in range(0,cycles-1,1):
    if (i>=stim_start1 and i<=stim_end1) or (i>=stim_start2 and i<=stim_end2) or (i>=stim_start3 and i<=stim_end3) :
        stimulus[i]=stim

data = np1.genfromtxt('ASER.csv', delimiter=';', names=['timestamp', 'Ap'])
plt.figure(2)
plt.suptitle("C elegans neuron model - ASER", fontsize=16)
plt.subplot(211)
plt.show()
plt.title("Action potential")
plt.xlabel('Time [ms]')
plt.ylabel('Action potential [mV]')
plt.plot(data['timestamp'], data['Ap'], color='r', label='Forces')
axes = plt.gca()
axes.set_xlim([0,3500])
axes.set_ylim([-60,20])

plt.subplot(212)
plt.title("Stimulus")
plt.xlabel('Time [ms]')
plt.ylabel('Current in [mA]')
plt.plot(data['timestamp'], stimulus, color='b', label='Spikes')
axes = plt.gca()
axes.set_xlim([0,3500])
axes.set_ylim([0,5])
plt.show()
print("Data ploted")