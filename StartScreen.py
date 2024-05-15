import random 
from Player import Player
from Game_util_tools import *
from Platform import Platform
from Button import Button

class Start_Screen():
    frames = [ ]
    for i in range(0,50):
        for _ in range(0,2):
            frames.append(GAME_UTIL.image_scale(rf"sky_up\IMGS\background_frames\frame_{i}_delay-0.03s.gif",(960,640)))
    
    def __init__(self,screen,screen_width,screen_height):
        #====================
        self.version = "1.0"
        pygame.mixer.music.set_volume(0.2)
        #====================
        self.start_date = datetime.datetime.now()
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.start_screen_is_running = True
        self.main_button = Button(self.screen ,self.screen_width//2-150 ,self.screen_height - 155,300,50,
                                  "#202020","PLAY",64,"#00ff00","#f4f4f4",1.5,"#aeaeae")
        self.platforms = [ ]
        for i in range(1,7):
            self.platforms.append(Platform(self.screen ,self.screen_width,self.screen_height,
                                           r"sky_up\IMGS\platforms\vulcan_plat1.png",
                                           random.randrange(100,600,20),
                                           i*100-50,
                                           random.choice([100,160,200]),
                                           20,
                                           "right" if i%2 == 0 else "left",
                                           random.choice([5,10])))
        self.pos = random.randint(0,5)    
        self.player = Player(self.screen ,self.screen_height,"",random.choice(colors),self.platforms[self.pos].X,self.platforms[self.pos].Y + 30)
        self.text_move = - 250

    def start_screen_draw(self):

        for platform in self.platforms:
            platform.draw()
        self.player.draw()
        GAME_UTIL.show_text(self.screen ,"SKY",200,"#00ff00",self.text_move,self.screen_height//2-100,2)
        GAME_UTIL.show_text(self.screen ,"Created by : Pr!tN",32,"#00ff00",self.text_move*1.7,self.screen_height//2+20,0.5)
        self.main_button.Y = self.screen_height - self.text_move + 65
        GAME_UTIL.show_text(self.screen ,"UP",200,"#00ff00",self.screen_width-self.text_move*2 if self.text_move > 0 else self.screen_width+250 
                            ,self.screen_height//2-100,2)
        GAME_UTIL.show_text(self.screen ,f"Version : {self.version}",32,"#00ff00",
                            self.screen_width-self.text_move*2.5 if self.text_move > 0 else self.screen_width+250 
                            ,self.screen_height//2 + 50,0.5)

        self.main_button.draw()
    
    def start_screen_engine(self):
        date_now = datetime.datetime.now()
        time_passed = (date_now - self.start_date).total_seconds()
        
        if time_passed >= 2:
            self.start_date = date_now
            self.pos = random.randint(0,5) 
            self.player.color = random.choice(colors)
            
        self.player.X = self.platforms[self.pos].X + 30
        self.player.Y = self.platforms[self.pos].Y - 30
        
        if self.text_move <= self.screen_width//2-270:
            self.text_move += 10
            
        for platform in self.platforms:
            platform.move()
            
        if self.main_button.clicked():
            self.start_screen_is_running = False  
            
    def start_screen_run(self):
        frame_index = 0
        while self.start_screen_is_running:

            self.screen.blit(self.frames[frame_index], (0, 0))
            frame_index = (frame_index + 1) % len(self.frames)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.start_screen_is_running = False
                    return "forced"

            self.start_screen_draw()
            self.start_screen_engine()
            clock.tick(60)
            pygame.display.update()