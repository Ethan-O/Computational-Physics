#Assignment 3 Python 3
"""
Created on Fri Feb  2 12:14:22 2018

@author: Ethan Otto
"""

# 2.9

import numpy as np
import matplotlib.pyplot as plt


#Initalizing simple model arrays
def init_simple(mag,ang, point,vel,t):
    
    vel[0] = np.array([mag*np.sin(np.deg2rad(ang)),mag*np.cos(np.deg2rad(ang))])
    
#Initalizing atmosphere recongnizing model arrays
def init_atmosphere(mag,ang,point,vel, t):
    
    vel[0] = np.array([mag*np.sin(np.deg2rad(ang)),mag*np.cos(np.deg2rad(ang))])

#Calculating Flight Path of simple model
def calc_simple(point,vel,t, delta_t, size):
    #Intializing constants
    B2_m = 4*10**(-5)
    g= 9.8

    #Incrementing by discrete units of time
    for i in range(size):
        #setting component positions
        x = point[i][0]
        y = point[i][1]
        #setting component velocities
        vx = vel[i][0]
        vy = vel[i][1]
        # Drag Force calculations
        Fdx = -B2_m*vx*np.sqrt(vx**2+vy**2)
        Fdy = -B2_m*vy*np.sqrt(vx**2+vy**2)
        
        #Calculating i+1 index position and velocities
        x_i1 = x + vx*delta_t
        y_i1 = y + vy*delta_t
        vx_i1 = vx + Fdx*delta_t
        vy_i1 = vy + (-g + Fdy)*delta_t
        
        #Updating arrays with i+1 values
        point[i+1] = np.array([[x_i1,y_i1]])
        vel[i+1] = np.array([[vx_i1,vy_i1]])
        t[i+1]= (t[i]+delta_t)
        
        #Exit loop if projectile has hit the ground
        if y_i1 < 0:
            # Truncate the array to receive only values up till it hits the ground
            point = np.copy(point[:i+1])
        
            return point

def calc_atmosphere(point,vel,t, delta_t , size):
    #Initialize constants
    B2_m = 4*10**(-5)
    g= 9.8
    a=6.5*10**-3
    alpha=2.5
    
    #Incrementing in discrete units of time
    for i in range(size):
    
        x = point[i][0]
        y = point[i][1]
        
        vx = vel[i][0]
        vy = vel[i][1]
        
        #Calculating drag force
        Fdx = -B2_m*vx*np.sqrt(vx**2+vy**2)*(1-a*y/300)**alpha
        Fdy = -B2_m*vy*np.sqrt(vx**2+vy**2)*(1-a*y/300)**alpha
        #Calculating i+1 values
        x_i1 = x + vx*delta_t
        y_i1 = y + vy*delta_t
        vx_i1 = vx + Fdx*delta_t
        vy_i1 = vy + (-g + Fdy)*delta_t
        #Updating arrays with i+1 values
        point[i+1] = np.array([[x_i1,y_i1]])
        vel[i+1] = np.array([[vx_i1,vy_i1]])
        t[i+1]= (t[i]+delta_t)
    
        #Exit loop if projectile hits the ground
        if y_i1 < 0:
             # Truncate the array to receive get values up till it hits the ground
            point = np.copy(point[:i+1])
    
            return point

#Calculate a Flight path in the simple model using magnitude mag in m/s, and angle ang in Degrees
def main(mag,ang):
    #Intialize constants
    delta_t = 0.1
    max_time = 10000
    size = int(max_time/delta_t)
    #Intialize arrays
    t = np.zeros(size)
    point = np.zeros((size,2))
    vel = np.zeros((size,2))

    
    init_simple(mag,ang,point,vel,t)
    #divide calcultions by 1000 to convert from m to km
    return calc_simple(point,vel,t,delta_t, size)/1000

#Calculate a Flight path in the atmosphere model using magnitude mag in m/s, and angle ang in Degrees
def main_a(mag,ang):
    #Initialize constants
    delta_t = 0.1
    max_time = 10000
    size = int(max_time/delta_t)
    #Intialize arrays
    t = np.zeros(size)
    point = np.zeros((size,2))
    vel = np.zeros((size,2))
    
    init_atmosphere(mag,ang,point,vel,t)
     #divide calcultions by 1000 to convert from m to km
    return calc_atmosphere(point,vel,t, delta_t, size)/1000

#Calculating Flight paths
p1 = main(700,30)
p2 = main(700,45)
p3 = main(700,50)

p1a = main_a(700,30)
p2a = main_a(700,45)
p3a = main_a(700,50)

p4a = main_a(700,40)
p5a = main_a(700,45)
p6a = main_a(700,50)
p7a = main_a(700,55)



fig, (ax,ax2) = plt.subplots(2, sharex=True)
fig.subplots_adjust(hspace= .3)
ax.set_title("Shell trajectory without and with atmosphere density correction")
ax.set_xlabel("Horizonal Distance (km)")
ax.set_ylabel("Height (km)")

ax.plot(p1[:,0], p1[:,1],'b--', label = "30")
ax.plot(p2[:,0], p2[:,1],'g--', label= "45")
ax.plot(p3[:,0], p3[:,1], 'r--', label= "50")


ax.plot(p1a[:,0], p1a[:,1],'b' ,label = "30a")
ax.plot(p2a[:,0], p2a[:,1], 'g',label = "45a")
ax.plot(p3a[:,0],p3a[:,1],'r',label="50a")
ax.legend(loc="upper left")

#Stand alone air density correction graph

ax2.set_title("Shell trajectory with atmosphere density correction")
ax2.set_xlabel("Horizonal Distance (km)")
ax2.set_ylabel("Height (km)")

#Plotting Paths
ax2.plot(p4a[:,0], p4a[:,1],'b' ,label = "40a")
ax2.plot(p5a[:,0], p5a[:,1], 'g',label = "45a")
ax2.plot(p6a[:,0],p6a[:,1],'r',label="50a")
ax2.plot(p7a[:,0],p7a[:,1],'c',label="55a")

ax2.legend(loc="upper left")
#Adjusting margins plots, so there is no overlap
plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.5,
                    wspace=0.55)
plt.show()
print("Looks like the best angle for range is about 45 Degrees")
