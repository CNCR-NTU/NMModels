# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 15:26:25 2016

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
import binascii

#-------------------------------------------------------------Main Part of the Code---------------------------------------
# DO NOT CHANGE
stByte = 255
reset = 238

# Simulation and model config/initialisation
# cycles = 300
cycles=1500
time_step=0.5


cycles=struct.pack('>H',cycles)
time_step=struct.pack('>f',time_step)




port = serial.Serial("/dev/ttyUSB1", baudrate=115200, timeout=0)
print ("connected to: " + port.portstr)
fp=open('HH.hex', 'wb+')
fp.close()
port.write(bytes([reset]))
time.sleep(1);
txTime=time.time()
#start byte
port.write(bytes([stByte]))
port.write(cycles)
port.write(time_step)
#stop byte
port.write(bytes([stByte]))
txTime=round(time.time()-txTime,4)
print("Transmitted in ", str(txTime), "s")
count=0
np=True
last_time=time.time()
print("Receiving data from the FPGA...")
txTime=time.time()
while np:
    line =port.read(7) # should block, not take anything less than 1500 bytes
    if line:
        fp=open('HH.hex', 'ab+')  
        #print (str(count)+" "+str(binascii.hexlify(line)))   
        fp.write(line)
        fp.close()
        count=count+1
        last_time=time.time()
    now=time.time()
    if now-last_time>1.0:
        np=False    
port.close()
txTime=round(time.time()-txTime,4)
print("Received in ", str(txTime), "s")
print("All Data was received with success!")
print ("Port closed with success!")


file1 = open('HH.hex',"rb") 
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
file2 = open('HH.csv',"w+")
file2.close()

file2 = open('HH.csv',"a+")
#opening a file to write the output
for i in range (0,len(rawHex),7):
    timestamp=struct.unpack('>H',rawHex[i:i+2])[0]
    value=struct.unpack('>f',rawHex[i+2:i+6])[0]
    spike=struct.unpack('B',rawHex[i+6:i+7])[0]
    file2.write('%s'%timestamp)
    file2.write(';')
    file2.write('%s'%value)
    file2.write(';')
    file2.write('%s'%spike)
    file2.write(';')
    file2.write('\n')
file2.close()
#print("Check log.txt file to see the output")
#call(["cat", "log.csv"])


data = np1.genfromtxt('HH.csv', delimiter=';', names=['timestamp', 'AP', 'Spike'])

plt.figure(1)
plt.suptitle("HH neuron model", fontsize=16)
plt.subplot(211)
plt.show()
plt.title("Action Potential")
plt.xlabel('Time [ms]')
plt.ylabel('Voltage [mV]')

plt.plot(data['timestamp'], data['AP'], color='r', label='Action Potential')

plt.subplot(212)
plt.title("Spikes")
plt.xlabel('Time [ms]')
plt.ylabel('0 or 1')
plt.plot(data['timestamp'], data['Spike'], color='g', label='Spikes')
plt.show()
print("Data ploted")