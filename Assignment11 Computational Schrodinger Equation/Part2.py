# Time dependent quantum mechanics with leap frog method
# Program to accompany "Computational Physics" by N. Giordano and H. Nakanishi
# Copyright Prentice Hall 1997, 2006
# m=1/2 here to be consistent with other programs here H. Nakanishi
# Modified for VPython
# Yongli Gao,  2/11/2006
#
# Vectorized operation
# Yongli Gao, 4/8/2017

from numpy import *
# initialize wavefunction
# r[) and iold() are assigned the real and imaginary parts 
# of a gaussian wavefunction at the initial time.  i() is
# assigned the imaginary part of the wavefunction a halfstep 
# in time later.
# prob() and phase() are assigned values for the initial time.
#
# The initial position, sigma and central wavenumber for the 
# gaussian at t = 0.
#
def initwfunc(dt,dx,v,r,i,iold,jmax,x_0,s_0,k_0):
    sum1 = 0.
    sigmasq = 4*s_0*s_0
    for j in range(1,jmax-1): # real and imaginary psi(t=0) 
        x = j*dx
        r[j] = cos(k_0*x)*exp(-(x-x_0)**2/sigmasq)
        iold[j] = sin(k_0*x)*exp(-(x-x_0)**2/sigmasq)
        sum1 = sum1+r[j]**2+iold[j]**2
    sum1 = sqrt(sum1*dx)
    for j in range(1,jmax-1): # normalization
        r[j] = r[j]/sum1
        iold[j] = iold[j]/sum1
    # fixed boundary ~ infinit potential well
    r[0] = 0.0
    r[jmax-1] = 0.0
    iold[0] = 0.0
    iold[jmax-1] = 0.0
    # Initial halfstep for I
    s = dt/(2*dx*dx)
    for j in range(1,jmax-1):
        i[j] = iold[j]+0.5*(s*(r[j+1]-2*r[j]+r[j-1])-v[j]*r[j]*dt)
    i[0] = 0.0
    i[jmax-1] = 0.0
    return

# Assumes box quantization.  r() and i() are fixed at the walls.   
# iold() holds the imaginary part of the wavefunction at the 
# previous timestep.  It is needed to compute the prob() and 
# phase() distributions. 
def timestep(dt,dx,v,r,i,iold,jmax):
    s = dt/(2.*dx*dx)
    for j in range(1,jmax-1):
        r[j] = r[j]-s*(i[j+1]-2*i[j]+i[j-1])+v[j]*i[j]*dt
        iold[j] = i[j]
    for j in range(1,jmax-1): # Can we combine this loop with the one above?
        i[j] = i[j]+s*(r[j+1]-2*r[j]+r[j-1])-v[j]*r[j]*dt
    return


#vectorized timestep, unsuccessful attempt
def timestep_vec(dt,dx,v,r,i,iold,jmax):
    dx2 = (2.*dx*dx)
    iold = i.copy()
    r[1:-1] -= dt*((i[2:]-2*i[1:-1]+i[:-2])/dx2-v[1:-1]*i[1:-1])
    i[1:-1] += dt*((r[2:]-2*r[1:-1]+r[:-2])/dx2-v[1:-1]*r[1:-1])
    return

#vectorized timestep, one thing at a time
def timestep_v1(dx,v,w):

    return (w[2:]-2*w[1:-1]+w[:-2])/(2.*dx*dx)-v[1:-1]*w[1:-1]

# initialize parameters. Try a=0.7,w=0.1,v_0=1e6,d=1e5,
# x_0=0.4,s_0=0.02,jmax=500,dt=1e-7,intval=10
#print "1D scattering in (-L,L) ..."
#a = float(raw_input("square well/barrier at (aL): a => "))
#w = float(raw_input("square well/barrier width (wL): w => "))
#v_0 = float(raw_input("V_0 (in units of hbar**2/2mL**2) => "))
#d = float(raw_input("incident energy (in units of hbar**2/2mL**2) => "))
#x_0 = float(raw_input("initial wave packet location (in units of +-L) => "))
#s_0 = float(raw_input("incident Gaussian half width (in units of L) => "))
#jmax = int(raw_input("split into jmax intervals; jmax => "))
#dt = float(raw_input("dt (in units of 2mL**2/hbar) => "))
#intval = float(raw_input("plot at interval of this many time steps  => "))
a,w,v_0,d,x_0,s_0,jmax,dt,intval=0.5,.05,40.e3,1.e5,0.4,0.02,500,1e-7,10

#Barrior width tested 0.05, 0.1, .25, .5

k_0 = sqrt(d)
dx = 1./jmax
v = array(jmax*[0.])
r = array(jmax*[0.])
i = array(jmax*[0.])
iold = array(jmax*[0.])

# set up potential for barrior
start = int(a/dx)
end = start + int(w/dx)
for j in range(start,end):
    v[j] = v_0
# initialize wavefunction
initwfunc(dt,dx,v,r,i,iold,jmax,x_0,s_0,k_0)

# set up plot

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots(figsize=(5, 3))
ax.set(xlim=(0, 1), ylim=(0, 20))

xrange = arange(0,1,dx)
#The curves
prob_curve = ax.plot(xrange,[0]*len(xrange),label="Probability")[0]
r_curve = ax.plot(xrange,r,label="Real")[0]
i_curve = ax.plot(xrange,i,label="Imaginary")[0]

#lines for barrior
ax.vlines(ymin=0,ymax=20, x=a,linestyles='dashed',label="Potential Barrior")
ax.vlines(ymin=0,ymax=20, x=(a+w),linestyles='dashed')
#Legend for the plot
ax.legend(loc=2,prop={'size': 7})
def update_curves(n):
   
    global i
    global r
    
    global prob_curve
    global r_curve
    global i_curve
    #Run for 100 interations then show visual update
    inter =0
    while inter <100:
        #timestep(dt,dx,v,r,i,iold,jmax)
        #timestep_vec(dt,dx,v,r,i,iold,jmax)
        iold=i.copy()
        r[1:-1] -= dt*timestep_v1(dx,v,i)
        i[1:-1] += dt*timestep_v1(dx,v,r)
        inter +=1

    prob = (r*r+i*iold).tolist()
    
    prob_curve.set_ydata(prob)
    r_curve.set_ydata((r+5.))
    i_curve.set_ydata((i+8.))
        
        #print(r)
        #print("Change " + str(n) + " Mean" + str(mean(r)))
        
#Function that controls the animation
anim = FuncAnimation(fig,update_curves,interval=1,frames=100)
plt.draw()
plt.show()

#Summary of wave behavor in in repsponse to varing potential barriors

#Case Narrow Width
#a= 0.7 w =.01, v=1/2*E

#Case Large Width
#a= 0.7 w =.3, v=1/2*E
#As the width increases it seems that less of the wave enters, and the wave diminishes faster in
#The high potential region

#Case Edge barrior
#a=0.9, w=0.05, v=1/2E

#Case Middle barrior
#a =0.5, w=0.05, v=1/2*E

#After the tranmission the wave in the after barrior region becomes very large for the edge barrior
#And is calm after transmissions

#In the middle case the after barrior region's wave is smaller and more steady

#Case High Potential 
#a=0.7, w=0.1, v= 1.01*E

#Case low Potential 
#a=0.7, w=0.1, v= 1/4*E

#High case: Only a little peice of the wave function makes it past the entry of the barrior
#Low case: About half of the wave passes through
