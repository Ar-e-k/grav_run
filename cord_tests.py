import matplotlib.pyplot as plt
from math import cos, sin, pi
from copy import deepcopy as dp

def find_dis(num):
    ang=2*pi/num
    dis=2-2*cos(ang)
    dis=dis**(1/2)
    return dis
    

def calc_cords(num, inverse=1, size=1):
    cords=[]
    dis=find_dis(num)

    ad=(
        pi/2*abs(num%2)*inverse+
        pi/num*abs(num%2-1)*abs(num%4-2)/2
    )

    for i in range(num):
        cord=[
            round(cos((i*2*pi)/num+ad)*size/dis, 3),
            round(sin((i*2*pi)/num+ad)*size/dis, 3)
        ]
        cords.append(cord)

    return cords
        
    min_x=sorted(cords, key=lambda x: x[0])[0][0]
    min_y=sorted(cords, key=lambda x: x[1])[int((inverse-1)/2)][1]

    new_min=sorted(dp(cords), key=lambda x: x[1])[0]

    '''
    for pos in range(len(cords)):
        cords[pos][0]+=abs(min_x)
        cords[pos][1]+=abs(min_y)*inverse
        
    return cords#'''

    print(new_min)
    for pos in range(len(cords)):
        print(cords[pos])
        cords[pos][0]+=abs(new_min[0])
        cords[pos][1]+=abs(new_min[1])
        print(cords[pos])

    return cords

def scatter(cords):
    xs=[]
    ys=[]

    for x, y in cords:
        xs.append(x)
        ys.append(y)

    plt.scatter(xs, ys)
    plt.axvline(0, color="black")
    plt.axhline(0, color="black")
    plt.show()

    
def main():
    num=int(input("Num of edges: "))
    inv=int(input("Inverse: "))
    size=int(input("Size: "))
    points=calc_cords(num, inv, size)

    print(points)
    scatter(points)


if __name__=="__main__":
    main()
