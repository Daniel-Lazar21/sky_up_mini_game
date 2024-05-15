from Game_util_tools import *
import time
class Button():
    def __init__(self,screen,X,Y,width,height,color,text,text_size,outline_color,
                 text_color,text_outline_size,text_outline_color):
        self.screen = screen
        self.X = X
        self.Y = Y
        self.width = width
        self.height = height
        self.color = color
        self.hover = False
        self.text_size = text_size
        self.text = text
        self.outline_color = outline_color
        self.text_color = text_color
        self.text_outline_size = text_outline_size
        self.text_outline_color = text_outline_color
        
    def draw(self):
        pygame.draw.rect(self.screen,self.outline_color,(self.X-5,self.Y-5,self.width+10,self.height+10),
                         border_radius=15 ,width = 5 )
        pygame.draw.rect(self.screen,self.color,(self.X,self.Y,self.width,self.height), 
                         border_radius=10)
        #calculez valorile pe care textul le are astfel incat sa pot centra textul in interiorul butonului
        text_width, text_height = GAME_UTIL.get_text_size(self.text, self.text_size)
        text_x = self.X + (self.width - text_width) // 2
        text_y = self.Y + (self.height - text_height) // 2 + 1 
        GAME_UTIL.show_text(self.screen,self.text, self.text_size, self.text_color, text_x, text_y,self.text_outline_size,self.text_outline_color)
        
    def check_hover(self):
        mouse_x , mouse_y = pygame.mouse.get_pos()
        my_rect = pygame.Rect(self.X-7.5,self.Y-7.5,self.width+15,self.height+15)
        if my_rect.collidepoint(mouse_x,mouse_y):
            if not self.hover: 
                self.X = self.X + 3
                self.Y = self.Y + 3

                self.width = self.width - 6
                self.height = self.height - 6
                self.text_size -= self.text_size//8
                self.hover = True
        else:
            if self.hover: 
                self.X = self.X - 3
                self.Y = self.Y - 3
                self.width = self.width + 6
                self.height = self.height + 6
                self.text_size += self.text_size//8
                self.hover = False
        return self.hover
    
    def clicked(self):
        if self.check_hover(): 
            if pygame.mouse.get_pressed()[0]:
                time.sleep(0.10)
                #mixer.Sound.play(mixer.Sound(my_sounds[0]))
                return True
            
        #verific daca apas butonul si incep jocul pe dificultataea aleasa!

class Slider():
    def __init__(self,screen,X,Y,width,height):
        self.screen = screen
        self.X = X
        self.Y = Y
        self.width = width
        self.height = height
        self.color = "#00ff00"
        self.circle_color = "#00ff00" 
        self.ball_pos = self.height//2
        self.circle_X = self.X + self.ball_pos
        self.circle_Y = self.Y + self.height//2 
        self.active = "ON"
        
    def draw(self):
        self.circle_X = self.X + self.ball_pos
        self.circle_Y = self.Y + self.height//2
        pygame.draw.rect(self.screen,self.color,(self.X,self.Y,self.width,self.height),2,20)
        pygame.draw.circle(self.screen,self.circle_color,(self.circle_X  ,self.circle_Y),self.height//2-4)
    
    def force_ON(self):
        self.circle_color = "#00ff00"
        self.color = "#00ff00"
        self.ball_pos = self.height//2
        self.active = "ON"
        
    def clicked(self):
        mouse_x , mouse_y = pygame.mouse.get_pos()
        my_rect = pygame.Rect(self.X,self.Y,self.width,self.height)
        if my_rect.collidepoint(mouse_x,mouse_y) and pygame.mouse.get_pressed()[0]:
            if self.active == "ON":
                self.circle_color = "#ff0000"
                self.color = "#ff0000"
                self.active ="OFF"
                self.ball_pos += self.width - self.height
            elif self.active == "OFF":
                self.color = "#00ff00"
                self.circle_color = "#00ff00"  
                self.active = "ON"
                self.ball_pos -= self.width - self.height
            time.sleep(0.2)
            return True
        
class Achievement_label():
    pass