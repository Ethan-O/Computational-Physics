# Planetary motion with the Euler-Cromer method
# based on Giordano and Nakanishi, "Computational Physics"
# Yongli Gao,  2/11/2006
#
# Add a plot for the Earth as the Vpython zooming has failed.
# Yongli Gao,  2/15/2017

from vpython import *

# possible values x=1, y=0, v_x=0, v_y=2pi, dt=0.002, beta=2
print ("two planet motion")

xe = 1.
ye = 0.
ve_x = 0.
ve_y = 6.28
xj = 0.
yj = 5.2
vj_x = - 2. * pi / sqrt(yj)
vj_y = 0.
dt = 0.002

# me/ms = 3.e-6, mj/ms = 9.5e-4
# me = float(raw_input("earth mass (in solar mass) -> "))
# mj = float(raw_input("jupiter mass (in solar mass) -> "))
# to visualize procession, try ve_y = 5., mj = 9.5e-2

me = 3.0e-6
mj = 9.5e-4

# plot 
window_w = 400
scene1 = display(width=window_w, height=window_w)
earth = sphere(radius=0.1, color=color.green)
earth.trail = curve(color=color.cyan)
jupiter = sphere(radius=0.1, color=color.yellow)
jupiter.trail = curve(color=color.cyan)
sun = sphere(pos=vec(0.,0.,0.), radius = 0.2, color=vec(1,1,1))

# plot earth only
scene2 = display(x=window_w,width=window_w, height=window_w)
earth2 = sphere(radius=0.02, color=color.green)
earth2.trail = curve(color=color.cyan)
sun2 = sphere(pos=vec(0.,0.,0.), radius = 0.1, color=vec(1,1,1))

# x,y = position of planet
# v_x,v_y = velocity of planet
# dt = time step
while 1: # use Euler-Cromer method
    rate(100)
    re = sqrt(xe**2 + ye**2)
    rj = sqrt(xj**2 + yj**2)
    rej = sqrt((xe - xj)**2 + (ye - yj)**2)
    ve_x = ve_x - 4 * pi**2 * dt * (xe / re**3 + mj * (xe - xj) / rej**3)
    ve_y = ve_y - 4 * pi**2 * dt * (ye / re**3 + mj * (ye - yj) / rej**3)
    vj_x = vj_x - 4 * pi**2 * dt * (xj / rj**3 + me * (xj - xe) / rej**3)
    vj_y = vj_y - 4 * pi**2 * dt * (yj / rj**3 + me * (yj - ye) / rej**3)
    xe = xe + ve_x * dt
    ye = ye + ve_y * dt
    xj = xj + vj_x * dt
    yj = yj + vj_y * dt
    earth.pos = vec(xe,ye,0.)
    earth.trail.append(pos=earth.pos)
    earth2.pos = vec(xe,ye,0.)
    earth2.trail.append(pos=earth.pos)
    jupiter.pos = vec(xj,yj,0.)
    jupiter.trail.append(pos=jupiter.pos) 




