import sys
import pygame
from random import randbytes, randint, seed
from copy import deepcopy as dp

import player as pl
import obstacle as obs

class Game:

    def __init__(self, screen=None, players=[12], screen_size=[1,1]):
        self.screen=screen

        keys=[i for i in range(len(players))]

        self.players=dict(zip(keys, players))

        self.screen_size=screen_size
        self.player_offset=0.25
        self.inputs={}

        self.grav=8
        self.speed=1/300

        self.action={
            "jump":lambda x:self.players[x].check_jump(1),
            "big_jump":lambda x:players[x].check_jump(1.5),
            "flip":lambda x:self.players[x].flip_grav()
        }

        self.ai_action={
            "jump":lambda x, jump:self.players[x].check_jump(1.5*abs(jump)),
            "flip":lambda x, val:self.players[x].flip_grav(val)
            #"flip":lambda x, val:self.players[x].flip_grav() if val>=0 else x
        }

        self.obstacles=[
            #obs.EvenObstacle(8, 40, self.screen_size[0], self.screen_size[1], 0),
            #obs.EvenObstacle(4, 40, self.screen_size[0], self.screen_size[1], 0),
            obs.obstacle_creator(4, 40, self.screen_size[0], self.screen_size[1], 1)
        ]

        if screen:
            self.font=pygame.font.Font('freesansbold.ttf', 20)


    def frame(self):
        self.texts=[]
        #self.texts.append(len(self.obstacles))
        self.draw_background()

        self.screen_size=self.screen.get_size()

        self.inputs={}
        pl_del=[]
        for key, player in self.players.items():
            player.p_frame(self.grav)
            self.draw_player(player)
            colide=self.check_cols(player)
            if colide:
                pl_del.append(key)
            self.inputs[key]=self.find_inputs(player)

        for key in pl_del:
            del self.players[key]

        ob_del=[]
        for pos, obstacle in enumerate(self.obstacles):
            dele=self.move_obs(obstacle)
            if dele:
                ob_del.append(pos)
            self.draw_obs(obstacle)

        for i in range(len(ob_del)-1, -1, -1):
            self.obstacles.pop(ob_del[i])
        
        #if new_screen!=self.screen_size:
        for player in self.players.values():
            player.change_screen(self.screen_size)
        for obstacle in self.obstacles:
            obstacle.change_screen(self.screen_size)
            #if len(self.obstacles)==1:
            #    self.obstacles.append(obstacle.attache())
        #if len(self.obstacles)==0:
        self.gen_obs()

        self.add_texts()

        if len(self.players.keys())==0:
            return False
        return True


    def add_texts(self):
        x=0
        y=20
        for i in range(len(self.texts)):
            self.draw_text(str(self.texts[i]), [x, y*i])


    def ret_inputs(self):
        return self.inputs


    def ret_alive(self):
        return list(self.players.keys())

        
    def draw_background(self):
        rect=pygame.Rect([0, 0], self.screen_size)
        pygame.draw.rect(self.screen, [0,0,0], rect)


    def draw_text(self, text, cords):
        hight=self.font.render(text, False, [0,255,0])
        self.screen.blit(hight, cords)
    
    
    def draw_player(self, player):
        rect=player.ret_rect()
        rect=(
            rect[0]+int(self.player_offset*self.screen_size[0]),
            #0.5*self.screen_size[0],
            #0.5*self.screen_size[1],
            rect[1],
            rect[2],
            rect[3]
        )
        #self.texts.append([[rect[0], rect[1]], [rect[0], rect[1]+rect[3]], [rect[0]+rect[2], rect[1]], [rect[0]+rect[2], rect[1]+rect[3]]])
        rect=pygame.Rect(rect)
        pygame.draw.rect(self.screen, [0,0,255], rect)


    def draw_obs(self, poly):
        cords=poly.ret_pos()
        #self.texts.append(cords)
        #self.texts.append(poly.tow_h)
        poly=pygame.draw.polygon(self.screen, [0,255,255], cords)


    def gen_obs(self):
        ob=len(self.obstacles)
        #return False
        if ob!=6:
            max_prob=103
        else:
            max_prob=0
        #max_prob=(6-ob)*100
        prob=randint(0, max_prob)
        if prob>100:
            side=randint(0, 1)
            edge=randint(5, 6)
            edge=4
            new_obstacle=obs.obstacle_creator(edge, 40, self.screen_size[0], self.screen_size[1], dp(side))
            for obstacle in self.obstacles:
                ret=new_obstacle.check_box_col(obstacle.ret_max(), obstacle.ret_side())
                if ret:
                    break
                else:
                    pass
            else:
                if prob>102 and type(new_obstacle)==obs.EvenObstacle:
                    self.gen_tower(new_obstacle)
                self.obstacles.append(new_obstacle)


    def gen_tower(self, base):
        max_h=5
        num=randint(1, max_h**2)
        hight=int(((num)**(1/2)))
        hight=max_h-hight
        #hight=2
        for i in range(hight):
            base=base.attache()
            self.obstacles.append(base)
                
                
    def move_obs(self, obstacle):
        return obstacle.move(self.speed)


    def check_cols(self, player):
        pot=[False, False]
        colide=False

        points=player.ret_points()
        x1=self.player_offset*self.screen_size[0]
        x2=self.player_offset*self.screen_size[0]+points[1]
        y1=points[2]
        y2=points[3]

        for obstacle in self.obstacles:
            col=obstacle.check_collision([x1, x2, y1, y2])

            side=obstacle.ret_side()
            if side==0:
                pot[side]=max([col[1], pot[side]])
            else:
                if col[1]:
                    pot[side]=min([col[1], (pot[side] or col[1])])
            colide=colide or col[0]

        cap=[0, 0]
        cap[0]=pot[0] or 0
        cap[1]=pot[1] or self.screen_size[1]
        player.update_max_h(cap)

        return colide

    
    def player_actions(self, player, action):
        self.action[action](player)


    def ai_actions(self, outputs):
        fitnesses={}
        for pos in self.players.keys():
            for action in outputs[pos]:
                self.ai_action[action[1]](pos, action[0])
            fitnesses[pos]=1

        return fitnesses


    def find_inputs(self, player):
        obs=20
        if player==None:
            return 3+obs*2
        inputs=[]

        inputs.append(player.hight)
        inputs.append(player.grav_dir)
        #inputs.append(player.check_jump(None))
        inputs.append(player.v_speed)

        pos=0
        for pos, obstacle in enumerate(self.obstacles):
            if obstacle.pos[0]>self.player_offset:
                break
        for i in range(obs):
            try:
                inputs.append(self.obstacles[pos+i].pos[0])
                inputs.append(self.obstacles[pos+i].pos[1])
            except IndexError:
                inputs.append(0)
                inputs.append(0)

        return inputs


    def exit(self):
        pygame.quit()



def main(pl_count=1, frame=None, fit_func=None):
    seed(1)
    pygame.init()
    #screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    p=800
    screen=pygame.display.set_mode((p, int(p*9/16)), vsync=1)
    pygame.display.set_caption("Gravity runner")

    
    screen_size=[pygame.display.Info().current_w, pygame.display.Info().current_h]
    players=[pl.Player(screen_size=screen_size) for i in range(pl_count)]

    pygame.mouse.set_visible(False)
    playing=True
    play=Game(screen, players, screen_size)
    clock=pygame.time.Clock()
    return ai_while(playing, play, clock, frame, fit_func)
    return player_while(playing, play, clock)


def ai_while(playing, play, clock, frame, fit_func):
    while playing:
        #clock.tick(60)
        playing=play.frame()

        inputs=[i for i in range(5)]
        inputs=play.ret_inputs()
        alive=play.ret_alive()

        outputs=frame(inputs, alive)
        fitness=play.ai_actions(outputs)
        fit_func(fitness)

        pygame.display.flip()

    play.exit()
    return play


def player_while(playing, play, clock):
    while playing:
        clock.tick(60)
        playing=play.frame()
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==27:
                    paused=True
                    while paused:
                        for event in pygame.event.get():
                            if event.type==pygame.KEYDOWN:
                                if event.key==27:
                                    paused=False
                                
                    #sys.exit()
                elif event.key==32:
                    play.player_actions(0, "jump")
                elif event.key==118:
                    play.player_actions(0, "flip")
                elif event.key==98:
                    play.player_actions(0, "big_jump")
        pygame.display.flip()

    play.exit()
    return play


if __name__=="__main__":
    game1=main()
