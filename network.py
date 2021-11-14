from random import randint as rd
from copy import deepcopy as dp

import layer as lr
import functions as ft

class Network:

    def __init__(self, layers):
        self.layers=layers


    def network_pass(self, input_vec):
        working_vec=dp(input_vec)
        print(input_vec)
        for layer in self.layers:
            layer.calc_output(working_vec)
            working_vec=layer.return_vec()

        return working_vec



def network_gen(input_size, output_size):
    layers=[]
    hiden_layers=rd(0, 3)
    min_size=max(input_size, output_size)
    for i in range(hiden_layers):
        hiden_size=rd(min_size, min_size+5)
        layer=lr.Layer(
            [[rd(-10, 10) for i in range(input_size)] for j in range(hiden_size)],
            [rd(-10, -10) for i in range(input_size)],
            [lambda x: ft.linear(x) for i in range(input_size)]
        )
        layers.append(layer)
    
    out_layer=lr.Layer(
        [[rd(-10, 10) for i in range(input_size)] for j in range(output_size)],
        [rd(-10, -10) for i in range(input_size)],
        [lambda x: ft.linear(x) for i in range(input_size)]
    )
    return Network(layers)


def main():
    net1=network_gen(3, 3)
    print([1,2,3])


if __name__=="__main__":
    main()
