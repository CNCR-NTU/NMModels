# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 15:26:25 2016

@author: pedromachado
"""

#import serial
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
cycles1=500
v_th=30 #mv
time_step=0.5
## (A) tonic spiking
# a=0.02, b=0.2, c=-65, d=6, v0=-70, w1+w2=14)
## (B) Phasic spiking
# a=0.02, b=0.25, c=-65, d=6, v0=-64, w1+w2=0.7
## (C) tonic bursting
# a=0.02, b=0.25, c=-50, d=2, v0=-70, w1+w2=1.0

a=0.02
b=0.2
c=-65.0
d=6.0
w11=7.0
w22=7.0
av=-70.0
mr=-14.0


#cycles=struct.pack('>H',cycles1)
#v_th=struct.pack('>H',v_th)
#time_step=struct.pack('>f',time_step)
#a=struct.pack('>f',a)
#b=struct.pack('>f',b)
#c=struct.pack('>f',c)
#d=struct.pack('>f',d)
#w1=struct.pack('>f',w11)
#w2=struct.pack('>f',w22)
#av=struct.pack('>f',av)
#mr=struct.pack('>f',mr)
#
#
#
#
#port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=0)
#print ("connected to: " + port.portstr)
#fp=open('IZK.hex', 'wb+')
#fp.close()
#port.write(bytes([reset]))
#time.sleep(1);
#txTime=time.time()
##start byte
#port.write(bytes([stByte]))
#port.write(cycles)
#port.write(v_th)
#port.write(time_step)
#port.write(a)
#port.write(b)
#port.write(c)
#port.write(d)
#port.write(w1)
#port.write(w2)
#port.write(av)
#port.write(mr)
##stop byte
#port.write(bytes([stByte]))
#txTime=round(time.time()-txTime,4)
#print("Transmitted in ", str(txTime), "s")
#count=0
#np=True
#last_time=time.time()
#print("Receiving data from the FPGA...")
#txTime=time.time()
#while np:
#    line =port.read(7) # should block, not take anything less than 1500 bytes
#    if line:
#        fp=open('IZK.hex', 'ab+')  
#        #print (str(count)+" "+str(binascii.hexlify(line)))   
#        fp.write(line)
#        fp.close()
#        count=count+1
#        last_time=time.time()
#    now=time.time()
#    if now-last_time>1.0:
#        np=False    
#port.close()
#txTime=round(time.time()-txTime,4)
#print("Received in ", str(txTime), "s")
#print("All Data was received with success!")
#print ("Port closed with success!")
#
#
#file1 = open('IZK.hex',"rb") 
#blocksize = 450000000 #56.25 MB
##reads from that block from the file and concatenates the values into string
#with file1:
#    block = file1.read(blocksize)
#    rawHex = ""
#    for ch in block:
#        # [2:] helps get rid of 0x and zfill(2) makes sure that the hex are represented into two hex numbers
#         rawHex += hex(ch)[2:].zfill(2)
#rawHex=binascii.a2b_hex(rawHex)
##print(rawHex)
#file2 = open('IZK.csv',"w+")
#file2.close()
#
#file2 = open('IZK.csv',"a+")
##opening a file to write the output
#for i in range (0,len(rawHex),7):
#    timestamp=struct.unpack('>H',rawHex[i:i+2])[0]
#    value=struct.unpack('>f',rawHex[i+2:i+6])[0]
#    spike=struct.unpack('B',rawHex[i+6:i+7])[0]
#    file2.write('%s'%timestamp)
#    file2.write(';')
#    file2.write('%s'%value)
#    file2.write(';')
#    file2.write('%s'%spike)
#    file2.write(';')
#    file2.write('\n')
#file2.close()
#print("Check log.txt file to see the output")
#call(["cat", "log.csv"])
print ("[SMC] Sending data to the HMC: \n")

print ("[SMC] Receiving data from the HMC...\n\n\n ")

print("[SMC] Simulation completed!")

weight=w11+w22
stimulus=np1.zeros(cycles1-1)
for i in range(0,cycles1-1,1):
    stimulus[i]=weight

data = np1.genfromtxt('IZK.csv', delimiter=';', names=['timestamp', 'AP', 'Spike'])

plt.figure(1)
plt.suptitle("FPGA results IZK - Tonic spike - Neuron 1", fontsize=16)
plt.subplot(2,2,1)
plt.title("Action Potential")
plt.xlabel('Time [ms]')
plt.ylabel('Voltage [mV]')

plt.plot(data['timestamp'], data['AP'], color='r', label='Action Potential')

plt.subplot(2,2,2)
plt.title("Spikes")
plt.xlabel('Time [ms]')
plt.ylabel('0 or 1')
plt.plot(data['timestamp'], data['Spike'], color='g', label='Spikes')

plt.subplot(2,2,(3,4))
plt.title("Stimulus")
plt.xlabel('Time [ms]')
plt.ylabel('Current [mA]')
plt.plot(data['timestamp'], stimulus, color='b', label='Stimulus')
axes = plt.gca()
axes.set_ylim([0,15.2])
plt.show()

print("Data ploted")
