import numpy as np

def binary(x):
    if x<0:
        return 0
    else:
        return 1


def binary2(x):
    return int(x/abs(x))

def tanh(x):
    return np.tanh(x)

def binary_tanh(x):
    if x>0:
        return np.tanh(x)
    else:
        return 0

def r_linear(x):
    if x<0:
        return 0
    else:
        return x

    
def linear(x):
    return x


def gaussian(x):
    return (((np.e)**-x)**2)
