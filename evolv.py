import numpy as np
from copy import deepcopy as dp
#from matplotlib import pyplot as plt

import main as gm
import network

class Evolution:

    def __init__(self, pop_size, input_size, output_names, runner):
        self.pop_size=pop_size
        self.input_size=input_size
        self.output_names=output_names
        self.runner=runner

        self.fitnesses=[]
        self.max_20_fitnesses=[]
        self.max_fitnesses=[]


    def first_gen(self):
        self.gen_num=1

        nets=[network.Network(self.input_size, len(self.output_names), 0.5, id=i) for i in range(self.pop_size)]

        self.generation=Generation(nets, list(self.output_names), self.runner)
        out=self.runner(len(self.generation.pops.keys()), self.generation.frame, self.generation.fit_func)
        self.fitness=self.generation.ret_fitness()

        return self.gen()


    def gen(self):
        nets=self.evolve()

        if self.gen_num==50:
            return self.fitnesses, self.max_fitnesses, self.max_20_fitnesses

        self.generation=Generation(nets, list(self.output_names), self.runner)
        out=self.runner(len(self.generation.pops.keys()), self.generation.frame, self.generation.fit_func)
        self.fitness=self.generation.ret_fitness()

        return self.gen()


    def evolve(self):
        total_fitness=0
        max_fit=[[0, 0] for i in range(int(self.pop_size*0.2))]
        for pos, fit in self.fitness.items():
            fit=fit[1]
            total_fitness+=fit
            if fit>max_fit[0][0]:
                max_fit[0]=[fit, pos]
                max_fit=sorted(max_fit, key=lambda x:x[0])

        max_fit=sorted(max_fit, key=lambda x:x[0], reverse=True)
        av_max=sum([i[0] for i in max_fit])/len(max_fit)

        if len(self.max_20_fitnesses)!=0 and (av_max<max(self.max_20_fitnesses) or max_fit[0][0]<max(self.max_fitnesses)) and False:
            nets=[]
            for net in self.fitness.values():
                net=net[0]
                nets.append(net)
            print(av_max)
            print(self.max_20_fitnesses)
            return nets

        self.graphs(total_fitness, max_fit[0][0], av_max, self.fitness[max_fit[0][1]][0].id)
        self.gen_num+=1

        nets=[]

        i=0
        while len(nets)<=self.pop_size:
            if i<len(max_fit):
                for j in range(int((len(max_fit)-i)/4)):
                    nets.append(self.fitness[max_fit[i][1]][0].evolve(gen=self.gen_num-1))
            else:
                i=-1
            i+=1

        if len(self.max_fitnesses)!=0 and max_fit[0][0]<max(self.max_fitnesses) and False:
            for i in range(0, len(max_fit)):
                print("-----"+str(i)+"-----")
                print(max_fit[i])
                print(self.fitness[max_fit[i][1]][0].id, self.fitness[max_fit[i][1]][1])

        nets=nets[0:int(self.pop_size*0.8)]
        nets+=[self.fitness[pos[1]][0] for pos in max_fit]
        return nets


    def evolve2(self):
        total_fitness=0
        max_fit=0
        max_fit_pos=0
        for pos, fit in self.fitness.items():
            fit=fit[1]
            total_fitness+=fit
            if fit>max_fit:
                max_fit=fit
                max_fit_pos=pos

        self.graphs(total_fitness, max_fit)
        self.gen_num+=1

        fits={}
        nets=[self.fitness[max_fit_pos][0]]
        for lis in self.fitness.values():
            net=lis[0]
            fit=lis[1]
            num=round(self.pop_size*fit/total_fitness-0.3)
            fits[net]=num
            continue
            for i in range(num):
                if i==0 and num!=1:
                    #continue
                    nets.append(net)
                #print(round(self.pop_size*fit/total_fitness))
                #print(fit)
                nets.append(net.evolve())


        work_fits=dp(fits)
        while len(nets)!=self.pop_size:
            for net, lim in work_fits.items():
                if lim!=0:
                    work_fits[net]-=1
                    nets.append(net.evolve())
                    break
            else:
                work_fits=dp(fits)
        '''
        print(len(nets))
        while len(nets)<self.pop_size:
            nets.append(self.fitness[max_fit_pos][0].evolve())

        nets=nets[0:self.pop_size]
        '''

        return nets


    def graphs(self, total_fitness, max_fit, av_top=0, id=None):
        print("\n\n\n--------"+str(self.gen_num)+"--------")
        print("Average fitness:", total_fitness/self.pop_size)
        if av_top:
            print("Average top 20%:", av_top)
        print("Top fitness:", max_fit)
        print("Top fitness ID:", id)

        self.fitnesses.append(total_fitness/self.pop_size)
        self.max_fitnesses.append(max_fit)
        self.max_20_fitnesses.append(av_top)

        #plt.plot([i for i in range(self.gen_num)], self.fitnesses)
        #plt.plot([i for i in range(self.gen_num)], self.max_fitnesses)
        #plt.plot([i for i in range(5)], [i for i in range(5)])

        #print(plt)
        #plt.show()


    def next_gen(self):
        pass



class Generation:

    def __init__(self, nets, action_names, runner):
        self.gen_pop(nets)
        self.action_names=action_names
        self.runner=runner

        #self.run()


    def gen_pop(self, nets):
        self.pops={}
        for i in range(len(nets)):
            self.pops[i]=[nets[i], 0]


    def run(self):
        self.runner(len(self.pops.keys()), self.frame, self.fit_func)


    def frame(self, inputs, alive):
        outs={}
        for pop in alive:
            net=self.pops[pop][0]
            if net==None:
                outs[pop]=[None]
                continue

            outputs=net.network_pass(inputs[pop])
            outs[pop]=[]
            for i, action in enumerate(self.action_names):
                outs[pop].append([float(outputs[i]), action])

        return outs


    def fit_func(self, fitness):
        for key, value in fitness.items():
            self.pops[key][1]+=value


    def ret_fitness(self):
        return self.pops
        fitness={}
        for pop, fit in self.pops.items():
            fit=fit[1]
            fitness[pop]=fit



def main():
    pop_size=100
    input_size=gm.Game().find_inputs(None)
    output_names=list(gm.Game().ai_action.keys())
    runner=gm.main
    evo1=Evolution(pop_size, input_size, output_names, runner)

    av, mx, at=evo1.first_gen()

    from matplotlib import pyplot as plt
    plt.plot([i for i in range(len(av))], av)
    plt.plot([i for i in range(len(mx))], mx)
    plt.plot([i for i in range(len(mt))], mt)
    plt.show()

    return evo1


if __name__=="__main__":
    test=main()
