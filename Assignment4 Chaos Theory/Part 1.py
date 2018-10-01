# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 16:59:14 2018

@author: ethan
Python 3
"""
#Importing libraries
import numpy as np

import matplotlib.pyplot as plt


def pendulum_path(ang_i, q=1/2, FD=1.5, length =1, delta_t =0.04, size = 5000):
    #Intializing Values
    g= 9.8
    L= g
    freqD = 2/3
    #Creating arrays
    ang = np.zeros(size)
    w = np.zeros(size)
    t = np.zeros(size)
    #Intializing arrays
    ang[0]= ang_i
    
    #Calculation loop
    for i in range(size-1):
        w[i+1] = w[i] +((g/L)*np.sin(ang[i]) - q*w[i] + FD*np.sin(freqD*t[i]))*delta_t
        ang[i+1] = ang[i] + w[i+1]*delta_t
        t[i+1] = t[i] + delta_t
        
        #Checking for out of bounds angles
        if(abs(ang[i+1]) > np.pi ):
            ang[i+1] = ang[i+1] + np.sign(ang[i+1])*-1*2*np.pi
    return ang, t, w

# Correction for finding the smallest angle difference between two angles
def ang_diff(x,y):
    
    if(abs(x-y)//np.pi >0):
        diff = 2*np.pi-abs(x-y)
    else:
        diff = abs(x-y)
    return diff

#Generating paths
delta= 0.001
pen1, t1, w1 = pendulum_path(.2)
pen2, t2, w2 = pendulum_path(.2+delta)

delta_pen = np.array(list(map(ang_diff, pen1,pen2)))

    
#First chart

fig = plt.figure()

plt.subplot(221)
plt.plot(t1,pen1)
plt.title('Pendulum Path One')
plt.ylabel("0 (radians)")
plt.xlabel("time (s)")
#Second Chart
plt.subplot(222)
plt.plot(t2,pen2)
plt.title('Pendulum Path Two')
plt.ylabel("0 (radians)")
plt.xlabel("time (s)")

#delta Angle Chart
fig2 = plt.figure()
ax2= fig2.add_subplot(111)

ax2.plot(t1,delta_pen)
plt.title('Delta Plot No Scaling')
plt.ylabel("d0 (radians)")
plt.xlabel("time (s)")

#delta Angle Chart
fig2 = plt.figure()
ax2= fig2.add_subplot(111)

ax2.plot(t1,np.log(delta_pen))
plt.title('Log(Delta Plot) No Scaling')
plt.ylabel("d0 (radians)")
plt.xlabel("time (s)")

#delta Angle Chart as Log Plot
fig2 = plt.figure()
ax2= fig2.add_subplot(111)
plt.yscale('log')
ax2.plot(t1,delta_pen)
plt.title('Log Delta Plot AKA The Graded Plot')
plt.ylabel("d0 (radians)")
plt.xlabel("time (s)")


#The slope looks to be about a factor of 2.5 per 15s
#delta_O = e^(Ct)
#log(delta_0) = log(e^(Ct))
# log(delta_0) = C*t
# Log(delta_)/dt = C
# C would be 2.5/15

