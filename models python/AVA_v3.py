# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 15:12:55 2016

@author: sst3costaa
"""


from numpy import *
from scipy import signal
import pylab

global T
global Vm

Vm=-30;    "Resting membrane potential"
T=1500;    "Time in milliseconds"

stim = 20
stim_start = 50.0
stim_end = 1000.

def I(t):
    if stim_start < t < stim_end:
        return stim
    else:
        return 0.0

def AVA(x, t0):
    return -1.2*x+I(t0)
    
def RK2(x, f, t0):    
    h=0.05             #Steps of 1 millisecond
    k1=f(x, t0)
    q=x+k1*h/2.;
    k2=f(q, t0+h/2.)
    return x+k2*h
    

V=zeros(T)
V[:]=Vm
x=0
for t in range(1,T):
    if I(t)>0 or I(t)<0:
        x=RK2(x, AVA, t)
        V[t]=2.35*x+Vm #+ 2.5*random.random()
    else:
        qstar=0



#b, a = signal.butter(3, 0.1, 'low')
#
#v=10*(random.random(T)-0.5)
#n = signal.filtfilt(b, a, v, padlen=150)
#V=V + n
t=arange(0,T)

pylab.plot(t, V)
pylab.title('AVA model')
pylab.ylabel('Membrane Potential (V)')
pylab.xlabel('Time (msec)')
pylab.show()