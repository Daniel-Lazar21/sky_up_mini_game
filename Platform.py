from Game_util_tools import *

class Platform():
    def __init__(self,screen,screen_width,screen_height,image,
                 X,Y,width,height,dir,velocity):
        self.screen_height = screen_height
        self.screen = screen
        self.screen_width = screen_width
        self.image = image
        self.X = X
        self.Y = Y
        self.dir = dir
        self.velocity = velocity
        self.touched = False
        self.width = width
        self.height = height
        
    def draw(self):
        self.screen.blit(GAME_UTIL.image_scale(self.image,(self.width,self.height)), (self.X,self.Y))
        #pygame.draw.rect(self.screen,"#aeaeae" ,(self.X+1,self.Y+1,self.width-2,self.height-2),border_radius = 10)
        #pygame.draw.rect(self.screen,self.outline_color ,(self.X-2,self.Y-2,self.width+4,self.height+4),border_radius = 10,width=2)
        
    def move(self):
        
        if self.X == 0:
            self.dir = "right"
        elif self.X == self.screen_width - self.width:
            self.dir = "left"
        
        if self.dir == "right":
            self.X += self.velocity
        elif self.dir == "left":
            self.X -= self.velocity
    
    def fall(self):
        self.Y += 100
    
    def out_of_screen(self):
        return self.Y > self.screen_height 