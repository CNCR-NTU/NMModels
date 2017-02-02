# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#Numerical simulation for FitzHugh-Nagumo equation
#defined as: x(dot) = c(y+x-x**3/3+z)
#            y(dot) = -(x-a+by)/c
from __future__ import division
from scipy import *
from numpy import *
import numpy as np
import pylab
import matplotlib as mp
import sys
#defining the system of the ODE x(dot) and y(dot)
def hugh_nagumo(x,t=0.1,a = 0.75,b = 0.5,c = 1.0, d = 0):
    return np.array([c*(x[0]+ x[1]- x[0]**3/3 + d),-1/c*(x[0]- a + b*x[1])])
#using the runge-kutta 4th order explicit algorithm
def ruge_4kutta(t0 = 0, x0 = np.array([1.]), t1 = 5, dt = 0.01, ng = None):
    tsp = np.arange(t0, t1, dt)
    Nsize = np.size(tsp)
    X = np.empty((Nsize, np.size(x0)))
    X[0] = x0
    for i in range(1, Nsize):
        k1 = ng(X[i-1],tsp[i-1])
        k2 = ng(X[i-1] + dt/2*k1, tsp[i-1] + dt/2)
        k3 = ng(X[i-1] + dt/2*k2, tsp[i-1] + dt/2)
        k4 = ng(X[i-1] + dt*k3, tsp[i-1] + dt)
        X[i] = X[i-1] + dt/6*(k1 + 2*k2 + 2*k3 + k4)
    return X
#plotting the cycles showing the qualitative behaviour the solution to the system of ODE
def do_plot():
    pylab.figure()
    X = ruge_4kutta(x0 = np.array([0.01,0.01]), t1 = 100,dt = 0.02, ng = hugh_nagumo)
    pylab.plot(X[:,0], X[:,1])
    pylab.title("Phase portrait when a, b, c, z > 0")
    pylab.show()
    return
#showing the plot of the fitzhugh-nagaumo using the above simulation
print (do_plot())