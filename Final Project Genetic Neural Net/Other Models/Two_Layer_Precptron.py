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
display(images3[130])
target3[60]
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
    arr = array([0]*n)
    for i in range(len(arr)):
        #Will generate a 1 or -1 with 50% probability
        arr[i] = int(2*(random() // .5) -1)
        
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
        
def convolute(img):
    s = img
    hori = [0,0,1,1,1,1,0,0]
    vert = [0,0,1,1,1,1,0,0]
    o1 = s[-1,:].dot(hori)
    o2 = s[-2,:].dot(hori)
    o3 = s[1,:].dot(hori)
    o4 = s[2,:].dot(hori)
    o5 = s[:,2].dot(vert)
    o6 = s[:,3].dot(vert)
    o7 = s[:,4].dot(vert)
    o8 = s[:,5].dot(vert)
    
    out = array(array([o1,o2,o3,o4,o5,o6,o7,o8]) > 0,dtype=int)
    return out
    #display(s)
   
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
    

def calc_flip(i_nodes,outputs,J,i):

    #linear algebra method
    Sumj = sum(J[:,i])
    delE = Sum_j*outputs[i]*2
    return delE


def sweep(i_nodes,J,n2):
    
    outputs = [-1,-1]
    for i in range(n2):
                #Calculating electrons change in E from spin flip at i,k,j
                E_flip = calc_flip(i_nodes,outputs,J,i)
                #If Energy is reduced, flip
                if( E_flip < 0):
                    outputs[i] = outputs[i]*-1

    return array(outputs)

def output(inputs,J,n2):
    
    total = inputs.dot(J)
    if total == 0:
        return 1
    
    return int((sign(total)+1)/2)

class mind:
    n1=8
    n2=2
    J1
    J_layers
    
    def mutate(self,ratio):
        t = 0
        n= self.n1
        
        times = int(floor(ratio*len(J1)))
        while t < times:
            
            i = int(floor(random()*n*n))
            j = int(floor(random()*n*n))
        
            self.J1[i,j] = self.J1[i,j]+ round(random())*2 -1
            t += 1
        return
        
    def miosis(self,ratio):
        t = 0
        n= self.n1
        J_new
        J = self.J_layers
        times = int(floor(ratio*len(J1)))
        while t < times:
            w = J.flatten()
                
            i = int(floor(random()*n*n))
            j = int(floor(random()*n*n))
        
            self.J1[i,j] = w[i,j]+ round(random())*2 -1
            t += 1
        return
    
    """def train_second(self,img):
        n = self.n
        for i in range(n):
            for j in range(n):
                self.J2[i,j] = img[i,j]
        return
       """    
    def  __init__(self):
        self.J1 = random_init(n1*n2).reshape((n1,n2))
        self.J2 = [1,1]#array([2*(random()-0.5),2*(random()-0.5)])
         
        return
    
    #def __init__(J1,J2):
    #    self.J1 = J1
    #    self.J2 = J2
  
                
    def predict(self,img):
        
        first = sweep(img,self.J1,n2=self.n2)
        #display(img2)
        out = output(first,self.J2,n2=self.n2)
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
    i  = 0
    for img in images:
        
        if(mind.predict(img) == targets[i]):
            correct += 1
        i = i +1
    return correct/i
    
def ring(minds,rep, gen, rand, win):
    i = 0
    while i < gen:
        acc = []
        for mind in minds:
            acc.append(accuracy(mind,images,targets))
        winner = minds[acc.index(max(acc))]
        minds2 =[]
        minds2.append(winner)
        while j < gen:
            minds2.append(winner.mutate(ratio=rand))
        i= i+1
    
        
        
mind1 = mind()
#mind1.train_second(images3[1])
#mind1.predict(images3[4]) 

J1 = mind1.J1
J2 = mind1.J2
for i in range(len(images3)):
    print(mind1.predict(images3[i]))
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

con= convolute(images3[1])

i = 0
import time

champs = []
while True:

    i= i+1
    if i % 1000 == 0:
        print (i)
    
    time1 = time.time()
    mind1 = mind()
    time2 = time.time()
    #print(time2-time1)
    time3 = time.time()
    acc = accuracy(mind1,images3,target3)
    time4 = time.time()
    #print(time4-time3)
    if acc > 0.92:
        champs.append(mind1)
        print(acc)
        print (i)
        if (i > 10000):
            break

champs[1].J1

rand = random()
new_champ_J1= rand*champs[1].J1 + (1-rand)*(champs[0].J1)

accuracy(champs[2],images3,target3)
champs[4].J1

mind2 = mind()
mind2.J1 = new_champ_J1
accuracy(mind2,images3,target3)

#calc_flip(img,J,1,2,1)
