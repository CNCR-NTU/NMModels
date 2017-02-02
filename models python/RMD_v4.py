# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 12:31:07 2016

@author: sst3costaa
"""

from scipy import *
from numpy import *
from pylab import *
#from scipy import signal
#from RK2_m import *

global stim, stim_start, stim_end, Vm, Vm1, Vm2, T

Vm1=-70;    "Resting membrane potential 1"
Vm2=-35;    "Resting membrane potential 2"
    
T=1200
  
stim_start = 100.0
stim_end = 500.

def I(t):
    if stim_start < t < stim_end:
        return 10.0
    elif 800 < t < 1000:
        return -10
    else:
        return 0.0

def f(t):
    return 1/(1+exp(-0.001*t))
   
def A(t):
    if Vm==Vm2:
        m=0.93
    else:
        m=0.4
    a=(0.04166/(0.0179+exp(-0.7376*I(t))))+0.3341#I[t]*0.2561+0.04766
    A = -a*(abs(I(t))+I(t))/(2*I(t))+m*(abs(I(t))-I(t))/(2*I(t))
    return A

def B(t):
    b=0.04*(1.103*I(t)**2-4.518*I(t)+14.84)/(I(t)**2-15.28*I(t)+79.42)
    B=b*(abs(I(t))+I(t))/(2*I(t))-0.04*(abs(I(t))-I(t))/(2*I(t))
    return B

def C(t): 
    C=126.66
    return C

def D(t):
    d = 7.851e-5/(1.711e-6+exp(-2.258*I(t)))+0.1244
    D = d-70*(abs(I(t))+I(t))/(2*I(t))-Vm*(abs(I(t))-I(t))/(2*I(t))
    return D

def RMD(x, t):
    return A(t)*x + B(t)*I(t)
    
def RK2(x, f, t0):
    h = 0.05
    k1 = f(x, t0)#-B(t0)*x + A(t0)*I(t0)# f(x, t0)
    q = x + k1*h/2.
    k2 = f(q, t0+h/2.)#-B(t)*q+A(t)*I(t0+h/2.)#f(q, t0+h/2.)
    return x + k2*h
    

V=zeros(T);
stimulus=zeros(T)
V[0]=Vm1
Vm=Vm2
x=0
s=0;

for t in range(0,T-1):
    stimulus[t]=I(t)
    if I(t)>0.0 or I(t)<0.0:
        x = RK2(x, RMD, t)
        V[t+1] = C(t)*x + D(t)
    else:
        x = 0
        if not I(t)==I(t-1):
            s=0
        if V[t]>=Vm2:
            "Negative sigmoid function to Vm2"
            V[t+1]=0.1*(Vm2-V[t])*f(s)+V[t]
            s+=1;
            Vm=Vm2
        elif V[t]<Vm2:
            "Positive sigmoid function to Vm1"
            V[t+1]=0.1*(Vm1-V[t])*f(s)+V[t]
            s+=1;    
            Vm=Vm1        


#b, a = signal.butter(3, 0.1, 'low')
#r=15*(random(T)-0.5)
#n = signal.filtfilt(b, a, r, padlen=150)
#V=V + n
t=0.05*arange(0,T)

stim = 1
stim_start = 100.0
stim_end = 600.

suptitle("C elegans neuron model - RMD", fontsize=16)
subplot(211)
show()
title("Action potential")
xlabel('Time [ms]')
ylabel('Action potential [mV]')
plot(t, V, color='r', label='Action Potential')


subplot(212)
title("Stimulus")
xlabel('Time [ms]')
ylabel('Current in [mA]')
plot(t, stimulus, color='b', label='Spikes')
axes = gca()
axes.set_ylim([15,-15])
show()