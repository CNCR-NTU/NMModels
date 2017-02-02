# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 12:11:28 2016

@author: sst3costaa
"""

from scipy import *
from numpy import *
from pylab import *

global stim, stim_start, stim_end, Cn, force, A, tau, T

T=1200 # 6000

A=100  #1
#a=5
tau1=1 #0.1
tauc=1 #0.1

   
stim = 1
stim_start = 50.0
stim_end = 1000.

def I(t):
    if stim_start < t < stim_end:
        return stim
    else:
        return 0.0
        
        
def CN(Cn, t):
    return -Cn/tauc + I(t)
    
def F(force, t):
    return -force/tau1 + A*Cn

def RK2(v, f, t0):
    h = 0.05
    k1 = f(v, t0)
    q = v + k1*h/2.
    k2 = f(q, t0+h/2.)
    return v + k2*h
    
V = zeros(T)
Cn = 0.0
force = 0.0
for i in range(0,T-1):
    Cn = RK2(Cn, CN, i)
    force = RK2(force, F, i)
    V[i+1] = force
    
t=arange(0,T)
st = map(I, t)
plot(t, V, 'k')
plot(t, 10*asarray(st)-20, 'k')

ylabel('Contraction force (%)')
xlabel('Time (ms)')
#grid()
ax = gca()
#ylim((-30, 101))
#ax.yaxis.set_visible(False)
#ax.axison=False
show()