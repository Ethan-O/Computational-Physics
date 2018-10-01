# simulation of diffusion limited aggrregation
# Yongli Gao  12/29/2005
# modified the display to put the cluster at center
# Yongli Gao 3/26/2012

from visual import *
from visual.graph import *
from random import *

npoint = 70 # size of the surface
r0 = 5.
point = resize(array([0]),(npoint,npoint))

def sign(val):
    if val > 0: return 1
    else: return -1

rmax = 0
r0 = 10
p = npoint/2
q = npoint/2
seed() # initial a random number.
point[p,q] = 1
step = [0,0]
board = min(min(p,npoint-p),min(q,npoint-q)) # the shortest from the seed to the wall

DLA = display(width=400, height=400, range=(npoint,npoint,npoint), center=(p,q,0), title="DLA Growth")
particle = box(color=color.yellow)

while r0<board-1:
# generate a particle randomly along the x axis
# This makes the cluster fairly straight, like a bone
# It is also has less volume and fewer holes
    r = r0 * 2  # particles appear from -r to r on the axis
    rmax = r0 * 3  # limit of moving area
    rx = 2*(random()-0.5)*r
    
    x = rx + p
    y = p
    n = 1
    #print "inital",x,y
# random walk until hit a sticky site
    while n>0:
        rate(10000)
        distr = abs(x - p) + abs(y - q)
        if distr>rmax: # discard if too far away
            n = 0
        if (x>0 and x<npoint-2) and (y>0 and y<npoint-2):# see if it can stick
            if point[x,y-1]==1 or point[x,y+1]==1 or point[x-1,y]==1 or point[x+1,y]==1:
                point[x,y] = 1
                box(pos=(x,y,0))
                #print "growth",x,y
                if distr>r0:
                    r0 = distr
                n = 0
        step[0] = 0
        step[1] = 0
        step[int(2*random())] = sign(random()-0.5)
        x = x + step[0]
        y = y + step[1]
        particle.pos = (x,y,0)

