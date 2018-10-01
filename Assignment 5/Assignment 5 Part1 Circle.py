# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 00:17:19 2018

@author: ethan
"""

# Planetary motion with the Euler-Cromer method
# based on Giordano and Nakanishi, "Computational Physics"
# Yongli Gao,  2/11/2006
#
# Add a plot for the Earth as the Vpython zooming has failed.
# Yongli Gao,  2/15/2017

from vpython import *
import numpy as np
# possible values x=1, y=0, v_x=0, v_y=2pi, dt=0.002, beta=2
print ("two planet motion")


#Conversions and constants
mtoA = 6.68459e-12
StoY = 3.17098e-8
G = 6.674*10**-11  # m^3⋅kg^−1⋅s^−2
#G = G*mtoA**3*1/StoY**2 # A^3kg^-1 Y^-2

xe = 1.
ye = 0.
ve_x = 0.
ve_y = 6.28

#0.002
dt = 0.0001

#Masses in Kg
me = 5.972e24

ms = 1.989e30

# plot 
window_w = 400
scene1 = display(width=window_w, height=window_w)
earth = sphere(radius=0.1, color=color.green)
earth.trail = curve(color=color.cyan)
sun = sphere(pos=vec(0.,0.,0.), radius = 0.2, color=vec(1,1,1))

# plot earth only
scene2 = display(x=window_w,width=window_w, height=window_w)
earth2 = sphere(radius=0.02, color=color.green)
earth2.trail = curve(color=color.cyan)
sun2 = sphere(pos=vec(0.,0.,0.), radius = 0.1, color=vec(1,1,1))

# x,y = position of planet
# v_x,v_y = velocity of planet
# dt = time step

l1= label(pos=vec(-4,1,0), text='Kinetic E of Earth')
l2 = label(pos=vec(-4,0,0),text='Poetential E of Earth')
l3 = label(pos=vec(-4,-1,0),text='Total E of Earth')

l4 = label(pos=vec(-4,-2,0), text='Ang Momentum Earth')


s1 = 'Kinetic E of Earth: '
s2 = 'Potential E of Earth'
s3 = 'Total E'
s4 = 'Ang Momentum Earth:'


while 1: # use Euler-Cromer method
    rate(1000)
    #for perfectly circular orbit
    re = 1
  
    ve_x = ve_x - 4 * pi**2 * dt * (xe / re**3)
    ve_y = ve_y - 4 * pi**2 * dt * (ye / re**3)

    xe = xe + ve_x * dt
    ye = ye + ve_y * dt

    
    ve = np.hypot(ve_x,ve_y)

    
    #Converting from Au and Years to meters and seconds
    ve = np.hypot(ve_x,ve_y)
    ve = ve*1/mtoA * StoY
    re = re* 1/mtoA
    
    #Calculating Kinetic E, Potential E, Total E, and angular momentum
    ke = 1/2*me*(ve)**2
    pe = -G*ms*me/(re)
    te = ke+ pe
    Le = ve*me/(re*1/(mtoA))
  
    
    l1.text = s1 + str(ke)
    l2.text = s2 + str(pe)
    l3.text = s3+ str(round(te,1))
    
    l4.text = s4 +str(round(Le,1))
    

    
    earth.pos = vec(xe,ye,0.)
    earth.trail.append(pos=earth.pos)
    earth2.pos = vec(xe,ye,0.)
    earth2.trail.append(pos=earth.pos)



