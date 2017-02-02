# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 15:06:32 2016

@author: pedromachado
"""

import serial
import time
import sys
import os
from subprocess import call
import struct
import numpy as np1
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import struct
import random
import numpy as np

stim = 1
stim_start = 100.0
stim_end = 600.

stimulus=np.zeros(cycles-1)
for i in range(0,cycles-1,1):
    if (i>=stim_start and i<=stim_end):
        stimulus[i]=stim


data = np1.genfromtxt('AMM.csv', delimiter=';', names=['timestamp', 'Force'])
plt.figure(2)
plt.suptitle("Muscle contraction FPGA 14 - AMM", fontsize=16, color='k')
plt.subplot(321)
plt.show()
plt.title("Muscle 1 contraction", color='k')
plt.xlabel('Time [ms]')
plt.ylabel('Contraction in [%]')
plt.plot(data['timestamp'], data['Force'], color='k', label='Forces')

plt.subplot(322)
plt.show()
plt.title("Muscle 2 contraction", color='g')
plt.xlabel('Time [ms]')
plt.ylabel('Contraction in [%]')
plt.plot(data['timestamp'], data['Force'], color='g', label='Forces')

plt.subplot(323)
plt.show()
plt.title("Muscle 3 contraction", color='c')
plt.xlabel('Time [ms]')
plt.ylabel('Contraction in [%]')
plt.plot(data['timestamp'], data['Force'], color='c', label='Forces')

plt.subplot(324)
plt.show()
plt.title("Muscle 4 contraction", color='m')
plt.xlabel('Time [ms]')
plt.ylabel('Contraction in [%]')
plt.plot(data['timestamp'], data['Force'], color='m', label='Forces')

plt.subplot(325)
plt.show()
plt.title("Muscle 5 contraction", color='b')
plt.xlabel('Time [ms]')
plt.ylabel('Contraction in [%]')
plt.plot(data['timestamp'], data['Force'], color='b', label='Forces')


plt.subplot(326)
plt.title("Stimulus", color='r')
plt.xlabel('Time [ms]')
plt.ylabel('Number of spikes')
plt.plot(data['timestamp'], stimulus, color='r', label='Stimulus')
axes = plt.gca()
axes.set_ylim([0,2])
plt.show()