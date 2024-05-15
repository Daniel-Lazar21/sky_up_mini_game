from Button import *

class SETTINGS():
    def __init__(self,screen,screen_height) -> None:
        self.my_sound_sfx = pygame.mixer.Sound(my_sounds[0])
        self.my_sound_sfx.set_volume(0.2)
        self.screen_height = screen_height
        self.volume = 0.1
        self.index_volume = int((self.volume/0.01)/5 - 1) + 1
        self.volume_levels = [ ]
        self.screen = screen
        self.settings_button = Button(self.screen,860,20,80,30,'#212121',"Settings",25,"#ff00ff","#FFD700",0.5,"#ff0000")
        self.settings_triggered = False
        self.settings_translate = 290 
        self.slider_volume = Slider(self.screen,self.settings_translate + 870,87.5,50,25)
        self.SFX_slider = Slider(self.screen,self.settings_translate + 800,210,60,23)
        for i in range (0,20):
            self.volume_levels.append([self.screen,"#00ff00",( 715 + i*10,150 - i,8,8 + 2*i),1,10])
            
    def draw(self):
        transparent = GAME_UTIL.image_scale(r"sky_up/IMGS/transparent.png",(280,self.screen_height-10))
        self.screen.blit(transparent,(self.settings_translate + 675,5))#-self.screen_height))
        pygame.draw.rect(self.screen,"#212121",(self.settings_translate + 670,0,290,self.screen_height), width = 10, border_radius = 20)
        GAME_UTIL.show_text(self.screen,f"Volume {int(self.volume*100)}%",32,"#00ff00",self.settings_translate + 720,90,2,"#000000")
        for _rect in self.volume_levels:
            pygame.draw.rect(_rect[0],_rect[1],(self.settings_translate +_rect[2][0],_rect[2][1],_rect[2][2],_rect[2][3]),_rect[3],_rect[4])
            pygame.draw.rect(_rect[0],"#000000",(self.settings_translate +_rect[2][0],_rect[2][1],_rect[2][2],_rect[2][3]),1,_rect[4])  
        self.slider_volume.draw()
        self.SFX_slider.draw()    
        GAME_UTIL.show_text(self.screen,f"SFX: ",35,"#00ff00",self.settings_translate + 720,210,2,"#000000")
        
    def volume_control(self):
        mouse_x,mouse_y = pygame.mouse.get_pos()
        for rect in range(self.index_volume,20):
            self.volume_levels[rect][3] = 1
        for i in range (0,len(self.volume_levels)):
            rect = pygame.Rect(715 + i*10,150 - i,8,8 + 2*i)
            if rect.collidepoint(mouse_x,mouse_y):
                
                for rect in range (0,20):
                    self.volume_levels[rect][3] = 1
                for rect in range(0,i+1):
                    self.volume_levels[rect][3] = 0
                if pygame.mouse.get_pressed()[0]: 
                    self.play_sfx_sound()
                    time.sleep(0.15)
                    self.volume = 0.01*((i+1)*5)
                    self.index_volume = int((self.volume/0.01)/5 - 1) + 1
                    self.slider_volume.force_ON() 
                    
            else:
                for rect in range(0,self.index_volume):
                    self.volume_levels[rect][3] = 0
    
    def play_sfx_sound(self):
        if self.SFX_slider.active == "ON":  

            mixer.Sound.play(self.my_sound_sfx)  
            #TODO vedem alta data daca se mai poate face ceva cu sfx sounds 
    
    def sliders_slide(self):     
        if self.slider_volume.clicked():
            self.play_sfx_sound()
            if self.volume:
                self.volume = 0
                self.index_volume = 0
            else:
                self.volume = 0.2
                self.index_volume = 4
                
        if self.SFX_slider.clicked(): 
            if self.SFX_slider.active == "OFF":
                mixer.Sound.play(mixer.Sound(my_sounds[0]))
                
    def move_button_settings(self):
        if self.settings_triggered:
            if self.settings_translate > 0:
                self.settings_translate -= 29
                self.settings_button.X -= 7.5
                self.slider_volume.X -= 29
                self.SFX_slider.X -= 29
        else:

            if self.settings_translate < 290:
                self.settings_translate += 29  
                self.settings_button.X += 7.5
                self.slider_volume.X += 29
                self.SFX_slider.X += 29  
                 
    def check_settings_button(self):
        if self.settings_button.clicked() :
            self.play_sfx_sound()
            self.settings_triggered = not self.settings_triggered     
                                