# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 01:40:15 2015

@author: pmachado
"""

from numpy import *
from pylab import *

## setup parameters and state variables
T       = 200                  # total time to simulate (msec)
dt      = 1               # simulation time step (msec)
time    = arange(0, T+dt, dt) # time array
t_rest  = 0                   # initial refractory time

## LIF properties
Vm      = zeros(len(time))    # potential (V) trace over time
Rm      = 40000                   # resistance (kOhm)
Cm      = 1                  # capacitance (uF)
tau_m   = Rm*Cm               # time constant (msec)
tau_ref = 4                   # refractory period (msec)
Vth     = 30.0                   # spike threshold (V)
V_spike = 2.0                 # spike delta (V)

## Stimulus


## iterate over each time step
for i, t in enumerate(time):
    I = randint(0,2)                 # input current (A)
    if t > t_rest:
      Vm[i] = Vm[i-1] + (I*Rm) / tau_m * dt
    if Vm[i] >= Vth:
      Vm[i] += V_spike
      t_rest = t + tau_ref
      print(t_rest)

## plot membrane potential trace
plot(time, Vm)
title('Integrate-and-Fire', size="large")
ylabel('Membrane Potential (V)')
xlabel('Time (msec)')
ylim([0,50])
show()