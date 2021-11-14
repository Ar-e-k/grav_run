class Player:

    def __init__(self, mass=10000, force=200, width=0.04, hight=0.1, speed_limit=0.012, screen_size=[1, 1]):
        self.mass=mass
        self.force=force
        self.p_hight=hight
        self.width=width

        self.screen_size=screen_size

        self.speed_limit=speed_limit

        self.v_speed=0
        self.speed=1 
        self.hight=1-self.p_hight
        self.jump=0
        self.grav_dir=1


    def change_screen(self, new_screen):
        self.screen_size=new_screen
        
        
    def p_frame(self, grav, h_max):
        h_max[0]/=self.screen_size[1]
        h_max[1]/=self.screen_size[1]
        
        self.update_v_speed(grav, h_max)
        self.update_hight(h_max)
        self.jump=0


    def update_hight(self, h_max):
        self.hight+=self.v_speed
        if self.hight>h_max[1]-self.p_hight:
            self.hight=h_max[1]-self.p_hight
            self.v_speed=0
        elif self.hight<h_max[0]:
            self.hight=h_max[0]
            self.v_speed=0
            
        
    def update_v_speed(self, grav, h_max):
        self.v_speed-=self.force*self.jump*self.grav_dir/self.mass
        if not(
                (self.hight==1-self.p_hight and self.grav_dir==1)
                or
                (self.hight==0 and self.grav_dir==-1)):
            grav_speed=grav*self.grav_dir/self.mass
            self.v_speed+=grav_speed

        #return None
            if not(
                    (self.v_speed>0 and self.grav_dir<0)
                    or
                    (self.v_speed<0 and self.grav_dir>0)):

                air=1.3
                if self.v_speed>self.speed_limit:
                    buff=self.v_speed-grav_speed*air
                    if buff>self.speed_limit:
                        self.v_speed=buff
                    else:
                        self.v_speed=self.speed_limit
                elif self.v_speed<-self.speed_limit:
                    buff=self.v_speed-grav_speed*air
                    if buff<-self.speed_limit:
                        self.v_speed=buff
                    else:
                        self.v_speed=-self.speed_limit

    
    def flip_grav(self):
        self.grav_dir*=-1


    def check_jump(self, jump, h_max):
        h_max[0]/=self.screen_size[1]
        h_max[1]/=self.screen_size[1]
        
        if self.hight==h_max[0] or self.hight==h_max[1]-self.p_hight:
            self.jump=jump


    def ret_rect(self):
        rect=[
            0,
            int(self.hight*self.screen_size[1]),
            int(self.width*self.screen_size[0]),
            int(self.p_hight*self.screen_size[1])
        ]
        return rect


    def ret_points(self):
        points=[
            0,
            int(self.width*self.screen_size[0]),
            int(self.hight*self.screen_size[1]),
            int((self.hight+self.p_hight)*self.screen_size[1])
        ]
        return points