import numpy as np
from copy import deepcopy as dp

import main as gm
import network

class Evolution:

    def __init__(self, pop_size, input_size, output_names, runner):
        self.pop_size=pop_size
        self.input_size=input_size
        self.output_names=output_names
        self.runner=runner

        self.first_gen()


    def first_gen(self):
        nets=[network.network_gen(self.input_size, len(self.output_names))]

        self.generation=Generation(nets, list(self.output_names), self.runner)



class Generation:

    def __init__(self, nets, action_names, runner):
        self.gen_pop(nets)
        self.action_names=action_names
        self.runner=runner

        self.run()


    def gen_pop(self, nets):
        self.pops={}
        print(nets)
        for i in range(len(nets)):
            self.pops[i]=[nets[i], 0]


    def run(self):
        self.runner(len(self.pops.keys()), self.frame, self.fit_func)


    def frame(self, inputs):
        outs=[]
        for pop, net in self.pops.items():
            net=net[0]
            if net==None:
                outs.append[None]
                continue

            print(inputs)
            #print(net.)
            outputs=net.network_pass(inputs)
            for i, action in enumerate(self.action_names):
                outs.append([outputs[i], action])


    def fit_func(self, fitness):
        for key, value in fitness.itmes():
            self.pops[key]+=value



def main():
    pop_size=10
    input_size=1
    output_names=list(gm.Game().ai_action.keys())
    runner=gm.main
    evo1=Evolution(pop_size, input_size, output_names, runner)
    return evo1


if __name__=="__main__":
    test=main()
