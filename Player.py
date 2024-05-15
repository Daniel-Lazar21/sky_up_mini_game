from Game_util_tools import *

class Player():
    black_list = ["#000000","#212121","#222222","#232323","#242424","#252525","#262626"]
    def __init__(self,screen,screen_height,name,color,X,Y):
        self.screen = screen
        self.screen_height = screen_height
        self.sides_velocity = 10
        self.name = name 
        self.X = X
        self.Y = Y
        self.fall_velocity = 15 #velocity trebuie sa scada treptat pt a putea ajunge = cu Y-ul unei platforme ! 
        self.is_landing = True
        self.color = color
        
    def draw(self):
        
        GAME_UTIL.show_text(self.screen,f'{self.name}', 20, '#ff0000', self.X-len(self.name)*len(self.name)/4.5, self.Y - 15)
        pygame.draw.rect(self.screen, "#000000" ,(self.X, self.Y, 30, 30),border_radius = 7,width=2)
        pygame.draw.rect(self.screen, self.color ,(self.X+2, self.Y+2, 26, 26),border_radius = 5)
    
    def fall(self):
        if self.Y < self.screen_height - 50:
            self.Y += self.fall_velocity
