# simulate wave motion
# based on Giordano and Nakanishi, "Computational Physics"
# Yongli Gao, 12/28/2005

from visual import *

nmax = 100 # number of spatial units
nsave = 2**10
c = 300. # speed of sound
dx = 0.01 # x step size
dt = dx / c # time step
r2 = (dt * c / dx)**2
Ai = 100 # initial hight of wave
x_gaussian = 10
x_sample = nmax / 5

# set up graphics
g = display(y = 30 + 200, width=600, height=170, title="Mechanical Wave")
wave = curve( x = arange(-nmax/2,nmax/2), display=g, color=color.red, radius = 0.5,
              t1=zeros((nmax,3),float), t0=zeros((nmax,3),float))
wave.color[x_sample] = color.green # color the sampling spot

# initial Gaussian pulse
for i in range(1,nmax-1):
    wave.t1[i,1] = 10. * exp(-1000. * (i * dx - x_gaussian * dx)**2)   
    wave.t0[i,1] = wave.t1[i,1]

"""
    if(i <= 50):
        wave.t1[i,1] = i*Ai*dx
    if(i > 50):
        wave.t1[i,1] = 50*Ai*dx- Ai*dx*(i-50)
    
    wave.t0[i,1] = wave.t1[i,1]
"""
# calculate and plot
def linWave(wave):
    wave.t1[0] = wave.t1[-1] = vector(0,0,0) # both ends fixed
    for i in range(1,nmax-1):
        wave.pos[i,1] = r2 * (wave.t1[i+1,1] + wave.t1[i-1,1])\
                        +2. * (1.0 - r2)\
                        * wave.t1[i,1] - wave.t0[i,1]

    wave.t0[:,1] = wave.t1[:,1]
    wave.t1[:,1] = wave.pos[:,1]

def wave_stiff_damp(nmax,wave):
    # add corrections of stiffness
    wave.t1[0] = vector(0,0,0) # fixed end
    wave.t1[-1] = vector(0,0,0) # fixed end
    
    c=300 #Speed of sound
    
    en = 1.e-9 * nmax * nmax
    #For Exagerated but visible Dampening
    b=40
    x=dx
    t=dt

    y = wave.t1[1,1] #Current y at 1
    ymn1 = wave.t0[1,1] # previous y at 1
    
    yi2 = wave.t1[1+2,1] # Current y at 1+2
    yi1 = wave.t1[1+1,1] #Current y at 1+1
    ymi1= wave.t1[1-1,1] # Current y at 1-1, 
    ymi2 = -wave.t1[1,1] # Current y at 1-2, which there is none at this bound so we take the inverse of the current

    #The Dampening Stiffness Equation
    value= -1/(1+b*t)*((6*en*r2+2*r2-2)*y - 4*en*r2*yi1-r2*yi1+en*r2*yi2-4*en*r2*ymi1-r2*ymi1+en*r2*ymi2+ymn1-b*t*ymn1)
    #print value
    
    wave.pos[1,1] = value

    """
    wave.pos[1,1] =(2. - 2. * r2  - 6. * r2 * en) * wave.t1[1,1] - wave.t0[1,1] + \
              r2 * (1. + 4. * en) * (wave.t1[2,1] + wave.t1[0,1]) - r2 * en * \
              (wave.t1[3,1] - wave.t1[1,1])

    """
    
    for i in range(2,nmax-2):
       
        y = wave.t1[i,1] #Current y at i
        yi2 = wave.t1[i+2,1] # Current y at i+2
        yi1 = wave.t1[i+1,1] #Current y at i+1
        ymi1= wave.t1[i-1,1] # Current y at i-1
        ymi2 = wave.t1[i-2,1] # Current y at i-2

        ymn1 = wave.t0[i,1] # previous y at i
        
        
        #The Dampening Stiffness Equation 
        wave.pos[i,1] = -1/(1+b*t)*((6*en*r2+2*r2-2)*y - 4*en*r2*yi1-r2*yi1+en*r2*yi2-4*en*r2*ymi1-r2*ymi1+en*r2*ymi2+ymn1-b*t*ymn1)
       
        
        """
        wave.pos[i,1] = (2. - 2. * r2  - 6. * r2 * en) * wave.t1[i,1] - wave.t0[i,1] + \
                        r2 * (1. + 4. * en) * (wave.t1[i+1,1] + wave.t1[i-1,1]) - r2 * \
                        en * (wave.t1[i+2,1] + wave.t1[i-2,1])
                        """
                        
    n = nmax - 2

    y = wave.t1[n,1]    #Current y at n
    ymn1 = wave.t0[n,1] # previous y at n
    
    yi2 = -wave.t1[n,1] # Current y at n+2, which there is none at this bound so we take the inverse of the current
    yi1 = wave.t1[n+1,1] #Current y at n+1
    ymi1= wave.t1[n-1,1] # Current y at n-1, 
    ymi2 = wave.t1[n-2,1] # Current y at n-2,

    
    wave.pos[n,1] = -1/(1+b*t)*((6*en*r2+2*r2-2)*y - 4*en*r2*yi1-r2*yi1+en*r2*yi2-4*en*r2*ymi1-r2*ymi1+en*r2*ymi2+ymn1-b*t*ymn1)
    """wave.pos[n,1] = (2. - 2. * r2  - 6. * r2 * en) * wave.t1[n,1] - wave.t0[n,1] + \
              r2 * (1. + 4. * en) * (wave.t1[n+1,1] + wave.t1[n-1,1]) - r2 * en * \
              (-wave.t1[n,1] + wave.t1[n-2,1])
"""
    wave.t0[:,1] = wave.t1[:,1]
    wave.t1[:,1] = wave.pos[:,1]

    print wave.pos[x_sample,1]




#Storing the amplitude of the x_sample spot
store_amp= [0.]*nsave
for i in range(nsave+10):
    rate(50)
    #linWave(wave)
    wave_stiff_damp(nmax,wave)
    if i < nsave:
        store_amp[i]= wave.pos[x_sample,1]
    


from visual.graph import *
#from numarray.fft import *
from numpy.fft import *

window_w = 600
window_h = 400
plot_max = float(raw_input("Maximum frequencey to plot (Hz) -> "))
power = gdisplay(width=window_w, height=window_h,\
                     title='Compare two FFT', xmax = plot_max,\
                     xtitle='Frequency (Hz)', ytitle='Power')
g_power = gcurve()

# open file in text format. The first line is the number of points,
# second step size, then data points each a single line.

npoint = nsave
dt = dt
f = array(npoint*[0.])
y = array(npoint*[0.])
ndt = npoint * dt
   
for i in range(npoint):
    y[i] = store_amp[i]
    #print i,y[i]
    f[i] = i / ndt
    
y_fft = fft(y) # FFT

# plot the fft result
g_power.color = (1,1,1)
for i in range(npoint/2):
    g_power.plot(pos=(f[i],(y_fft[i].real**2+y_fft[i].imag**2)))
    #print (f[i],y_fft[i].real**2+y_fft[i].imag**2)


