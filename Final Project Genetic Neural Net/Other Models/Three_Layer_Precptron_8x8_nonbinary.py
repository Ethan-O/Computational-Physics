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

#Dislpay 2D array of -1 and 1
def display(arr):

    cmap = colors.ListedColormap(['white','purple'])
    
    fig, ax= plt.subplots()
    ax.imshow(arr,cmap=cmap)
    
#Randomly generate array of -1 and 1
def random_init(n):
    arr = array([0]*n)
    for i in range(len(arr)):
        #Will generate a 1 or -1 with 50% probability
        arr[i] = int(2*(random() // .5) -1)
        
    return arr
l2 = random_init(1000)
#Randomly modify a 2D map by t changes
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
#The Neural Net Classifier for 3 digits
class mind:
    #number of neurons in first, secound and third layer
    n1=64
    n2=5
    n3=3
    #Strengh of connections
    J=array([])
    
    def  __init__(self,J="empty"):
        if J is "empty":
            self.J = random_init(self.n1*self.n2*self.n3)
        else:
            self.J = J
        return

    #The J_ij connections are encoded this is to decode them
    def decoder(self,i,j,l):
        n1 = self.n1
        n2 = self.n2
        J = self.J
        if l == 1:
            return J[(i)+n1*(j)]
        if l == 2:
            return J[i+n2*j+n1*n2]
        return "Not a layer"
    #This returns a radomized by ratio version of the current neural net
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

    #Preparing the 2D array image of the neural net input
    def prepare_img(self,img):
        
        return array(img).flatten()
    
    # the sum of the weighted inputs going to the jth neuron, in layer l
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
    # calculating the energy gained/lossed in fliping the jth neuron
    def calc_flip(self,inputs,outputs,j,l):

        #linear algebra method
       
        w_sum = self.sum_winput(inputs,j,l)
        delE = w_sum*outputs[j]*2
        return delE
    #sweeping through each of the neurons in layer l, using outputs from previous layer as inputs
    def sweep(self,i_nodes,nj,l):
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
        

def accuracy(mind,images,targets):
    correct = 0
    i  = 0
    for img in images:
        
        if(mind.predict(img) == targets[i]):
            correct += 1
        i = i +1
    return round(correct/i,3)
    

import matplotlib.pyplot as plt

#The function that places the nets in competition and creates generations
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
        if( i%2 == 0):
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
            plt.title("Generation Randomization: " + str(rand))
            plt.show()
            return winner
        
        minds =[]
        minds.append(winner)
    
        while j < children:
            minds.append(winner.miosis(ratio=rand))
            j= j+1
        i= i+1
        
            
    return 


def genetic_cor(mind1, mind2):
    return (sum(abs(mind1.J + mind2.J))/2 )*1/(len(mind1.J))
        
def best_random(n,train_set_x,train_set_y):
    a = 0
    best_mind = mind()
    for i in range(n):
        mind1 = mind()
        b = accuracy(mind1,train_set_x,train_set_y)
        if b >a:
            a = b
            best_mind = mind1
    print(a)
    return best_mind


#Loading The Digits Dataset
digits = datasets.load_digits()
images = digits['images']
#Turning the values of -1 and 1
images2 = [(im > 10)*2-1 for im in images]
target = digits['target']

#Selecting only the images 0,1,2
zeros = digits['target']== 0
ones = digits['target'] == 1
twos = digits['target'] == 2
both = [a or b or c for a,b,c in zip(zeros,ones,twos)]

images3 = array(digits['images'])[both]
images3 = array([(im > 6)*2-1 for im in images3])

target3= array(digits['target'])[both]
#Just displaying some of the images
display(images[0])
display(images[1])
display(images3[2])


#Paritioning Training data and test data
train_ratio = 8/10
train_size= int(train_ratio*len(images3))
train_ind = array(sample(range(len(images3)), train_size))

train_set_x = [images3[i] for i in train_ind]
train_set_y = [target3[i] for i in train_ind]   

test_ind = delete(array(range(len(images3))),train_ind)
test_set_x = images3[test_ind]
test_set_y = target3[test_ind]

#Displaying a member of the training data
display(train_set_x[87])

#Creating two winners of two seperate selection cycyles
minds = [mind(),mind(),mind()]
win1= ring(minds,train_set_x,train_set_y,gen=50,rand=1/50)
minds = [mind(),mind(),mind()]
win2= ring(minds,train_set_x,train_set_y,gen=50,rand=1/10)

print(accuracy(win1,test_set_x,test_set_y))
print(accuracy(win2,test_set_x,test_set_y))

#Selecting the best of purely randomly generated connections
print("Random Generation")
mindr=best_random(500,train_set_x, train_set_y)

print(accuracy(mindr,test_set_x,test_set_y))

print(genetic_cor(win1,win2))


