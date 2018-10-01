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
    J= zeros((n*n,n*n))
    for m in maps:
        mf = m.flatten()
        for i in range(n*n):
            for xy in range(n*n):
                J[i,xy] += mf[xy]*mf[i]
               
    return 1/M*J
            
basic_train(A_image)
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



n = 8


lattice = random_init(n)
J = basic_train(images2[0:2])

list(map(display,images2[1:10]))

display(images2[1])
lat = sweep(images2[15],J,1)
display(lat)


calc_flip(img,J,1,2,1)
