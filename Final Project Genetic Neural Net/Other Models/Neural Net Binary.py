# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 00:28:04 2018

@author: ethan
"""

from numpy import * 
from random import *
import matplotlib.pyplot as plt
from matplotlib import colors
from sklearn import datasets

digits = datasets.load_digits()
images = digits['images']
images2 = [(im > 10)*2-1 for im in images]
target = digits['target']

zeros = digits['target']== 0
ones = digits['target'] == 1
both = [a or b for a,b in zip(zeros,ones)]

images3 = array(digits['images'])[both]
images3 = array([(im> 10)*2-1 for im in images3])

target3= array(digits['target'])[both]

A_image = array([[-1,-1,-1,-1,1,1,-1,-1,-1,-1],
           [-1,-1,-1,1,1,1,1,-1,-1,-1],
           [-1,-1,1,1,-1,-1,1,1,-1,-1],
           [-1,1,1,-1,-1,-1,-1,1,1,-1],
           [-1,1,1,1,1,1,1,1,1,-1],
           [1,1,1,1,1,1,1,1,1,1],
           [1,1,1,-1,-1,-1,-1,1,1,1],
           [1,1,-1,-1,-1,-1,-1,-1,1,1],
           [1,1,-1,-1,-1,-1,-1,-1,1,1],
           [1,1,-1,-1,-1,-1,-1,-1,1,1]])


def random_init(n):
    arr = array([0]*n**2)
    for i in range(len(arr)):
        #Will generate a 1 or -1 with 50% probability
        arr[i] = int(2*(random() // .5) -1)
    arr = arr.reshape((n,n))
    return arr

def random_mix(m,t):
    n = len(m[0])
    i = 0
    m = copy(m)
    while i < t:
    
        x = round(random()*(n-1))
        y = round(random()*(n-1))
        m[x,y] = m[x,y]*-1
        i+= 1
    return m
        
def basic_train(maps):
    n= len(maps[0][0])
    M = len(maps)
    J= array([0]*n*n*n*n)
    J = J.reshape((n*n,n*n))
    for m in maps:
        mf = m.flatten()
        for i in range(n*n):
            for xy in range(n*n):
                J[i,xy] += mf[xy]*mf[i]
               
    return 1/M*J
            
basic_train(list([A_image]))

def display(arr):

    cmap = colors.ListedColormap(['white','purple'])
    
    fig, ax= plt.subplots()
    ax.imshow(arr,cmap=cmap)
    

def calc_flip(lattice,J,i,j,n):
     #Parametric Boundary Conditions
    def correct_edge(x,n_max=n):
        if x < 0:
            x = n_max-1
        if x >= n_max-1:
            x = 0
        return x

    E=0
    # Aggregate spin of 6 nearest neighbors
    Sj = 0

    for a in range(n):
        for b in range(n):
            ab = a*n + b
            ij = i*n + j
            
            Sj+= J[ij,ab]*lattice[a,b]

    E = Sj*lattice[i,j]*2
    return E


def sweep(lattice,J,sweeps):
    n= shape(lattice)[0]
    lattice2 = copy(lattice)
    for s in range(sweeps):
    
        for i in range(n):
            for j in range(n):
                    #Calculating electrons change in E from spin flip at i,k,j
                    E_flip = calc_flip(lattice,J,i,j,n)
                    #If Energy is reduced, flip
                    if( E_flip < 0):
                        lattice2[i,j] = lattice[i,j]*-1

    return lattice2

def output(lattice,J):
    n = shape(lattice)[0]
    total = 0
    for a in range(n):
        for b in range(n):
            total += J[a,b]*lattice[a,b]
    total/(n*n)
    out = (sign(total)+1)/2
    return out

class mind:
    n=8
    J1 = array([0]*n**4).reshape(n*n,n*n)
    J2 = array([-1]*n**2).reshape(n,n)
    
    def mutate_first(self,times = 1):
        t = 0
        n= self.n
        while t < times:
            
            i = int(floor(random()*n*n))
            j = int(floor(random()*n*n))
        
            self.J1[i,j] = self.J1[i,j]+ round(random())*2 -1
            t += 1
        return
        
    def train_second(self,img):
        n = self.n
        for i in range(n):
            for j in range(n):
                self.J2[i,j] = img[i,j]
        return
                
    def  __init__(self):
        n = self.n
        
        self.mutate_first(50)
        
        self.train_second(images3[1])
        
    #def __init__(J1,J2):
    #    self.J1 = J1
    #    self.J2 = J2
  
                
    def predict(self,img):
        img2 = sweep(img,self.J1,1)
        #display(img2)
        out = output(img2,self.J2)
        return out
    
    def weight_mixer(Ja,Jb,shape):
        Jc = zeros(shape)
        n = shape[0]
        
        for i in range(n):
            for j in range(n):
                val = round(random)
                val = Ja[i,j]*val + Jb[i,j]*(1-val)
                Jc[i,j] = val
        return val
        
    def createMind(mind1, mind2):
        J1_new = weight_mixer(mind1.J1,mind2.J1)
        J2_new = weight_mixer(mind1.J2,mind2.J2)
        mind3 = mind(J1_new,J2_new)
        return mind3
        

def accuracy(mind,images,targets):
    correct = 0
    for counter, img in enumerate(images):
        if(mind.predict(img) == targets[counter]):
            correct += 1
    return correct/counter
    

mind1 = mind()
mind1.train_second(images3[1])
mind1.predict(images3[3]) 
J1 = mind1.J1
J2 = mind1.J2

J3 = sum(J1)

mind2 = mind()
mind2.predict(images3[10]) 
J2 = mind2.J1

display(images3[10])
accuracy(mind1,images3,target3)
mind1 = mind()
mind1.predict(images3[3])
lattice = random_init(n)
J = basic_train(images3[0:2])

list(map(display,images3[1:10]))

lat = sweep(images3[15],J,4)
display(lat)

while True:
    mind1 = mind()
    J3 = mind1.J1
    acc = accuracy(mind1,images3,target3)
    if acc > 0.51:
        print(acc)
        break


#calc_flip(img,J,1,2,1)
