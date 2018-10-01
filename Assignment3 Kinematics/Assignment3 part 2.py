# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 14:59:59 2018

@author: Ethan Otto
"""

#Assignment 3 Python 3
# 2.14

import numpy as np

import matplotlib.pyplot
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D


#Initializing the velocity
def init_v(mag,theta,phi):
    #Tranforming from spherical cordinates to cartesian coordinates
    x= mag*np.sin(np.deg2rad(phi))*np.cos(np.deg2rad(theta))
    y= mag*np.sin(np.deg2rad(phi))*np.sin(np.deg2rad(theta))
    z= mag*np.cos(np.deg2rad(phi))
    
    return np.array([x,y,z])

#Calculates an orthogonal vector to vector <x,y> 
def calc_perp(x,y):
    
    if(x ==0):
        return np.array([1,0])
    if(y==0):
        return np.array([0,1])
        

    # <x, y> . <a,b> = x*a +y*b == 0 if Orthogonal
    # For direction vector a^2 + b^2 =1,b = sqrt(1-a^2)
    #Substitute vx*a+vy*sqrt(1-a^2) ==0
    #Solve for a: a = -+ y/sqrt(x^2+y^2)
    #Solve for b: b = -+ x/sqrt(x^2+y^2)

    a = y/np.sqrt(y**2+x**2)
    #a*x must have the opposite sign of y*b
    sign = a*x/abs(a*x)
    b = -1*sign* x/np.sqrt(x**2+y**2)
    
    return np.array([a,b])
    
calc_perp(1,5)
    
def calc(vi):
    
    delta_t = 0.1
    max_time = 10000
    B2_m = 4*10**(-5)
    g= 9.8
    size = int(max_time/delta_t)
    
    #Initializing arrays
    t = np.zeros(size)
    point = np.zeros((size,3))
    vel = np.zeros((size,3))
    
    # Magnitudes of wind speed
    w_mag = 10
    # initial Velocities by axis component (x,y is ground plan, z is altitude)
    vel[0][0] = vi[0]
    vel[0][1] = vi[1]
    vel[0][2] = vi[2]
    
    vi_x = vi[0]
    vi_y = vi[1]
    vi_z = vi[2]
    
    # Axis wise windspeed
    # We need it to be parrellel to ground and orthogonal to v_i
    # So we need a direction vector perpendicular to the v_i vx vy vector
    perp = calc_perp(vi_x, vi_y) 
    # Directions Vectors for w
    u_x = perp[0]/np.sqrt(perp[0]**2+perp[1]**2)
    u_y = perp[1]/np.sqrt(perp[0]**2+perp[1]**2)
    
    # wind speed components
    wx= u_x*w_mag
    wy= u_y*w_mag    
    w = np.array([wx,wy,0])
    
    # want to stop when we hit the end of our time array
    for i in range(size-1):
        
        x = point[i][0]
        y = point[i][1]
        z = point[i][2]
        
        vx = vel[i][0]
        vy = vel[i][1]
        vz = vel[i][2]

        # Calculate the Acceleration Components
        #np.linalg.norm finds the vector magnetude
        Fdx = -B2_m*np.linalg.norm(vel[i] - w)*(vx-wx)
        Fdy = -B2_m*np.linalg.norm(vel[i] - w)*(vy-wy)
        # There is no vertical wind
        Fdz = -B2_m*np.linalg.norm(vel[i] - w)*(vz)
        
        #Steping the position and velocity
        x_i1 = x + vx*delta_t
        y_i1 = y + vy*delta_t
        z_i1 = z + vz*delta_t
        vx_i1 = vx + Fdx*delta_t
        vy_i1 = vy + (Fdy)*delta_t
        vz_i1 = vz + (-g + Fdz)*delta_t
        # Adding the new steps into their repective arrays
        point[i+1] = np.array([[x_i1,y_i1,z_i1]])
        vel[i+1] = np.array([[vx_i1,vy_i1,vz_i1]])
        t[i+1]= (t[i]+delta_t)
        # checking if projectile has hit the ground
        if z_i1 < 0:
            point = np.copy(point[:i+1])
            # Return the points and convert m to km
            return point

def main(mag,ang, phi):
    #ang is angle in the x y plane
    #phi is angle between vertical and horizontal, so phi = 0 is all z+, phi= 90 is all x, y velocity
    
    vi = init_v(mag,ang,phi)
    
    return calc(vi)



#Generating trajectories
p1 = main(1000,0,30)
p2 = main(1000,0,45)

p3 = main(1000,0,0)

p4 = main(1000,0,45)
p5 = main(1000,30,45)
p6 = main(1000,60,45)

#Ploting settings
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#Labels
ax.set_title("Shell trajectory with wind speed of 10m/s, varying phi")
ax.set_xlabel("X Axis (m)")
ax.set_ylabel("Y Axis (m)")
ax.set_zlabel("Z Axis (m)")

ax.plot(xs=p1[:,0], ys=p1[:,1],zs=p1[:,2],c='g', label="phi = 30")
ax.plot(p2[:,0], p2[:,1],zs=p2[:,2],c= 'b', label= "phi=45")

ax.legend(loc="center left")
#Clearly the wind speed is causing the ball to develop a velocity orthogonal it its origional

#Comparing different theta same phi
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_title("Shell trajectory with wind speed of 10m/s, varying theta")
ax.set_xlabel("X Axis (m)")
ax.set_ylabel("Y Axis (m)")
ax.set_zlabel("Z Axis (m)")
# With no initial velocity in x y plane, it defaults to wind in the y direction
ax.plot(p4[:,0], p4[:,1],zs=p4[:,2],c= 'g', label= "theta = 0")
ax.plot(p5[:,0], p5[:,1],zs=p5[:,2],c= 'b', label= "theta = 30")
ax.plot(p6[:,0], p6[:,1],zs=p6[:,2],c= 'r', label= "theta = 60")
ax.legend(loc="center left")


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_title("Shell trajectory with wind speed of 10m/s and ball is thrown straight up")
ax.set_xlabel("X Axis (m)")
ax.set_ylabel("Y Axis (m)")
ax.set_zlabel("Z Axis (m)")
# With no initial velocity in x y plane, it defaults to wind in the y direction
ax.plot(p3[:,0], p3[:,1],zs=p3[:,2],c= 'r', label= "phi = 0")

ax.legend(loc="center left")


plt.show()

