# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 15:36:37 2018

@author: ethan
"""

import numpy as np
from numpy.random import *
import matplotlib.pyplot as plt





def walk2D(n=100,w=500,step_mag=1):
    #Intialize time size and number of walkers
    # n is time steps, w is number of walkers
    #Intialize array of mean squared displacements

    #Intialize array of current walker positions
    twxy = np.repeat(50.0,n*w*2).reshape((n,w,2))

    for j in range(w):
    
        for i in range(n-1):
           
            # Using the hypersphere point picking method of choosing a direction in n dimensional space
            # http://mathworld.wolfram.com/HyperspherePointPicking.html
            x = randn()*step_mag
            y = randn()*step_mag
            
            mag = np.sqrt(x**2+y**2)
            x = x/mag
            y = y/mag
            twxy[i+1,j] = twxy[i,j] + [x,y]
        
            
    return twxy




def create_partitions(twxy,n_xparts=9, n_yparts=9, fixed=False, x_lim=(0,100), y_lim=(0,100)):
#For Determining entropy, the grid is broken up into 81 equal area partitions

    #If the grid is fixed, then we create the partition from the fixed grid limits
    #Note if the fixed grid is larger than the number of steps, particles can leave the system
    if(fixed):
        
        dx = (x_lim[1]-x_lim[0])/n_xparts
        dy = (y_lim[1]-y_lim[0])/n_yparts
        x_partitions = np.arange(x_lim[0],x_lim[1]+0.1,dx)
        y_partitions = np.arange(x_lim[0],x_lim[1]+0.1,dy)
    else:
    #The Height of each box will be the difference between the lowest and highest particle, times 1/9
    # Likewise for horizontal distance length.
    #Number of partition lines, 81 boxes means 10 verticle and 10 horizontal lines
        n= twxy.shape[0]
        x_min = twxy[1,1,0]
        x_max = twxy[1,1,0]
        
        y_min = twxy[1,1,0]
        y_max = twxy[1,1,0]
        #Finding the minimum and maximum points for all time steps
        for nw in twxy[:,:,0]:
            for x in nw:
                if(x < x_min):
                    x_min= x
                if(x > x_max):
                    x_max = x
                    
        for nw in twxy[:,:,1]:
            for y in nw:
                if(y < y_min):
                    y_min= y
                if(y > y_max):
                    y_max = y
        
        
        #The extra 0.2 is so the boundary points are included in the partition
        dx = (x_max - x_min +0.2)*1/n_xparts
        dy = (y_max - y_min +0.2)*1/n_yparts
        
        # The extra +1 is so the last line is included 
        x_partitions = np.arange(x_min-0.01,x_max+0.01+1,dx)
        y_partitions = np.arange(y_min-0.01,y_max+0.01+1,dy)
        
    return x_partitions,y_partitions

#Counts the Points within each partition
def point_count(twxy,x_parts,y_parts):
    n = twxy.shape[0]
    
    x_points = twxy[:,:,0]
    
    y_points = twxy[:,:,1]
    
    n_xparts = x_parts.shape[0]-1
    n_yparts = y_parts.shape[0]-1
  
    occupency = np.repeat(0.0,n*n_xparts*n_yparts).reshape(n,n_xparts,n_yparts)
    x_pos = 0
    y_pos = 0
    
    
    for i in range(n):
        for j in range(w):
            x_pos = "Error"
            y_pos = "Error"
            for x in range(n_xparts):
                #print(x_points[i,j],i,j)
                if(x_parts[x+1]>= x_points[i,j] >= x_parts[x]):
                    x_pos = x
                    
            if(x_pos == "Error"):
                print(i,j)
                    
            for y in range(n_yparts):
                if(y_parts[y+1]>= y_points[i,j] >= y_parts[y]):
                    y_pos = y
            occupency[i,x_pos,y_pos] += 1
    
    return occupency


#Calculates entopy for each time step
def calc_entropy(box_counts,w):
    n , n_xparts, n_yparts= box_counts.shape 
    S = np.array([0.0]*n)
    for i in range(n):
        for x in range(n_xparts):
            for y in range(n_yparts):
                p= box_counts[i,x,y]/w
                if p ==0:
                    continue
                
                S[i] += -p*(np.log(p))
    return S

w=500
n= 200
twxy = walk2D(n=n,w=500)
x_points = twxy[:,:,0]
y_points = twxy[:,:,1]

x_partitions, y_partitions = create_partitions(twxy,fixed=False)

box_counts = point_count(twxy,x_partitions,y_partitions)

entrop= calc_entropy(box_counts,w)


plt.figure()
plt.xlim([min(x_partitions)-.01, max(x_partitions)+.01])
plt.ylim([min(y_partitions)-.01, max(y_partitions)+.01])
plt.scatter(twxy[20-1,:,0],twxy[20-1,:,1],s=1)
#Drawing the Grid
for x in x_partitions:
    plt.axvline(x, color='black')
for y in y_partitions: 
    plt.axhline(y,color='black')

plt.scatter(50,50,color='red')
#plt.plot(np.array(range(100))*0.0005)
plt.title("500 2D Random Walk Particles without bounds Final Step")
plt.ylabel("Vertical Distance")
plt.xlabel("Horizontal Distance")
plt.show()

plt.figure()
plt.plot(range(n),entrop)
plt.title("Entropy of the System Over Time")
plt.ylabel("Entropy")
plt.xlabel("Time Steps")
plt.show()

    



