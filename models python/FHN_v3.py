# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 11:06:03 2016

@author: sst3costaa
"""
from scipy import *
from numpy import *
from pylab import *

# Variables
global stim, stim_start, stim_end, v, w, a, b, tau, T, dt

T=6000

a=0.7
b=0.8
tau=12.5

   
stim = 0.6
stim_start = 00.0
stim_end = 6000.

dt = 0.05

# Stimulus input
def I(t):
    if stim_start < t < stim_end:
        return stim
    else:
        return 0.0

# Equations of the differential 
def FHN_v(v, t):
    return (v - v**3 - w + I(t))

def FHN_w(w, t):
    return (v + a - b*w)/tau

# Runge kutta
def RK2(v, f, t0):
    k1 = f(v, t0)
    q = v + k1*dt/2.
    k2 = f(q, t0+dt/2.)
    return v + k2*dt
    
# Fitz Nagumo calulation
V = zeros(T)
v = 0.0
w = 0.0
spikes=zeros(T)
stimulus=zeros(T)
for i in range(0,T-1):
    v = RK2(v, FHN_v, i)
    w = RK2(w, FHN_w, i)
    V[i+1] = v*45.0
    stimulus[i]=I(i)
    if V[i+1]<V[i] and V[i]>V[i-1] and V[i]>40:
        spikes[i+1]=1;

# Plots
t=arange(0,T*dt, dt)
#st = map(I, t)
suptitle("FHN neuron model", fontsize=16)
subplot(2,1,1)    
plot(t,V, color='r', label='Action Potential')
title('FHN model')
ylabel('Action Potential [mV]')
xlabel('Time [ms]')
show() 

subplot(2,1,2)
plot(t,spikes, color='g', label='Spikes')
title("Spikes")
xlabel('Time [ms]')
ylabel('0 or 1')
show() 

subplot(2,2,(3,4))
title("Stimulus")
xlabel('Time [ms]')
ylabel('Current [mA]')
plot(t, stimulus, color='b', label='Stimulus')
ylim([0,1])
show()