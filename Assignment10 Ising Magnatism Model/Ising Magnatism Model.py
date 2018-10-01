# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 00:28:04 2018

@author: ethan
"""

from numpy import * 
from random import *


def random_init(n):
    lattice = array([0]*n**3)
    for i in range(len(lattice)):
        #Will generate a 1 or -1 with 50% probability
        lattice[i] = int(2*(random() // .5) -1)
    lattice = lattice.reshape((n,n,n))
    return lattice


def calc_flip(lattice,i,j,k,n):
     #Parametric Boundary Conditions
    def correct_edge(x,n_max=n):
        if x < 0:
            x = n_max-1
        if x >= n_max-1:
            x = 0
        return x

    J=1
    E=0
    # Aggregate spin of 6 nearest neighbors
    S = 0

    S+= lattice[correct_edge(i-1),j,k]
    S+= lattice[correct_edge(i+1),j,k]
    
    S+= lattice[i,correct_edge(j-1),k]
    S+= lattice[i,correct_edge(j+1),k]
    
    S+= lattice[i,j,correct_edge(k-1)]
    S+= lattice[i,j,correct_edge(k+1)]

    E = J*S*lattice[i,j,k]*2
    return E


def sweep_temp(lattice,sweeps,Temps):
    kb=1
    Mags = array([0]*len(Temps)*sweeps)
    Mags = Mags.reshape((sweeps,len(Temps)))
    T_count = 0
    lattice_copy = copy(lattice)
    for T in Temps:
        for s in range(sweeps):
        
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        #Calculating electrons change in E from spin flip at i,k,j
                        E_flip = calc_flip(lattice,i,j,k,n)
                        #If Energy is reduced, flip
                        if( E_flip <= 0):
                            lattice[i,j,k] = lattice[i,j,k]*-1
                        else:
                            #If energy is not reduced use metropolis algorithm to estimate higher energy transitions
                            #Described by boltzman distribution
                            u = random()
                            if u <= exp(-E_flip/(kb*T)):
                                lattice[i,j,k] = lattice[i,j,k]*-1
                                
            Mags[s,T_count] = sum(lattice)
        T_count+= 1
        lattice = copy(lattice_copy)
        #print(sum(lattice))
    return array(Mags)


#Temperature, Bolzmann's constant, Magnetic feild Strength
kb=1  #1.38064852* 0**(-23)
n = 10
sweeps = 500
Temps = [2,4,5,10]

lattice = random_init(n)

mags= sweep_temp(lattice,sweeps,Temps)/n**3

import matplotlib.pyplot as plt

plt.figure(1)
plt.cla()
plt.plot(mags[:,0],'r' ,label= 'T=2')
plt.plot(mags[:,1],'b', label= 'T=4')
plt.plot(mags[:,2],'g', label= 'T=5')
plt.plot(mags[:,3],label='T=10')
plt.xlabel("Time Steps")
plt.ylabel("Magnetization (Normalized to 1)")
plt.title("Magetization of Randomized 3D Ising Model")
plt.legend(loc='upper right')
plt.show()

print("Fig1 Generated")
#Now to show how average manetization changes accross many temperatures

lattice = random_init(n)
#Temperature Range, which is close to T_c
T_Range = arange(3,6,.1)
#Number of time steps
sweeps = 200
mag_temps = sweep_temp(lattice,sweeps,T_Range)/n**3 #Normalization

#Suming up each column in mag_temps to get the sweep average magnetization for each temperature
mag_temps_sum = array([sum([mag[i] for mag in mag_temps[:] ]) for i in range(len(mag_temps[1,:]))])/sweeps

plt.figure(2)
plt.cla()
plt.plot(T_Range,mag_temps_sum,'bo')
plt.xlabel("Temperature T")
plt.ylabel("Average Magnetization (Normalized to 1)")
plt.title("Magetization VS Temperature in 3D Ising Model")
plt.show()
print("Fig2 Generated")

#From the Graph it appears the Tc is around 4.5
plt.figure(3)
plt.cla()
plt.plot(T_Range,abs(array(mag_temps_sum)),'go')
plt.xlabel("Temperature T")
plt.ylabel("Average Absolute Magnetization (Normalized to 1)")
plt.title("Absolute Magetization VS Temperature in 3D Ising Model")
plt.show()
print("Fig3 Generated")
#Esitmated from graph
T_c= 4.65
#Last Position where T_C > T_Range
last_T = where((T_c - T_Range) > 0)[0][-1]

#M = A*(Tc-T)^b
#Log(M) = B log(Tc-T) +Log(A)
#The slope of this plot should be b
mag_temps_log = log(abs(array(mag_temps_sum[:last_T])))
T_diff_log = log(T_c-T_Range[:last_T])

#Getting the y intercept for the b estimate line
A = sum(mag_temps_log-0.30*T_diff_log)/len(T_diff_log)

#The red dotted line compares the eyeball estiamate of b with the line
plt.figure(4)
plt.cla()
plt.plot(T_diff_log,mag_temps_log,'b',label="Simulated Data")
plt.plot(T_diff_log,0.30*T_diff_log +A ,'r--',label="Line, b = 0.30, Tc=4.65 ")
plt.xlabel("Log Dfference Between T_c And T")
plt.ylabel("Log Absolute Magnetization (1 Normalized)" )
plt.legend()
plt.title("Estimating b (the slope of log(M) vs Log(Diff T))")
plt.show()
#So we can say 3.0 is a decent estimate of b for the 3D Isis model

print("Fig4 Generated")
