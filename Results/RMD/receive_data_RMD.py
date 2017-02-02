# -*- coding: utf-8 -*-
"""
Created on Thu May 12 12:36:01 2016

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


cycles=1500



#-------------------------------------------------------------Main Part of the Code---------------------------------------
# DO NOT CHANGE
stByte = 255
reset = 238
# Simulation and model config/initialisation
#cyclesMSB=23
#cyclesLSB=112
cycles=struct.pack('>H',cycles)
port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=0)
print ("connected to: " + port.portstr)
fp=open('RMD.hex', 'wb+')
fp.close()
port.write(bytes([reset]))
time.sleep(1);
txTime=time.time()
#start byte
port.write(bytes([stByte]))
port.write(cycles)
npi=True
last_time=time.time()
print("Receiving data from the FPGA...")
txTime=time.time()
while npi:
    line =port.read(7) # should block, not take anything less than 1500 bytes
    if line:
        fp=open('RMD.hex', 'ab+')  
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

file1 = open('RMD.hex',"rb") 
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
#opening a file to write the output
file2 = open('RMD.csv',"w+")
file2.close()

file2 = open('RMD.csv',"a+")
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


data = np1.genfromtxt('RMD.csv', delimiter=';', names=['timestamp', 'Ap'])
plt.figure(2)
plt.title("C elegans neuron model - RMD")
plt.xlabel('Time [ms]')
plt.ylabel('Membrane potential [mV]')
plt.plot(data['timestamp'], data['Ap'], color='r', label='Forces')
axes = plt.gca()
axes.set_xlim([0,1500])
plt.show()
print("Data ploted")