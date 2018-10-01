# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 20:08:15 2018

@author: ethan
"""

# Time independent quantum mechanics - square well with shooting method
# Program to accompany "Computational Physics" by N. Giordano and H. Nakanishi
# Copyright Prentice Hall 1997, 2006
# modified for VPython.
# Yongli Gao, 4/11/2006
import matplotlib.pyplot as plt
from numpy import *
# initialize variables
# psi = wave function  dx = spatial step   square well runs from -xmax to xmax
# V = potential outside well   parity = +1 (even) or -1 (odd)
# b = if psi>b, it is considered diverging and calculation stops
# e = energy and de = energy step
# try first V=100, dx=0.02, no barrier inside (2), even (1), b=100,
# energy=0.5, de=0.05, sde=0.00001 

nsize = 5000
psi = nsize * [0.]
vmax = 100.
dx = 0.02
ans = 2
parity = 1
b = 100.
#.5
energy = 2
de = 0.05
sde = 0.00001

#vmax = float(raw_input("Square well [-1,1] with V=0 inside. V outside => "))
#dx = float(raw_input("step size dx => "))
#ans = float(raw_input("secondary well/barrier inside? yes [1], no [2] => "))
if ans==1:
    #a = float(raw_input("secondary well/barrier at [-a,a]. a => "))
    #v2 = float(raw_input("potential inside => "))
    a = 0.1
    v2 = 1.0
else:
    a=0
    v2=0

#parity = float(raw_input("look for even [1] or odd [-1] parity solution? => "))
if (parity != 1):
    parity = -1
#b = float(raw_input("redefine b as infinity, b => "))
#energy = float(raw_input("initial guess for energy => "))
#de = float(raw_input("initial energy increment => "))
#sde = float(raw_input("stop iteration when de = => "))

def potential(x,v,a,v2): # the potential is 0 inside the box and V outside 
    if abs(x) <= a:
        return v2
    if abs(x) <= 1: # walls are at x = +1 and -1
        return 0.
    else:
        return v


#tlabel = label(pos=(0,2.5,0),text="temperature")

# display the wave function


def dispsi(psi,imax,dx,parity,red):
    points = list()
    for i in arange(-imax,0,1):
        points.append(array([i*dx,parity*psi[-i]]))
    for i in arange(1,imax-1,1):
        points.append(array([i*dx,psi[i]]))
    points = array(points)
    x = points[:,0]
    y = points[:,1]
    line = '0.5'
    width = 0.1
    if (red ==True):
        line = '--r'
        width= 1
    plt.plot(x,y,line,lw=width)
    return


# psi() = wave function, dx = spatial grid size, Vmax is potential outside box
# energy is current best guess for E, de is amount E is changed in hunting
# for a solution

if parity==1:
    psi[0] = 1 # search for an even parity solution
    psi[1] = 1
else:
    psi[0] = -dx
    psi[1] = 0

last_diverge = 0 # use to keep track of direction of last divergence
                 # loop as we zero in on the proper value of E

n=0
more  = 1
while more==1:
  
    n=n+1                       
    i = 1
    k = 1
    while k==1 and i<nsize-1: # integrate from x=0 to 1
        psi[i+1]=2.*psi[i]-psi[i-1]-2.*(energy-potential(i*dx,vmax,a,v2))*\
                   dx**2*psi[i]
        if abs(psi[i+1])>b:
            k = 0 # psi is diverging so stop now
        i = i + 1
    
    if abs(de)<sde:
        print("dE=",de," iteration=",n," Energy=",energy)
        #tlabel.text = "Energy="+str(energy)
        dispsi(psi,i,dx,parity,True)
        more = 0 # done with the simulation
    
    if psi[i] > 0:
        diverge = +1
    else:
        diverge = -1

    if diverge*last_diverge<0:
        de = - 0.625 * de

    energy = energy + de
    last_diverge = diverge
    dispsi(psi,i,dx,parity,False) # display this estimate for psi


plt.vlines(x=1, ymin= 0, ymax = vmax, color='g',alpha=.6)
plt.vlines(x=-1,ymin =0, ymax= vmax, color='g',alpha=.6)
plt.hlines(y=0, xmin=-1, xmax=1, color='g',alpha=.6)

axes = plt.gca()
axes.set_xlim([-1.3,1.3])
axes.set_ylim([-1,2])
