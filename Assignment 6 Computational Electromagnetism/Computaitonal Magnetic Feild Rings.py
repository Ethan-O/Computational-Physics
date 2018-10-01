
# compute the magnetic field from a circular current loop
# Program to accompany "Computational Physics" by N. Giordano
# Copyright Prentice Hall 1997
# Yongli Gao,  1/1/2006
#
# modified to have simpler scaling of graphics
# Yongli Gao, 3/6/2012
#

from visual import *
from numpy import *

def calculate_field(ring1,ring2,lmax,x,y,z,real = False): # calculate magnetic field at x,y,z for a loop of size ring
    dtheta = 2. * pi / 50. # step size for integration along theta
    bx = 0.
    by = 0.
    bz = 0.

    #Delta B = u0*I/(4*Pi)*dr*dL/L^3
    #Assuming the current is 1 and coordinates are in meters
    I  = 1 # Amps
    u0 = 4*pi*10**(-7) # H/m

    #constant for calculating B
    c = I*u0/(4*pi)
    
    #If we want unrealistic but easily visable values
    if real == False:
        c = 1
    
    #Ring z values
    ring1z = 0
    ring2z = ring1
    for theta in arange(0.,2.*pi, dtheta):
        #First loop vectors
        dl1x = -ring * dtheta * sin(theta) # components of dr
        dl1y = ring * dtheta * cos(theta)
        r1x = x - ring * cos(theta) # components of r
        r1y = y - ring * sin(theta)
        r1z = z - ring1z
        
        #Second Loop vectors
        dl2x = -ring * dtheta * sin(theta) # components of dr
        dl2y = ring * dtheta * cos(theta)
        r2x = x - ring * cos(theta) # components of r
        r2y = y - ring * sin(theta)
        r2z = z - ring2z
        
        
        r1 = sqrt(r1x**2 + r1y**2 + r1z**2)
        r2 = sqrt(r2x**2 + r2y**2 + r2z**2)
        
        #Additional Feild from first loop
        if r1 > 2. / lmax: # avoid the wire itself
            bx+= c*dl1y * r1z / r1**3  # Biot-Savart law (cross product)
            by+= -c*dl1x * r1z / r1**3
            bz+= c*(dl1x * r1y - dl1y * r1x) / r1**3
            
        #Additional Feild from second loop
        if r2 > 2./ lmax: # avoid the second wire
            bx+= c*dl2y * r2z / r2**3  
            by+= -c*dl2x * r2z / r2**3
            bz+= c*(dl2x * r2y - dl2y * r2x) / r2**3
    #print x,y,z,bx,by,bz
    return (bx,by,bz)

ring = 0.5 # radius of circular current loop
lmax = 40 # size of the grid in -1<x<1, y=0, -1<z<1
factor = 200 # factor to reduce the size of field vector arrows

# set up graphics
window_w = 800
window_h = 800

g = display(x=0, y=0, width=window_w, height=window_h,
                    title='Magnetic Field',
                    xtitle='r', ytitle='B')

# plot the loop
nloop = 50
dtheta = 2. * pi / (nloop-1)
loop1 = curve(z = nloop*[0.], color=color.red, radius = 1./lmax)
loop2 = curve(z = nloop*[.5], color=color.blue, radius = 1./lmax)
for i in range(nloop): # set the x,y atributes for the curve object loop
    theta = i * dtheta
    loop1.x[i] = ring * cos(theta) # components of r
    loop1.y[i] = ring * sin(theta)
    loop2.x[i] = ring * cos(theta)
    loop2.y[i] = ring * sin(theta)
 
for i in range(-lmax,lmax): # compute and plot field in x-z plane
    for j in range(-lmax,lmax):
        xij = float(i)/lmax
        zij = float(j)/lmax
        field = array(calculate_field(ring,ring,lmax,xij,0.,zij))/factor
        vfield = arrow(pos=(xij,0,zij),axis=field,color=color.green)

#Calculating B Field along the z axis from -1 to 1
Bz = 2*lmax*[0.]
j= 0
for i in range(-lmax,lmax): # compute and plot field in x-z plane
    zi = float(i)/lmax
    #B vector along each axis
    bx,by,bz = calculate_field(ring,ring,lmax,0,0,zi,real=True)
    #Magnetude of B
    Bz[j] = sqrt(bz**2+bx**2+by**2)
    j+= 1

#Analytical Solution, Super position of two rings
Az = 2*lmax*[0.]
j=0
for i in range(-lmax,lmax):
    zi = float(i)/lmax
    I  = 1 # Amps
    u0 = 4*pi*10**(-7) # H/m
    Az[j] = u0*I*0.5**2 /2*(1/(.5**2+zi**2)**(3/2)+1/(0.5**2+(zi+0.5)**2)**(3/2))
    j+= 1

print "The Numerical Approximation of B, its off by a factor of 4"
print Bz
print "The Analytical Solution of B"
print Az
