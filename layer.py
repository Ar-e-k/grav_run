import numpy as np
import functions as ft

class Layer:

    def __init__(self, matrix, bais, activation_vector):
        self.matrix=np.array(matrix)
        self.bais=np.array([bais]).T
        self.act_vector=activation_vector

        self.output_vec=np.empty((1,len(self.bais))).T


    def calc_output(self, input_vec):
        self.input_vec=np.array([input_vec]).T

        output_vec=self.matrix.dot(self.input_vec)
        output_vec+=self.bais

        for i in range(len(self.input_vec)):
            self.output_vec[i][0]=self.act_vector[i](output_vec[i][0])

            
    def return_out(self):
        return self.output_vec



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
