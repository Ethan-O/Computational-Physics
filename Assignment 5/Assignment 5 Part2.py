# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 00:18:11 2018

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

#Mass of the earth and jupitor in solar mass
me = 3.0e-6
mj = 9.5e-4


#Initial Values

xe = 1.
ye = 0.
ve_x = 0.
ve_y = 6.28
xj = 0.
yj = 5.2
vj_x = - 2. * pi / sqrt(yj)
vj_y = 0.
#To make the momentum of the system zero, the sun's momentum must counter the earth and jupitor's
xs = 0
ys = 0

vs_x = -ve_x*me -vj_x*mj
vs_y = -ve_y*me -vj_y*mj

#Time Step interval
dt = 0.02


#Center of Mass
xc = me*xe+mj*xj+1*xs/(me+mj+1)
yc = me*ye+mj*ye+1*ys/(me+mj+1)


# plot 
window_w = 400
scene1 = display(width=window_w, height=window_w)
earth = sphere(radius=0.1, color=color.green)
earth.trail = curve(color=color.cyan)
jupiter = sphere(radius=0.1, color=color.yellow)
jupiter.trail = curve(color=color.cyan)
sun = sphere(radius = 0.05, color=color.red,opacity=0.3)
sun.trail= curve(color=color.cyan)
center = sphere(pos=vec(xc,yc,0.), radius = 0.001, color=color.white)


#Labels
l1= label(pos=vec(-5,5,0), text='Kinetic E of Earth')
l2= label(pos=vec(-5,4.0,0), text='Kinetic E of Jupiter')

l3 = label(pos=vec(-5,3,0), text='Ang Momentum Earth')
l4= label(pos=vec(-5,2,0), text='Ang Momentum Jupiter')

s1 = 'Kinetic E of Earth: '
s2 = 'Kinetic E of Jupiter: '
s3 = 'Ang Momentum Earth:'
s4 = 'Ang Momentum Jupiter: '

while 1: # use Euler-Cromer method
    rate(100)
    #Finding the position Vectors
    re = sqrt(xe**2 + ye**2)
    rj = sqrt(xj**2 + yj**2)
    rs = sqrt(xs**2 + ys**2)
    
    #Finding the Body to Body vectors
    rej = sqrt((xe-xj)**2 + (ye-yj)**2)
    res = sqrt((xe-xs)**2 + (ye-ys)**2)
    rjs = sqrt((xj-xs)**2 + (yj-ys)**2)
    #G*Mu=v^2*r
    
    #Velocity Step
    ve_x = ve_x - 4*np.pi**2*(xe-xs)/(res**3)*dt - 4*np.pi**2*(xe-xj)*mj/(rej**3)*dt
    ve_y = ve_y - 4*np.pi**2*(ye-ys)/(res**3)*dt - 4*np.pi**2*(ye-yj)*mj/(rej**3)*dt
    
    vj_x = vj_x - 4*np.pi**2*(xj-xs)/(rjs**3)*dt - 4*np.pi**2*(xj-xe)*me/(rej**3)*dt
    vj_y = vj_y - 4*np.pi**2*(yj-ys)/(rjs**3)*dt - 4*np.pi**2*(yj-ye)*me/(rej**3)*dt
    
    vs_x = vs_x - 4*np.pi**2*(xs-xj)*mj/(rjs**3)*dt - 4*np.pi**2*(xs-xe)*me/(res**3)*dt
    vs_y = vs_y - 4*np.pi**2*(ys-yj)*mj/(rjs**3)*dt - 4*np.pi**2*(ys-ye)*me/(res**3)*dt
    
    #Position Step
    xe = xe + ve_x * dt
    ye = ye + ve_y * dt
    xj = xj + vj_x * dt
    yj = yj + vj_y * dt
    xs = xs + vs_x * dt
    ys = ys + vs_y * dt
    #Calculating velocity Magnetude
    ve = np.hypot(ve_x,ve_y)
    vj = np.hypot(vj_x,vj_y)
    vs = np.hypot(vs_x,vs_y)
    
    #Calculating Engery and Angular Momentum
    ke = me*1/2*ve**2
    kj = mj*1/2*vj**2
    ks = 1/2*vs**2
    
    Le = me*ve/re
    Lj = mj*vj/rj
    
    #Labels
    l1.text = s1 + str(ke)
    l2.text = s2 + str(kj)
    
    l3.text = s3 +str(Le)
    l4.text = s4 +str(Lj)
    #Updating Body Positions
    earth.pos = vec(xe,ye,0.)
    earth.trail.append(pos=earth.pos)
    jupiter.pos = vec(xj,yj,0.)
    jupiter.trail.append(pos=jupiter.pos)
    sun.pos= vec(xs, ys,0.)
    sun.trail.append(pos=sun.pos)


