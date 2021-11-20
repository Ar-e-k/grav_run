from random import uniform, seed

import network

def tester(power, num):
    seed(1)
    lis=[uniform(0, num**(1/power))**power for i in range(10000)]
    return sum(lis)/len(lis)


def main():
    net=network.Network(net="net1")
    bais_list=[]
    mat_list=[]
    for layer in net.layers:
        for bais in layer.bais_list:
            bais_list.append(bais)
        for mat in layer.mat_list:
            for num in mat:
                mat_list.append(num)

    print("mat:")
    print(max(mat_list), min(mat_list), sum(mat_list)/len(mat_list))
    print("bais:")
    print(max(bais_list), min(bais_list), sum(bais_list)/len(bais_list))


if __name__=="__main__":
    main()
