# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 15:36:37 2018

@author: ethan
"""

import numpy as np
from numpy.random import *
import matplotlib.pyplot as plt


#Intialize time size and number of walkers
n = 100
w = 500
#Intialize array of mean squared displacements
x2ave = np.zeros(n)
#Intialize array of current walker positions
xyzw = np.array( [np.zeros(w),np.zeros(w),np.zeros(w)])

for j in range(w):

    for i in range(n):
       
        # Using the hypersphere point picking method of choosing a direction in n dimensional space
        # http://mathworld.wolfram.com/HyperspherePointPicking.html
        x = randn()
        y = randn()
        z = randn()
        
        mag = np.sqrt(x**2+y**2+z**2)
        x = x/mag
        y = y/mag
        z = z/mag
        xyzw[:,j] = xyzw[:,j] + [x,y,z]
        x2ave[i] = x2ave[i]+ sum(xyzw[:,j]**2)
#Taking the Mean by dividing by number of walkers           
x2ave = x2ave/w

plt.scatter(range(n),x2ave)
plt.title("Average Squared Displacement From Center Over Time")
plt.xlabel("Time Steps")
plt.ylabel("Average Squared Displacement From Center")

#The Slope is clearly 1, since <r^2>= 2*D*t, where  D = 1/2
