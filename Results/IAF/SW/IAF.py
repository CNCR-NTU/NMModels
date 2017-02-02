# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 01:40:15 2015

@author: pmachado
"""

from numpy import *
from pylab import *

## setup parameters and state variables
T       = 300                  # total time to simulate (msec)
dt      = 1               # simulation time step (msec)
time    = arange(0, T+dt, dt) # time array
t_rest  = 0                   # initial refractory time

## LIF properties
Vm      = zeros(len(time))    # potential (V) trace over time
spike   = zeros(len(time))    # potential (V) trace over time
Rm      = 40000                   # resistance (kOhm)
Cm      = 1                  # capacitance (uF)
tau_ref = 5                   # refractory period (msec)
Vth     = 30.0                   # spike threshold (V)
V_spike = 2.0                 # spike delta (V)
weight1 = 2.0
weight2 = 2.0


## Stimulus
csyn1=0
syn1=0
csyn2=0
syn2=0

## iterate over each time step
for i, t in enumerate(time):
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
    if Vm[i]==0.0:
        Vm[i]=V_spike
    I = syn1+syn2
    if t > t_rest:
      Vm[i] = Vm[i-1] + I/Cm*dt
    if Vm[i-1]>=Vth:
        Vm[i]=V_spike
        t_rest = t + tau_ref
    if Vm[i] >= Vth:
        Vm[i] =Vth 
        spike[i]=1

## plot membrane potential trace
figure(2)
suptitle("Python simulation IAF", fontsize=16)
subplot(211)
plot(time, Vm, 'red')
title('Integrate-and-Fire', size="large")
ylabel('Membrane Potential (V)')
xlabel('Time (msec)')
subplot(212)
plot(time, spike, 'green')
title('Integrate-and-Fire', size="large")
ylabel('Spikes (0 or 1)')
xlabel('Time (msec)')
show()