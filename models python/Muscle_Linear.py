# -*- coding: utf-8 -*-
"""
Created on Fri Mar 04 11:48:09 2016

@author: sst3costaa
"""
from scipy import *
from numpy import *
from pylab import *

global stim, stim_start, stim_end, A, B, C, T, dt

T=1200

# theta3*f''(t)+theta2*f'(t)+theta1*f(t)=theta0*u(t)
theta0=0.023
theta2=0.26
theta3=4.0e-3
D = 1400#theta0/theta3
B = 25#theta2/theta3
C = -1#theta1/theta3
A = 1#theta3

dt = 0.05
stim = 1
stim_start = 100.0
stim_end = 600.

def I(t):
    if stim_start < t < stim_end:
        return stim
    else:
        return 0.0
        
def RK22(v1, v2, t0):
    M1a = 0
    M1b = -C
    M1c = -B
    M1d = -A
    M2a = 0
    M2b = D
    k1a = M1a*v1 + M1b*v2 + M2a*I(t0)
    k1b = M1c*v1 + M1d*v2 + M2b*I(t0)
    q1a = v1 + k1a*dt*0.5
    q1b = v2 + k1b*dt*0.5
    k2a = M1a*q1a + M1b*q1b + M2a*I(t0)
    k2b = M1c*q1a + M1d*q1b + M2b*I(t0)
    q2a = v1 + k2a*dt*0.5
    q2b = v2 + k2b*dt*0.5 
    k3a = M1a*q2a + M1b*q2b + M2a*I(t0)
    k3b = M1c*q2b + M1d*q2b + M2b*I(t0)
    q3a = v1 + k3a*dt*0.5
    q3b = v2 + k3b*dt*0.5
    k4a = M1a*q3a + M1b*q3b + M2a*I(t0)
    k4b = M1c*q3b + M1d*q3b + M2b*I(t0)
    q4a = v1 + (1/6.)*dt*(k1a + 2*k2a + 2*k3a + k4a)
    q4b = v2 + (1/6.)*dt*(k1b + 2*k2b + 2*k3b + k4b)
    return q4a, q4b
    
V = zeros(T)
v1 = 0.0
v2 = 0.0
for i in range(0,T-1):
    v1, v2 = RK22(v1, v2, i)
    V[i+1] = v1
    
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
ax.axison=False
show()