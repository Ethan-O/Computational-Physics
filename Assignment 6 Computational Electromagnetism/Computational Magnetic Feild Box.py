
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from numpy import * 

#size of length of the box that contains the plot
Lsize = 20

v = resize(array([0.]),(20,20,20))
voltage = 10

#High Potential Rod (lighting)
v[8:13,8:13,5:21] = voltage

#Ground
v[:,:,0] = 0

#copy this initial guess for V field
v2 = copy(v)


#Return True if the point is in an object (Rod or Plane)
def in_object(i,j,k):
   return k == 0 or (8<= i <=12 and  8<= j <=12 and  5<= k <=20)

#Update the Jacobi Relaxation
def  update(v1,v2,vsize):
    diff=0
    for i in range(1,vsize-1):
        for j in range(1,vsize-1):
            for k in range(1,vsize-1):
                if in_object(i,j,k):
                    continue
                
                v2[i,j,k] = (v1[i+1,j,k]+v1[i-1,j,k]+v1[i,j+1,k]+v1[i,j-1,k]\
                +v1[i,j,k+1]+v1[i,j,k-1])/6
                diff = diff + abs(v1[i,j,k] - v2[i,j,k])
    diff = diff / vsize**3
    return diff
#Calculate the electric feild given potential feild
def calcE(v,vsize):
    ex= resize(array([0.]),(20,20,20))
    ey= resize(array([0.]), (20,20,20))
    ez= resize(array([0.]), (20,20,20))
    #Only calculating the space two points in, to avoid boundary problems
    for i in range(2,vsize-2):
        for j in range(2,vsize-2):
            for k in range(2, vsize-2):
                ex[i,j,k] = -(v[i+1,j,k]-v[i-1,j,k])/2.0
                ey[i,j,k] = -(v[i,j+1,k]-v[i,j-1,k])/2.0
                ez[i,j,k] = -(v[i,j,k+1]-v[i,j,k-1])/2.0
                
    
    return ex,ey,ez

diff = 0
#diff goes to zero for my operating system on this range
for i in range(1,1000):
    diff = update(v,v2,Lsize)
    diff = update(v2,v,Lsize)


ex, ey, ez = calcE(v2,Lsize)



#Plotting
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
#X,Y,Z coords for 3d plot
y,x, z = meshgrid(arange(1, 21, 1),
                      arange(1, 21, 1),
                      arange(1, 21, 1))
#Slicing the data (we can't use all 20^3 values)
secx = slice(0,Lsize,2)
secy = slice(0,Lsize,2)
secz = slice(0,Lsize,2)


#The vector plot
ax.quiver(x[secx,secy,secz], y[secx,secy,secz], z[secx,secy,secz], ex[secx,secy,secz], ey[secx,secy,secz], ez[secx,secy,secz], length=0.9)


#The Zero potential plane
x,y = meshgrid(range(1,21), range(1,21))
#setting z = 1 for each x,y
z=x*0+1
ax.plot_surface(x,y,z,alpha=0.9)

#The Lighting(Potential Rectangle) outline
x =repeat(9,21-4)
y =repeat(13,21-4)
z =range(4,21)
ax.plot(x,y,z, color="green")

x =repeat(13,21-4)
y =repeat(13,21-4)
z =range(4,21)
ax.plot(x,y,z, color="green")

x =repeat(13,21-4)
y =repeat(9,21-4)
z =range(4,21)
ax.plot(x,y,z, color="green")

x =repeat(9,21-4)
y =repeat(9,21-4)
z =range(4,21)
ax.plot(x,y,z, color="green")
plt.show()
