# simulation of percolation
# Yongli Gao  12/29/2005

from visual import *
from visual.graph import *
from random import *

npoint = 15 # size of the surface
# threshold 0.32
#prob = float(raw_input("Enter occupation probability (0-1)"))

#By adding an extra dimension we are adding more sides that could connect to each individual point, increasing the chance of a connection
#So we would epect the perculation probability to go down
prob = 0.4
point = resize(array([0]),(npoint,npoint,npoint))

dis1 = display(x=600, width=400, height=400, xmin=0,xmax=npoint, ymin=0,
               ymax=npoint, center=(npoint/2,npoint/2,0), title="Percolation")
# set up a random array
for i in range(1,npoint-1):
    rate(100)
    for j in range(1,npoint-1):
        for k in range(1, npoint-1):
            if random()<prob:
                point[i,j,k] = 1
                box(pos=(i,j,k))

#raw_input("Hit return to see percolation")
ilabel = 1 # index of the cluster
for i in range(1,npoint-1):
    for j in range(1,npoint-1):
        for k in range(1,npoint-1):
            if point[i,j,k] == 1:
                #Bridge between three clusters, find out if they differ
                if point[i-1,j,k]>0 and point[i,j-1,k]>0 and point[i,j,k-1]>0:
                    pointa = point[i-1,j,k]
                    pointb = point[i,j-1,k]
                    pointc = point[i,j,k-1]
                    point[i,j,k] = pointa
                    if pointa!=pointb:  # a bridge between two clusters.  make them as one.
                         for m in range(1,i+1):
                             for n in arange(1,npoint-1):
                                 for p in arange(1,npoint-1):
                                     if point[m,n,p]==pointb:
                                         point[m,n,p] = pointa
                    if pointa!=pointc:
                        for m in range(1,i+1):
                             for n in arange(1,npoint-1):
                                 for p in arange(1,npoint-1):
                                     if point[m,n,p]==pointc:
                                         point[m,n,p] = pointa

                
                elif point[i-1,j,k]>0 and point[i,j-1,k]>0:
                    pointa = point[i-1,j,k]
                    pointb = point[i,j-1,k]
                    point[i,j,k] = pointa
                    if pointa!=pointb:  # a bridge between two clusters.  make them as one.
                         for m in range(1,i+1):
                             for n in arange(1,npoint-1):
                                 for p in arange(1,npoint-1):
                                     if point[m,n,p]==pointb:
                                         point[m,n,p] = pointa

                elif point[i,j-1,k]>0 and point[i,j,k-1]>0:
                    pointa = point[i,j-1,k]
                    pointb = point[i,j,k-1]
                    point[i,j,k] = pointa
                    if pointa!=pointb:  # a bridge between two clusters.  make them as one.
                         for m in range(1,i+1):
                             for n in arange(1,npoint-1):
                                 for p in arange(1,npoint-1):
                                     if point[m,n,p]==pointb:
                                         point[m,n,p] = pointa
                                     
                elif point[i-1,j,k]>0 and point[i,j,k-1]>0:
                    pointa = point[i-1,j,k]
                    pointb = point[i,j,k-1]
                    point[i,j,k] = pointa
                    if pointa!=pointb:  # a bridge between two clusters.  make them as one.
                         for m in range(1,i+1):
                             for n in arange(1,npoint-1):
                                 for p in arange(1,npoint-1):
                                     if point[m,n,p]==pointb:
                                         point[m,n,p] = pointa

                
                elif point[i-1,j,k]>0:
                    point[i,j,k] = point[i-1,j,k]
                elif point[i,j-1,k]>0:
                    point[i,j,k] = point[i,j-1,k]
                elif point[i,j,k-1]>0:
                    point[i,j,k] = point[i,j,k-1]
                else:
                    ilabel = ilabel + 1
                    point[i,j,k] = ilabel
                   
# plot if any of the clusters percolates
colors = [(1,1,1),(0,0,1),(0,1,0),(1,0,0),(0,1,1),(1,1,0),(.5,.5,.5),(1,0,1),(.5,1,1),(1,.5,1)] # set up 6 colors
icolor = 0

for i in range(1,ilabel+1):
    iperco = zeros((6),int) # array to record if a cluster connects at least two sides
    for j in range(1,npoint-1):
        for k in range(1,npoint-1):
            #One check for a maching index along each side
            if point[1,j,k]==i: iperco[0] = 1
            if point[npoint-2,j,k]==i: iperco[1] = 1
            if point[j,1,k]==i: iperco[2] = 1
            if point[j,npoint-2,k]==i: iperco[3] = 1
            if point[j,k,1]==i: iperco[4] = 1
            if point[j,k,npoint-2] ==i: iperco[5] =1
            
    if iperco[0]+iperco[1]+iperco[2]+iperco[3]+iperco[4]+iperco[5]>=3:
        #print i, iperco
        icolor = icolor + 1
        for k in range(1,npoint-1):
            for j in range(1,npoint-1):
                for v in range(1,npoint-1):
                    if point[k,j,v]==i:
                        box(pos=(k,j,v),color=colors[icolor%6])
    
 
