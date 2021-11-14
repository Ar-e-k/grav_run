import numpy as np

def binary(x):
    if x<0:
        return 0
    else:
        return 1

    
def tanh(x):
    return np.tanh(x)


def r_linear(x):
    if x<0:
        return 0
    else:
        return x

    
def linear(x):
    return x


def gaussian(x):
    return (((np.e)**-x)**2)
