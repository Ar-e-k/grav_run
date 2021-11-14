from math import cos, sin, pi
from copy import deepcopy as dp

class Obstacle:

    def __init__(self, edge, size, x, y, side=1, hight=0, pos=1, tow_h=1):
        self.hight=hight
        self.size=size
        self.edge=edge
        size=size*x/800
        self.cords=self.gen_cords(edge, size=size)#, inverse=inverse)
        #self.lines=self.calc_lines()
        self.side=side
        self.find_limits()

        self.tow_h=tow_h

        self.screen_size=[x, y]
        self.pos=[pos, self.side-(self.hight*(self.side*2-1))]


    def change_screen(self, new_screen):
        size=self.size*new_screen[0]/800
        self.cords=self.gen_cords(self.edge, size=size)
        self.screen_size=new_screen
        self.find_limits()
        
        
    def calc_lines(self):
        lines=[]
        count_dis=lambda i:(
            (self.cords[0][0]-self.cords[i][0])**2
            +(self.cords[0][1]-self.cords[i][1])**2
            )
        g_dis=min([count_dis(i) for i in range(1, len(self.cords))])
        
        for pos, point in enumerate(self.cords):
            for point2 in range(pos+1, len(self.cords)):
                point2=self.cords[point2]
                try:
                    grad=int((point[1]-point2[1])/(point[0]-point2[0]))
                     
                except ZeroDivisionError:
                    grad=0
                c=point[1]-grad*point[0]
                dis=(point[0]-point2[0])**2+(point[1]-point2[1])**2

                if dis==g_dis:
                    print("point1", point)
                    print("point2", point2)
                    print(grad, c, axis)
                    lines.append([grad, c, axis])

            #print("------------------Break------------------")
            
        return lines

    
    def find_limits(self):
        self.x_min=min([i[0] for i in self.cords])
        self.x_max=max([i[0] for i in self.cords])
        self.y_max=max([i[1] for i in self.cords])


    def check_box_col(self, points, side):
        if side==self.side:
            x_min=self.pos[0]*self.screen_size[0]-self.x_min
            x_max=self.pos[0]*self.screen_size[0]-self.x_max
            check1=self.check_x(points[0])
            check2=self.check_x(points[1])
            if not(check1) and not(check2):
                return False
            else:
                return True
        return False
        

    def check_collision(self, points):
        check1=self.check_x(points[0])
        check2=self.check_x(points[1])
        if not(check1) and not(check2):
            return False, False
        check3=self.check_y(points[2])
        check4=self.check_y(points[3])
        if not(check3) and not(check4):
            return False, True
        return True, False
        
        
    def check_x(self, x):
        x_min=self.pos[0]*self.screen_size[0]-self.x_min
        x_max=self.pos[0]*self.screen_size[0]-self.x_max
        if x>x_max and x<x_min:
            return True
        return False


    def check_y(self, y):
        y1=y*(self.side*2-1)
        y2=(self.pos[1]*self.screen_size[1]+self.y_max-(self.side*self.y_max*2))*(self.side*2-1)
        if y1>y2:
            return True
        return False

    
    def find_dis(self, num):
        ang=2*pi/num
        dis=2-2*cos(ang)
        dis=dis**(1/2)
        return dis
    

    def gen_cords(self, num, inverse=1, size=1):
        cords=[]
        dis=self.find_dis(num)

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

        mins=sorted(dp(cords), key=lambda x: x[1])[0]
    
        for pos in range(len(cords)):
            cords[pos][0]+=abs(mins[0])
            cords[pos][1]+=abs(mins[1])*inverse
        
        return cords


    def move(self, speed):
        if self.pos[0]-speed<0:
            #self.pos[0]=1
            return True
        else:
            self.pos[0]=self.pos[0]-speed

            
    def ret_pos(self):
        pos=[self.pos[0]*self.screen_size[0], self.pos[1]*self.screen_size[1]]
        new_cords=[]
        for cord in self.cords:
            new_cords.append([int(pos[0]-cord[0]), int(pos[1]+cord[1]-(self.side*cord[1]*2))])
        return new_cords


    def ret_side(self):
        return self.side 


    def ret_max(self):
        x_min=self.pos[0]*self.screen_size[0]-self.x_min
        x_max=self.pos[0]*self.screen_size[0]-self.x_max
        return [x_max, x_min]



class EvenObstacle(Obstacle):

    def __init__(self, edge, size, x, y, side=1, hight=0, pos=1, tow_h=1):
        super().__init__(edge, size, x, y, side, hight, pos, tow_h)
        self.find_top_x()


    def change_screen(self, new_screen):
        super().change_screen(new_screen)
        self.find_top_x()
        

    def find_top_x(self):
        self.x_tops=sorted(self.cords, key=lambda x: x[1])[0:2]
        self.x_tops=[i[0] for i in self.x_tops]
        

    def check_collision(self, points):
        f_check=super().check_collision(points)
        if not(f_check[0]) and not(f_check[1]):
            return False, False
        elif f_check[1]:
            slide1=self.check_above(points[0])
            slide2=self.check_above(points[1])
            return False, slide1 or slide2 
        else:
            return True, False

        
    def check_above(self, x):
        x_min=self.pos[0]*self.screen_size[0]-self.x_tops[0]
        x_max=self.pos[0]*self.screen_size[0]-self.x_tops[1]
        if x>x_max and x<x_min:
            return int(self.pos[1]*self.screen_size[1]+self.y_max-(self.side*self.y_max*2))
        return False


    def attache(self):
        cords=sorted(self.cords, key=lambda x: x[1])
        #print(cords)
        cords2=sorted(self.cords, key=lambda x: x[0])
        print(cords2)
        new_obs=EvenObstacle(
            self.edge,
            self.size,
            self.screen_size[0],
            self.screen_size[1],
            self.side,
            pos=dp(self.pos[0]),
            tow_h=int(self.tow_h+1),
            hight=dp((cords[-1][1]/self.screen_size[1])*self.tow_h)#*self.pos[1])
        )
        return new_obs
        


class OddObstacle(Obstacle):

    def check_collision(self, points):
        check1=super().check_collision(points)[0]
        return check1, False



def obstacle_creator(edge, size, x, y, side=1, hight=0, pos=1):
    if edge%2==0:
        return EvenObstacle(edge, size, x, y, side=side, hight=0, pos=1)
    else:
        return OddObstacle(edge, size, x, y, side=side, hight=0, pos=1)

    
def main():
    obs=Obstacle(4, 2, 10, 10)
    print(obs.return_pos())


if __name__=="__main__":
    main()
