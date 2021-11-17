import numpy as np
from copy import deepcopy as dp
from random import uniform as rd
from random import randint as ri

import functions as ft

class Layer:

    def __init__(self, matrix, bais, activation_vector):
        self.mat_list=matrix
        self.bais_list=bais

        self.matrix=np.array(matrix)
        self.bais=np.array([bais]).T
        self.act_vector=activation_vector

        self.output_vec=np.empty((1,len(self.bais))).T

    
    def calc_output(self, input_vec):
        if type(input_vec)==type([]):
            self.input_vec=np.array([input_vec]).T
        else:
            self.input_vec=input_vec

        output_vec=self.matrix.dot(self.input_vec)
        output_vec+=self.bais

        for i in range(len(self.output_vec)):
            self.output_vec[i][0]=self.act_vector[i](output_vec[i][0])


    def return_out(self):
        return self.output_vec


    def edit(self, rg):
        mut_prob=0.5
        mat_list=dp(self.mat_list)
        for i, row in enumerate(self.mat_list):
            for j in range(len(row)):
                if rd(0, 1)<mut_prob:
                    mat_list[i][j]+=rg

        bais_list=dp(self.bais_list)
        for i in range(len(self.bais_list)):
            if rd(0, 1)<mut_prob:
                self.bais[i]+=rg

        return Layer(mat_list, bais_list, self.act_vector)


    def edit2(self, rg):
        i=ri(0, len(self.mat_list)-1)
        j=ri(0, len(self.mat_list[0])-1)
        self.mat_list[i][j]=rg

        i=ri(0, len(self.bais_list)-1)
        self.bais_list[i]=rg

        return Layer(self.mat_list, self.bais_list, self.act_vector)


def main():
    layer1=Layer(
        [
            [2, 2, 2],
            [3, 3, 3],
            [4, 4, 4]
        ],
        [1, 2, 3],
        [
            lambda x: ft.linear(x),
            lambda x: ft.linear(x),
            lambda x: ft.linear(x)
        ]
    )
    layer1.calc_output([5, 6, 7])
    print(layer1.return_out())
    

if __name__=="__main__":
    main()
