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

#--------single precision floating point representation method---
def IEEE_float_representation(Item_Value):
    bias = 127 # bias for 32 bit floating point is 127
    #print(Item_Value[0])
    sign_bit = Item_Value[0]
    Exponent_bits = Item_Value[1:9]
    Mantissa_bits = Item_Value[9:32]
    #print("Sign bit: ", sign_bit)
    #print("Exponent bits: ", Exponent_bits)
   # print("Mantissa bits: ", Mantissa_bits)
    Exponent = int(Exponent_bits,2) - bias
    #print("Exponent:" , Exponent)
    	
    # the decimal point shifted 3 places towards the LSB to get the fractional part
    # we add 1 to the fractional part and shift the decimal point as per the exponent bits
    if Exponent > 0 or Exponent == 0: 
        Fractional_part = Item_Value[Exponent +9:32]
        Shifted_bits = Item_Value[9 :9 + Exponent]
        Integer_part = bin(1)[2:].zfill(1) 
        IEEE_Rep_integer = Integer_part + Shifted_bits
    elif Exponent < 0:
        #negative expnent means the integer part is zero
        #so just the fractional part is calculated and then the final value is multiplied with 2^(exponent)
        #print("Negative Exponent")
        Fractional_part = Item_Value[ 9:32]
        #Shifted_bits = Item_Value[9 +Exponent : 9 ]
        #we keep the integer part as implied 1 to meet the IEEE format
        # the format should look like 1.something
        # for negative exponent. 1.somthing is finlly multiplied with 2^exponent to give, 0.something...
        Integer_part = bin(1)[2:].zfill(1) 
        IEEE_Rep_integer = Integer_part 
    #print "SHifted bits: ", Shifted_bits
    #print "Fractional Part: ", Fractional_part
    #print "Integer Part: ", Integer_part
    #print "IEEE representation Integer: ", IEEE_Rep_integer	
    IEEE_Rep_integer = int(IEEE_Rep_integer,2)
    #print "IEEE rep int in dec: ",IEEE_Rep_integer
    fractionalPart_size = len(Fractional_part)
    #print "Fractional Part size", fractionalPart_size
    count = 0 
    fractional_Value = 0
    #running computation on the fractional part
    for i in range(0,fractionalPart_size,1):
        #print i , Fractional_part[i]
        count = count +1	
        #print "count :",count
        fraction_Value =  int(Fractional_part[i])*2**(-(i+1))
        #binary = int(binary,2)
        #print "binary dec conversion:" , fraction_Value
        fractional_Value +=fraction_Value 
	
    IEEE_Rep_num = IEEE_Rep_integer + fractional_Value
    #checking the sign bit for negative or positive value
    if sign_bit == bin(1)[2:].zfill(1):
        IEEE_Rep_num = -IEEE_Rep_num
        #print "Negative number: ", IEEE_Rep_num
    #for negative exponent, the final result is multiplied with 2^exponent. 
    # this is  special case, 
    if Exponent <0:
        IEEE_Rep_num = (IEEE_Rep_num)*2**(Exponent)
    #print("IEEE rep :", IEEE_Rep_num)
    return IEEE_Rep_num	

#itemval = '10111110011110101110000101001000'

#IEEE_float_representation(itemval)
cycles=300
#-------------------------------------------------------------Main Part of the Code---------------------------------------
# DO NOT CHANGE
stByte = 255
reset = 238

# Simulation and model config/initialisation
#time_step 1 ms
time_stepMSB=0
time_stepLSB=1
# cycles = 300
cyclesMSB=1
cyclesLSB=44
# abs_ref = 5 ms
abs_refMSB=0
abs_refLSB=5
# cap = 1 uF
capMSB=0
capLSB=1
#v_res = 2mV
v_resMSB=0
v_resLSB=2
# v_th = 10 mV
v_thMSB=0
v_thLSB=30
# weight1 = 2 mA
weight1MSB=0
weight1LSB=2
# weight2 = 2 mA
weight2MSB=0
weight2LSB=2



port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=0)
print ("connected to: " + port.portstr)
fp=open('IAF.hex', 'wb+')
fp.close()
port.write(bytes([reset]))
time.sleep(1);
txTime=time.time()
#start byte
port.write(bytes([stByte]))
##time_step 2 bytes
port.write(bytes([time_stepMSB]))
port.write(bytes([time_stepLSB]))
##cycles 2 bytes
port.write(bytes([cyclesMSB]))
port.write(bytes([cyclesLSB]))
##abs_ref 2 bytes
port.write(bytes([abs_refMSB]))
port.write(bytes([abs_refLSB]))
##cap 2 bytes
port.write(bytes([capMSB]))
port.write(bytes([capLSB]))
##v_res 2 bytes
port.write(bytes([v_resMSB]))
port.write(bytes([v_resLSB]))
##v_th 2 bytes
port.write(bytes([v_thMSB]))
port.write(bytes([v_thLSB]))
##weight1 2 bytes
port.write(bytes([weight1MSB]))
port.write(bytes([weight1LSB]))
##weight2 2 bytes
port.write(bytes([weight2MSB]))
port.write(bytes([weight2LSB]))
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
        fp=open('IAF.hex', 'ab+')  
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


file1 = open('IAF.hex',"rb") 
blocksize = 450000000 #56.25 MB
#reads from that block from the file and concatenates the values into string
with file1:
	block = file1.read(blocksize)
	rawHex = ""
	for ch in block:
		# [2:] helps get rid of 0x and zfill(2) makes sure that the hex are represented into two hex numbers
		rawHex += hex(ch)[2:].zfill(2)
#print(rawHex)
#counter to take note of number of iterations
counter = 0
#opening a file to write the output
file2 = open('IAF.csv',"w+")
file2.close()
#file2.write('----Timestamp----   ')
#file2.write(' ----Value-----------   ')
#file2.write('       ----Spike------\n')
#there might be more than one set of hex information
#so it iterates as it breaks the numbers into a group of 7 bytes
for i in range (0,len(rawHex),14):

    NewrawHex = rawHex[i:i+14]
    #print("New Hex", NewrawHex)
    #print(len(NewrawHex))
	
    BinaryValue = ''
    #each byte is analysed and converted to binary
    for i in range (0,len(NewrawHex),2):
        DecValue = int(NewrawHex[i:i+2],16)	
        BinaryValue = BinaryValue + bin(DecValue)[2:].zfill(8)
    #print(BinaryValue, len(BinaryValue))
    timestamp = int(NewrawHex[0:4],16)
    FloatingNumber = BinaryValue[16:47]
	#retrieved binary stream is fed into this function which returns a corresponding float32 number in dec 
    FloatingValue = IEEE_float_representation(FloatingNumber)
    spike = 0
    #FloatingValue=struct.unpack('!f',bytes.fromhex(FloatingNumber))[0]
	#now the LSB is checked to see if there is a spike or not
    if int(BinaryValue[55],2) == 1:
        #print("There is a spike")
        spike = 1
    else:
        #print("No spike") 
        spike = 0
    counter= counter + 1
    #print("Iteration Number:", counter)
    #for each iteration, the values are written
    file2 = open('IAF.csv',"a+")
    file2.write('%s'%timestamp)
    file2.write(';')
    file2.write('%s'%FloatingValue)
    file2.write(';')
    file2.write('%s'%spike)
    file2.write(';')
    file2.write('\n')
    file2.close()
#once the file is completely read, the output file is closed and the opeartion is finished
print("Data anaysed.")
#print("Check log.txt file to see the output")
#call(["cat", "log.csv"])

weight1 = 2.0
weight2 = 2.0
csyn1=0
syn1=0
csyn2=0
syn2=0
stimulus=np.zeros(cycles-1)

for i in range(0,cycles-1,1):
    if csyn1< 3:
        csyn1=csyn1+1
        syn1=0
    else:
        syn1=weight1
        csyn1=0
    if csyn2< 7:
        csyn2=csyn2+1
        syn2=0
    else:
        syn2=weight2
        csyn2=0
    stimulus[i]=syn1+syn2

data = np1.genfromtxt('IAF.csv', delimiter=';', names=['timestamp', 'AP', 'Spike'])

plt.figure(1)
plt.suptitle("FPGA results IAF", fontsize=16)
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
axes.set_ylim([0,5])
plt.show()
print("Data ploted")