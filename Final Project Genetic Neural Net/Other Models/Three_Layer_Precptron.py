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


def display(arr):

    cmap = colors.ListedColormap(['white','purple'])
    
    fig, ax= plt.subplots()
    ax.imshow(arr,cmap=cmap)
    


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

def random_img(m,t):
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




def final_filter(Filters,img):
    matches = []
    for Filter in Filters:
        matches.append(Filter.dot(img))
    highest = matches.index(max(matches))
    #index starts at zero filter
    return highest-1
    
class mind:
    n1=25
    n2=5
    n3=2
    J=array([])
    
    def  __init__(self,J="empty"):
        if J is "empty":
            self.J = random_init(self.n1*self.n2*self.n3)
        else:
            self.J = J
        return

    
    def decoder(self,i,j,l):
        n1 = self.n1
        n2 = self.n2
        J = self.J
        if l == 1:
            return J[(i)+n1*(j)]
        if l == 2:
            return J[i+n2*j+n1*n2]
        return "Not a layer"
    
    
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
        J = self.J
        J_new = copy(J)
        n = len(J)
        times = int(floor(ratio*n))
        while t < times:
 
            i = int(floor(random()*n))
        
            J_new[i] = J[i]*-1
            t += 1
        mind_new = mind(J_new)
        return mind_new


    def prepare_img(self,img):
        
        return array(img).flatten()
        
    def sum_winput(self,j_inputs,j,l):
        if l == 1:
            ni = self.n1
        elif l ==2:
            ni = self.n2
        else:
            ni = "error"
        #Sum up all the inputs weighted i*wi for the jth node
        w_inputs = list(map(lambda i: self.decoder(i,j,l),list(range(ni))))
        w_sum = j_inputs.dot(w_inputs)
        return w_sum
    
    def calc_flip(self,inputs,outputs,j,l):

        #linear algebra method
       
        w_sum = self.sum_winput(inputs,j,l)
        delE = w_sum*outputs[j]*2
        return delE

    def sweep(self,i_nodes,nj,l,outputs=[-1,-1]):
        outputs = [-1]*nj
        for i in range(nj):
                    #Calculating electrons change in E from spin flip at i,k,j
                    E_flip = self.calc_flip(i_nodes,outputs,i,l)
                    #If Energy is reduced, flip
                    if( E_flip < 0):
                        outputs[i] = outputs[i]*-1
    
        return array(outputs)
                
    
    def predict(self,img):
        pre_img = self.prepare_img(img)
        hidden_out = self.sweep(pre_img,nj=self.n2,l=1)
        final_out = self.sweep(hidden_out,nj=self.n3,l=2)
        if final_out[0] == final_out[1]:
            return 0
        #display(img2)
        
        number = final_out.argmax()
        return number
    
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
        
        

mind2 = mind1.miosis(1/10)
mind1.decoder(20,4,1)
mind2.decoder(1,1,1)
J1 = mind1.J
J2= mind2.J




one_image = array([[-1,1,1,1,-1],
                 [-1,1,1,1,-1],
                 [-1,1,1,1,-1],
                 [-1,1,1,1,-1],
                 [ 1,1,1,1, 1]])

zero_image = array([[-1, 1, 1,1,-1],
                 [ 1,-1,-1,-1, 1],
                 [ 1,-1,-1,-1, 1],
                 [ 1,-1,-1,-1, 1],
                 [-1, 1, 1, 1,-1]])


train_set_x = [abs(i%2+1)*random_img(zero_image,4)+abs((i)%2)*random_img(one_image,2) for i in range(100)]
train_set_y= [0,1]*100


display(train_set_x[0])
mind1 = mind()
mind1.predict(train_set_x[1])
accuracy(mind1,train_set_x,train_set_y)

accuracy(mind2,train_set_x,train_set_y)
mind1.predict(train_set_x[3])

a = 0
for i in range(10000):
    mind1 = mind()
    b = accuracy(mind1,train_set_x,train_set_y)
    if b >a:
        a = b


def accuracy(mind,images,targets):
    correct = 0
    i  = 0
    for img in images:
        
        if(mind.predict(img) == targets[i]):
            correct += 1
        i = i +1
    return correct/i
    

import matplotlib.pyplot as plt


def ring(minds,images, targets, children=10, gen=2, rand=1/5):
    i = 0
    j = 0
    w_acc = []
    def accs(minds,images,targets):
        acc = []
        for mind in minds:
            acc.append(accuracy(mind,images,targets))
        return acc
    
    while True:
        j=0
        
        acc = accs(minds,images,targets)
        if( i%10 == 0):
            print("Round: " + str(i))
            print(acc)
        max_acc = max(acc)
        w_acc.append(max_acc)
        winner = minds[acc.index(max_acc)]
        
        if(i == gen):
            
            plt.figure()
            plt.plot(range(1,i+2),w_acc)
            plt.xlabel("Generation")
            plt.ylabel("Accuracy")
            plt.show()
            return winner
        
        minds =[]
        minds.append(winner)
    
        while j < children:
            minds.append(winner.miosis(ratio=rand))
            j= j+1
        i= i+1
        
            
    return 

acc= [1.0, 0.5, 0.25, 0.5, 0.75, 0.5, 0.25, 0.5, 0.5, 0.75, 0.5]
acc.index(max(acc))
minds = [mind(),mind(),mind()]
win= ring(minds,train_set_x,train_set_y,gen=100,rand=1/10)
accuracy(win,train_set_x,train_set_y)
mind1 = mind()
#mind1.train_second(images3[1])
#mind1.predict(images3[4]) 


i = 0
import time

