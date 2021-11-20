from random import uniform as rd
from random import randint as ri
from random import seed
from copy import deepcopy as dp
from time import time
import pickle

import layer as lr
import functions as ft

class Network:

    def __init__(self, input_size=0, output_size=0, rang=0, layers=None, id=None, net=None):
        self.input_size=input_size
        self.output_size=output_size
        self.rang=rang

        self.id=id

        if not(layers):
            if not(net):
                self.layers=self.network_gen(input_size, output_size, rang)
            else:
                self.layers=self.load_net(net)
        else:
            self.layers=layers


    def network_pass(self, input_vec):
        working_vec=dp(input_vec)
        for layer in self.layers:
            layer.calc_output(working_vec)
            working_vec=layer.return_out()

        return working_vec


    def load_net(self, net):
        file=open("nets/"+net, "rb")
        layers=pickle.load(file)
        file.close()

        new_layers=[]
        for i in range(len(layers)-1):
            layer=lr.Layer(
                layers[i][0],
                layers[i][1],
                [lambda x: ft.tanh(x) for i in range(len(layers[i][1]))]
            )
            new_layers.append(layer)

        out_layer=lr.Layer(
            layers[-1][0],
            layers[-1][1],
            [lambda x:ft.binary_tanh(x), lambda x:ft.binary2(x)]
        )

        new_layers.append(out_layer)
        return new_layers

    
    def network_gen(self, input_size, output_size, rang):
        layers=[]
        hiden_layers=ri(0, 3)
        min_size=max(input_size, output_size)
        last_layer=input_size
        for i in range(hiden_layers):
            hiden_size=ri(min_size, min_size+5)
            layer=lr.Layer(
                [[rd(-rang, rang) for i in range(last_layer)] for j in range(hiden_size)],
                [rd(-rang, rang) for i in range(hiden_size)],
                [lambda x: ft.tanh(x) for i in range(hiden_size)]
            )
            layers.append(layer)
            last_layer=hiden_size

        out_layer=lr.Layer(
            [[rd(-rang, rang) for i in range(last_layer)] for j in range(output_size)],
            [rd(-rang, rang) for i in range(output_size)],
            [lambda x:ft.binary_tanh(x), lambda x:ft.binary2(x)]
            #[lambda x: ft.tanh(x) for i in range(output_size)]
        )
        layers.append(out_layer)
        return layers


    def evolve(self, gen):
        t=1000*time()
        seed(int(t) % 2**32)
        layers=[]
        for layer in self.layers:
            rang=self.rang
            new_layer=layer.edit(rd(0, rang**(1/2))**2*(ri(0, 1)*2-1))
            layers.append(new_layer)

        return Network(self.input_size, self.output_size, self.rang, layers=layers, id=str(str(self.id)+"."+str(gen)))


    def remake(self, gen):
        layers=[]
        for layer in self.layers:
            rang=self.rang
            new_layer=layer.remake(rang)
            layers.append(new_layer)

        return Network(self.input_size, self.output_size, self.rang, layers=layers, id=str(str(id)+"."+str(gen)))


    def evolve1(self):
        return Network(self.input_size, self.output_size, self.rang+rd(-self.rang/10, self.rang))


    def ret_mats(self):
        layers=[]
        for layer in self.layers:
            new_layer=[]
            new_layer.append(layer.mat_list)
            new_layer.append(layer.bais_list)
            layers.append(new_layer)
        return layers


def main():
    net1=network_gen(3, 3)


if __name__=="__main__":
    main()
