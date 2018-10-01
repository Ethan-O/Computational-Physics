#Assignment 1 Computational Physics
# Ethan Otto 1/22/18

# Ex 5.3 Python 3
def check_fermat(a,b,c,n):
    exp = (a**n + b**n == c**n)
    if(n > 2 and exp):
        print("Holy smokes,Fermat was wrong!")
    else:
        print("No, that doesn't work")

def prompt_user():
    a = int(input("Please enter a:\n"))
    b = int(input("Please enter b:\n"))
    c = int(input("Please enter c:\n"))
    n = int(input("Please enter n:\n"))
    
    check_fermat(a,b,c,n)

prompt_user()

# Ex 7.2 Python 3

def square_root(a):
    x = a/2
    while True:
        print(x)
        y = (x + a/x)/2
        epsilon = 0.00000000001
        y = (x + a/x)/2
        if( abs(x-y) < epsilon):
            return x
        x=y

square_root(100)