# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 11:43:46 2015

@author: pedromachado
"""

from numpy import *
import numpy as np1
from pylab import *

## setup parameters and state variables
cycles       = 1000                  # total time to simulate (msec)
dt      = 1               # simulation time step (msec)
t_rest  = 5                   # initial refractory time

## SAM properties
Vm      = []    # potential (V) trace over time
spike   = []    # potential (V) trace over time
Rm      = 40                   # resistance (MOhm)
Cm      = 1                  # capacitance (nF)
tau_m   = Rm*Cm               # time constant (msec)
tau_ref = 5                   # refractory period (msec)
Vth     = 30.0                   # spike threshold (V)
decayP = 7.0                 # spike delta (V)
weight1 = 3.0
weight2 = 4.0


## Stimulus
csyn1=0
syn1=0
csyn2=0
syn2=0

## iterate over each time step
t=t_rest
stimulus=[]
time=[]

for t in range(0,cycles,1):
    spike.append(0)
    if t==0:
        Vm.append(0.0)
    else:
        Vm.append(Vm[t-1])
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
    I = syn1+syn2
    stimulus.append(syn1+syn2)
    time.append(t)
    #I       = randint(0,2)                 # input current (A)
    if t > t_rest:
        Vm[t] = Vm[t-1] + (I*Rm) / tau_m * dt -Vm[t-1]/ tau_m * dt 
    if Vm[t-1]>=Vth:
        Vm[t]=Vm[t-1]-decayP
        t_rest = t + tau_ref
    if Vm[t] >= Vth:
        Vm[t] =Vth 
        spike[t]=1

        
        
        #print(t_rest)
        
## plot membrane potential trace
        
data = np1.genfromtxt('SAM.csv', delimiter=';', names=['timestamp', 'AP', 'Spike'])

figure(1)
suptitle("SAM neuron model", fontsize=16)
subplot(321)
plot(time, Vm, 'r')
title('Python simulation', size="large")
ylabel('Membrane Potential (V)')
xlabel('Time (msec)')
subplot(323)
plot(data['timestamp'], data['AP'], color='b', label='Action Potential')
title('FPGA results', size="large")
ylabel('Membrane Potential (V)')
xlabel('Time (msec)')

subplot(322)
plot(time, spike, 'r')
plot(data['timestamp'], data['Spike'], color='b', label='Spikes')
title('Python simulation', size="large")
ylabel('Spikes (0 or 1)')
xlabel('Time (msec)')
subplot(324)
plot(data['timestamp'], data['Spike'], color='b', label='Spikes')
title('FPGA results', size="large")
ylabel('Spikes (0 or 1)')
xlabel('Time (msec)')
subplot(3,2,(5,6))
title("Stimulus")
xlabel('Time [ms]')
ylabel('Current [mA]')
plot(time, stimulus, color='orange', label='Stimulus')
axes = plt.gca()
show()