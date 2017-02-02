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

import numpy as np1
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import numpy as np
import struct
import binascii

cycles=1000
#-------------------------------------------------------------Main Part of the Code---------------------------------------
# DO NOT CHANGE
stByte = struct.pack('>B',255)
reset = struct.pack('>B',238)

# Simulation and model config/initialisation
#time_step 1 ms
time_step=struct.pack('>H',1)
# cycles = 300
cyclesh=struct.pack('>H',cycles)
# abs_ref = 5 ms
abs_ref=struct.pack('>H',5)
# cap = 1 nF
cap=struct.pack('>H',1)
# resistor = 40 MOhm
resistor=struct.pack('>H',40)
#decayP = 10mV
v_res=struct.pack('>H',2)
# v_th = 30 mV
v_th=struct.pack('>H',30)
# weight1 = 2 mA
weight1h=struct.pack('>H',3)
# weight2 = 2 mA
weight2h=struct.pack('>H',4)



port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=0)
print ("connected to: " + port.portstr)
fp=open('LIF.hex', 'wb+')
fp.close()
port.write(reset)
time.sleep(1);
txTime=time.time()
#start byte
#start byte
port.write(stByte)
port.write(time_step)
port.write(cyclesh)
port.write(abs_ref)
port.write(cap)
port.write(resistor)
port.write(v_res)
port.write(v_th)
port.write(weight1h)
port.write(weight2h)
port.write(stByte)
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
        fp=open('LIF.hex', 'ab+')  
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


file1 = open('LIF.hex',"rb") 
blocksize = 450000000 #56.25 MB

with file1:
    block = file1.read(blocksize)
    rawHex = ""
    for ch in block:
        # [2:] helps get rid of 0x and zfill(2) makes sure that the hex are represented into two hex numbers
         rawHex += hex(ch)[2:].zfill(2)
rawHex=binascii.a2b_hex(rawHex)
file1.close()

file2 = open('LIF.csv',"w+")
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
#once the file is completely read, the output file is closed and the opeartion is finished
print("Data anaysed.")
#print("Check log.txt file to see the output")
#call(["cat", "log.csv"])

weight1 = 3.0
weight2 = 4.0
csyn1=0
syn1=0
csyn2=0
syn2=0
stimulus=[]

for i in range(0,cycles-1,1):
    if csyn1< 6:
        csyn1=csyn1+1
        syn1=0
    else:
        syn1=weight1
        csyn1=0
    if csyn2< 13:
        csyn2=csyn2+1
        syn2=0
    else:
        syn2=weight2
        csyn2=0
    stimulus.append(syn1+syn2)

data = np1.genfromtxt('LIF.csv', delimiter=';', names=['timestamp', 'AP', 'Spike'])

plt.figure(1)
plt.suptitle("LIF FPGA results", fontsize=16)
plt.subplot(2,2,1)
plt.show()
plt.title("Action Potential")
plt.xlabel('Time [ms]')
plt.ylabel('Voltage [mV]')

plt.plot(data['timestamp'], data['AP'], color='r', label='Action Potential')

plt.subplot(2,2,2)
plt.title("Spikes")
plt.xlabel('Time [ms]')
plt.ylabel('0 or 1')
plt.plot(data['timestamp'], data['Spike'], color='g', label='Spikes')
plt.show()

plt.subplot(2,2,(3,4))
plt.title("Stimulus")
plt.xlabel('Time [ms]')
plt.ylabel('Current [mA]')
plt.plot(data['timestamp'], stimulus, color='b', label='Stimulus')
axes = plt.gca()
plt.show()
print("Data ploted")