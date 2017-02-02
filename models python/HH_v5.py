# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 14:12:51 2016

@author: sst3costaa
"""

from numpy import *
from scipy import *
from pylab import *

# Variables
global Cm, gbarNa, gbarK, gbarl, ENa, EK, El, h, T

T = 300
ENa = 55.17     # Reversal potentials, in mV
EK  = -72.14
El  = -49.42
gbarNa = 1.2      # maximum conducances, in mS/cm^2
gbarK  = 0.36
gbarl  = 0.003

Vm  = -60        # Resting membrane potential

Cm  = 0.01     # membrane capacitance, in uF/cm^2
dt = 0.05
t=arange(0,T,dt)

# Input stimulus
def I(t):
    return 0.1

# Definition of differential equations 
def am(v):
    return 0.1*(v+35.)/(1-exp(-(v+35)/10.))

def bm(v):
    return 4.0*exp(-0.0556*(v+60.))
    
def an(v):
    return 0.01*(v + 50.)/(1-exp(-(v + 50.)/10.))

def bn(v):
    return 0.125*exp(-(v + 60.)/80.)
    
def ah(v):
    return 0.07*exp(-0.05*(v + 60.))

def bh(v):
    return 1./(1+exp(-(0.1)*(v + 30.)))

# Runge kutta adaptation of HH 
def HH(y, i):
    v = y[0]
    n = y[1]
    m = y[2]
    h = y[3]
    gNa=gbarNa*(m**3)*h
    gK=gbarK*(n**4)
    gl=gbarl
    
    INa=gNa*(v-ENa)
    IK=gK*(v-EK)
    Il=gl*(v-El)
    
    dydt = zeros(4)
    dydt[0] = ((1/Cm)*(I(i)-(INa+IK+Il)))
    dydt[1] = an(v)*(1-n)-bn(v)*n
    dydt[2] = am(v)*(1-m)-bm(v)*m
    dydt[3] = ah(v)*(1-h)-bh(v)*h
    
    return dydt

# Initialise values

V=zeros(len(t))
m=zeros(len(t))
n=zeros(len(t))
h=zeros(len(t))
spikes=zeros(len(t))    
stimulus=zeros(len(t))  
V[0] = -60
m[0] = am(V[0])/(am(V[0])+bm(V[0]))
n[0] = an(V[0])/(an(V[0])+bn(V[0]))
h[0] = ah(V[0])/(ah(V[0])+bh(V[0]))

# Calculate HH
for i in range(0, len(t)-1):
    stimulus[i]=I(i)
    K1 = HH([V[i], n[i], m[i], h[i]], i)
    k1 = K1[0]
    n1 = K1[1]
    m1 = K1[2]
    h1 = K1[3]
    
    qk1 = V[i] + dt*(0.5*k1)
    qn1 = n[i] + dt*(0.5*n1)
    qm1 = m[i] + dt*(0.5*m1)
    qh1 = h[i] + dt*(0.5*h1)
    
    K2 = HH([qk1, qn1, qm1, qh1], i)
    k2 = K2[0]
    n2 = K2[1]
    m2 = K2[2]
    h2 = K2[3]
    
    V[i+1] = V[i] + dt*k2
    n[i+1] = n[i] + dt*n2
    m[i+1] = m[i] + dt*m2 
    h[i+1] = h[i] + dt*h2
    
    if V[i+1]<V[i] and V[i]>V[i-1] and V[i]>35:
        spikes[i+1]=1;

suptitle("HH neuron model", fontsize=16)
subplot(2,2,1)    
plot(t,V, color='r', label='Action Potential')
title('Action Potential')
ylabel('Action Potential [mV]')
xlabel('Time [ms]')
show() 

subplot(2,2,2)
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
show()
