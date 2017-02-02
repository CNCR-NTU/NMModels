from numpy import *
from pylab import *

## setup parameters and state variables
T       = 300                  # total time to simulate (msec)
dt      = 1               # simulation time step (msec)
time    = arange(0, T+dt, dt) # time array
t_rest  = 0                   # initial refractory time

## LIF properties



Av      = zeros(len(time))    # potential (V) trace over time
V      = zeros(len(time))    # Membrane potential (V) trace over time
Ur      = zeros(len(time))    # potential membrane (U) trace over time
spike   = zeros(len(time))    # potential (V) trace over time
Vth = 30.0                   # spike threshold (V)

"""
## (A) tonic spiking
# a=0.02, b=0.2, c=-65, d=6, v0=-70, w1+w2=14)
a = 0.02                   # resistance (MOhm)
b = 0.2                  # capacitance (nF)
c = -65.0               # time constant (msec)
d = 6.0                   # refractory period (msec)
weight1 = 7.0
weight2 = 4.0
Av[0]=-70.0
Ur[0]=-14.0
"""

"""
## (B) Phasic spiking
# a=0.02, b=0.25, c=-65, d=6, v0=-64, w1+w2=0.7
a = 0.02                   # resistance (MOhm)
b = 0.25                  # capacitance (nF)
c = -65.0               # time constant (msec)
d = 6.0                   # refractory period (msec)
weight1 = 0.3
weight2 = 0.334
Av[0]=-64.0
Ur[0]=-14.0
"""


## (C) tonic bursting
# a=0.02, b=0.25, c=-50, d=2, v0=-70, w1+w2=1.0
a = 0.02                 
b = 0.238                 
c = -50.0               
d = 2.2                   
weight1 = 1.0
weight2 = 1.0
Av[0]=-70.0
V[0]=-70.0
Ur[0]=-14.0


## Stimulus
syn1=0
syn2=0

stimulus=zeros(T+1)
## iterate over each time step
for i in range(1,T+1,dt):
    syn1=weight1
    syn2=weight2
    I = syn1+syn2
    stimulus[i-1]=I
    #I       = randint(0,2)                 # input current (A)
    V[i]=Av[i-1]+0.04*Av[i-1]*Av[i-1]*dt+5.0*Av[i-1]*dt+140.0*dt-Ur[i-1]*dt+I*dt
    V[i]=V[i]+0.04*V[i]*V[i]*dt+5.0*V[i]*dt+140.0*dt-Ur[i-1]*dt+I*dt
    if V[i]< Vth:
        Av[i]= V[i]
        Ur[i]= Ur[i-1]+a*b*Av[i-1]-a*Ur[i-1]
    else:
        V[i]=Vth
        Av[i]=c
        Ur[i]=Ur[i-1]+d
        spike[i]=1
        

## plot membrane potential trace
figure(2)
#suptitle("Python simulation IZK (A) tonic spiking", fontsize=16)
#suptitle("Python simulation IZK (B) phasic spiking", fontsize=16)
suptitle("Python simulation IZK (C) tonic bursting", fontsize=16)
subplot(2,2,1)
plot(time, V, 'red')
title('Action Potential', size="large")
ylabel('Action Potential [mV]')
xlabel('Time [ms]')

subplot(2,2,2)
plot(time, spike, 'green')
title('Spikes', size="large")
ylabel('Spikes (0 or 1)')
xlabel('Time [ms]')
show()

subplot(2,2,(3,4))
title("Stimulus")
xlabel('Time [ms]')
ylabel('Current [mA]')
plot(time, stimulus, color='b', label='Stimulus')
axes=gca()
axes.set_ylim([0,2.2])
plt.show()