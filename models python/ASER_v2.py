# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 15:38:43 2016

@author: sst3costaa
"""

#from scipy import signal
from numpy import *
import pylab

global T
global Vm
#global T_prev

Vm=-60.    #Resting membrane potential
T=3500
#T_prev=1000

def I(t):
    if 100 < t < 600:
        return 4.
    elif 1200< t < 1700:
        return 4.
    elif 2300 < t < 2800:
        return 4.
    else:
        return 0.0
        
def ASER(x, t0):
    return -0.8*x+0.064*I(t0)/sqrt(abs(I(t0)))
    
def RK2(x, f, t0):    
    h=0.05             #Steps of 1 millisecond
    k1=f(x, t0)
    q=x+k1*h/2.;
    k2=f(q, t0+h/2.)
    return x+k2*h
    
#def RK2(u, u2, x, A, B):
#    h=0.001;
#    k1=-B*x+A*u;
#    q=x+k1*h/2.;
#    k2=-B*q+A*u2;
#    return x+k2*h
    
#def LTI(u_1, u, qstar, A, B):
#    qstar=RK2(u_1, u, qstar, A, B)      
#    return qstar

#def f(t):
#    return 1/(1+exp(-0.001*t))
      

V=zeros(T);
V[:]=Vm;
v=0
x=0
step=0.005
t1=1
i=0
state=0
I_prev = 0
icount=0
vcount=[]
tmstp=[]
for t in range(0,T-1):
    if icount<500:
        I_prev=I_prev + I(t)
    else:
        I_prev=0.0
        t1=1.0
        state=0
        t1=0
    if I(t)!=I(t-1) and I(t) != 0.0:
        state+=1
    if I(t)>0 or I(t)<0:
        i=I(t)
#        A=3.2/sqrt(abs(I[t]))
#        B=40
        C=186.66
        if state>1:
            D=Vm
            print(t)
        else:
            D=Vm/2. - Vm/2.*(abs(I(t))-I(t))/(2.0*I(t))
#        qstar=LTI(I[t-1],I[t],qstar, A, B)
        v = RK2(v, ASER, t)
        vcount.append(v)
        tmstp.append(t)
        if I(t)>2:
            state-=1
            V[t+1]=C*v+D+0.0125*t1
            t1+=1
        else:
            V[t+1]=C*v+D

    else:
        v=0
        if I(t)!=I(t-1):
            x=0
            t1=0
        if V[t]>Vm and state<3:
            V[t+1]=-7.292*x**3 + 3.635*x**2 - 5.13*x - 25.6/i - 0.008*I_prev
            x+=step
        else:
            x=0 
    if I(t)==0:
        icount+=1
    else:
        icount=0
t=arange(0,T)
st = map(I, t)
pylab.plot(t, V)
#pylab.plot(t, st,'k')
pylab.title('ASER model')
pylab.ylabel('Membrane Potential [mV]')
pylab.xlabel('Time [s]')
plt.show()
pylab.show()
