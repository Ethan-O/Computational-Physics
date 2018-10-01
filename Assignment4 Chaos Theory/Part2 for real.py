# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 20:41:55 2018

@author: ethan
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 16:59:14 2018

@author: ethan
Python 3
"""
#Importing libraries
import numpy as np

import matplotlib.pyplot as plt


def pendulum_path(ang_i, q=1/2, FD=1.2, delta_t =0.02, size = 8000000):
    #Intializing Values
    g= 9.8
    L= g
    freqD = 2.0/3.0
    drive_period = 2*np.pi/freqD
    cycle_out = 100
    ##Intializing arrays
    theta = np.zeros(size)
    omega = np.zeros(size)
    t = np.zeros(size)
    
    #These arrays collect the values of theta > 2 and where drive theta = 0
    theta[0]= ang_i
    theta2 = []
    omega2 =[]
    t2 = []
    
    #Calculation loop
    for i in range(size-1):
        #Runge-Kutta Method
        #k2 = f(0i,ti,wi)
        #k3 = wi + 1/2 k2 *dt
        #k4 = f(0i + 1/2*k1 *dt, ti +1/2*dt, wi+ 1/2*dw/dt)
        # dw/dt = FD*FreqD*cos(FreqD*(ti))
        k2 = -g/L*np.sin(theta[i]) -q*omega[i] + FD*np.sin(freqD*t[i])
        k3 = omega[i] + 1/2*k2*delta_t
        k4 = -g/L*np.sin(theta[i]+1/2*omega[i]*delta_t) - q*(omega[i] + 1/2*delta_t*FD*freqD*np.cos(freqD*(t[i]))) + FD*np.sin(freqD*(t[i]+1/2*delta_t))
        
        theta_i1 = theta[i] + k3*delta_t
        omega_i1 = omega[i] + k4*delta_t
        t_i1 = t[i] + delta_t
        
        #Checking for out of bounds angles
        if(abs(theta_i1) > np.pi ):
            theta_i1 = theta_i1 + np.sign(theta_i1)*-1*2*np.pi
            
        # Storing this iterations values
        theta[i+1] = theta_i1
        omega[i+1] = omega_i1
        t[i+1]= t_i1
            
        # Selecting the points with theta's larger the 2
        if(theta_i1 > 2 and t_i1 % drive_period<0.5*delta_t and t_i1/drive_period>=cycle_out):
            theta2.append(theta_i1)
            omega2.append(omega_i1)
            t2.append(t_i1)

    return theta2, omega2, t2



def ang_diff(x,y):
    
    if(abs(x-y)//np.pi >0):
        diff = 2*np.pi-abs(x-y)
    else:
        diff = abs(x-y)
    return diff

#Generating paths

theta1, w1, t1 = pendulum_path(0.2)

fig = plt.figure()

#First chart
plt.subplot(111)
plt.scatter(theta1,w1,s=.1)
plt.title('PoinCare Plot')
plt.ylabel("Omega (radians/s)")
plt.xlabel("Theta (radians)")
#Please wait a miniute

