# Assignment 2 Python 3
# Ethan Otto 1/31/18

#10.3


def cum_sum(x):
    cum_sum=0
    list_cum = []
    length = len(x)
    i = 0
    for e in x:
        assert type(e) == int or type(e) == float
        cum_sum +=e
        list_cum.append(cum_sum)
        i += 1
        if i == length:
            return list_cum

t= cum_sum([1,2,3,4,5,6,7,8,9,10])
t


# 2D Class object Python 3

class Point(object):
    """A 2D Point object"""
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y
    
    def __str__(self):
        string = "{x: %d, y: %d }" % (self.x,self.y) 
        return string
    
    def __add__(self, other):
        assert isinstance(other,Point)
        p = Point()
        p.x = self.x + other.x
        p.y = self.y + other.y
        return p
    
    def __sub__(self, other):
        assert isinstance(other,Point)
        p = Point()
        p.x = self.x- other.x
        p.y = self.y - other.y
        return p
    
    def __mul__(self, num):
        assert isinstance(num, (float,int))
        p = Point()
        p.x = self.x*num
        p.y = self.y*num
        return p
    def __rmul__(self,num):
        return self*num
        
    def dot(self,other):
        assert isinstance(other,Point)
        dot = self.x*other.x + self.y*other.y
        return dot

p1 = Point(4,10)
p2 = Point(1,8)

print(p1+p2)
print(p1-p2)
print(p1*4)
print(4*p1)
p1.dot(p2)


