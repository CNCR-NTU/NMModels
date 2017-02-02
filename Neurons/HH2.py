# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 18:38:03 2015

@author: pedromachado
"""

from scipy import *
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.integrate import odeint
from numpy import *
import numpy as np

def exp1(x):
    return 1+x*(1+0.5*x+0.17*x*x+0.0445*x*x*x)

def hodgkinHuxley(yy, t, p):

	#Name the variables
    V = yy[0]
    n = yy[1]
    m = yy[2]
    h = yy[3]
	
	#Name the parameters
    C_m = p[0]
    V_Na = p[1]
    V_K = p[2]
    V_l = p[3]
    g_Na = p[4]
    g_K = p[5]
    g_l = p[6]
	
	#The injected current? ? ? ? 
    I = p[7]

 
 
	#Auxiliary quantities	
    alpha_n = (0.01*(V+10)) / (exp((V+10)/10) -1 ) 
    beta_n = 0.125 * exp(V/80)	
    alpha_m = (0.1 *(V+25)) / (exp((V+25)/10) -1 ) 
    beta_m  = 4 * exp(V/18)
    alpha_h = 0.07 * exp( V/ 20)
    beta_h = 1 / (exp((V+30)/10) +1 )

    alpha_n1 = (0.01*(V+10)) / (exp1((V+10)/10) -1 )
    beta_n1 = 0.125 * exp1(V/80)	
    alpha_m1 = (0.1 *(V+25)) / (exp1((V+25)/10) -1 ) 
    beta_m1  = 4 * exp1(V/18)
    alpha_h1 = 0.07 * exp1( V/ 20)
    beta_h1 = 1 / (exp1((V+30)/10) +1 )
	

     
	# HH model
    V_dot1 = (-1/C_m) * ( g_K*n*n*n*n*(V-V_K) + g_Na*m*m*m*h*(V-V_Na)+g_l*(V-V_l)-I)
    n_dot1 = alpha_n1 * (1-n) - beta_n1 *n 
    m_dot1 = alpha_m1 * (1-m) - beta_m1 * m 
    h_dot1 = alpha_h1 * (1-h) - beta_h1 * h
    
    V_dot = (-1/C_m) * ( g_K*n*n*n*n*(V-V_K) + g_Na*m*m*m*h*(V-V_Na)+g_l*(V-V_l)-I)
    n_dot = alpha_n * (1-n) - beta_n *n 
    m_dot = alpha_m * (1-m) - beta_m * m 
    h_dot = alpha_h * (1-h) - beta_h * h  
    res=[V_dot1, n_dot1, m_dot1, h_dot1]
    return res


#Define initial conditions for the state variables
y0 = [0,0,0,0]

delta_t=10000
t=np.zeros(delta_t)
for i in range(delta_t):
    t[i]=i/100
#Define time interval and spacing for the solutions
#t = arange(0,100,0.01)

#Define fixed parameters pp. 520 (HH1952 paper)
C_m = 1
V_Na = -115
V_K = 12
V_l = -10.613
g_Na = 120
g_K = 36
g_l = 0.3
#no current? 
I = -20

#Pack the parameters in a single vector
p = [C_m,V_Na, V_K,V_l,g_Na,g_K,g_l,I] 

#Call the integrator 
y = odeint(hodgkinHuxley, y0, t, args=(p,)) 


y_=np.zeros((delta_t,4))
y_[0,:]=y0
    
for i in range(delta_t-1):
    y_[i+1,:]=np.add(y_[i,:],hodgkinHuxley(y_[i,:],t,p))
    

#plt is the alias for matplotlib.pyplot (see imports) 
#Repeat the same thing for different values of I and plot

#subplot2grid allows for placement of subplots in canvas
# (3,1) means that we'll have 3 rows and 1 column of plots
# (0,0) means that whatever is being plotted right after this command, will go on the 0 row 0 col
plt.subplot2grid((3,1),(0,0))

#plt.xlabel("Time (msec)")
#since all plots share the same xlabel, we want to skip the first 2 labels. 
#mpl is an alias for matplotlib (see imports)
plt.gca().xaxis.set_major_locator(mpl.ticker.NullLocator())
plt.title("Hodgkin and Huxley | I=0ma", size="large")
plt.xlabel("Time (msec)")
plt.ylabel("Volts (mV)")
I = 0
p = [C_m,V_Na, V_K,V_l,g_Na,g_K,g_l,I] 
y1 = odeint(hodgkinHuxley, y0, t, args=(p,)) 
plt.plot(t,-y1[:,0])

plt.subplot2grid((3,1),(1,0))
#since all plots share the same xlabel, we want to skip the first 2 labels.
#mpl is an alias for matplotlib (see imports)
plt.gca().xaxis.set_major_locator(mpl.ticker.NullLocator())
plt.title("Hodgkin and Huxley| I=-8.75ma", size="large")
plt.xlabel("Time (msec)")
plt.ylabel("Volts (mV)")
I = -8.75
p = [C_m,V_Na, V_K,V_l,g_Na,g_K,g_l,I] 
y2 = odeint(hodgkinHuxley, y0, t, args=(p,)) 
plt.plot(t,-y2[:,0])

plt.subplot2grid((3,1),(2,0))
plt.title("Hodgkin and Huxley | I=10ma", size="large")
plt.xlabel("Time (msec)")
plt.ylabel("Volts (mV)")
I = -10
p = [C_m,V_Na, V_K,V_l,g_Na,g_K,g_l,I] 
y3 = odeint(hodgkinHuxley, y0, t, args=(p,)) 
plt.plot(t,-y3[:,0])