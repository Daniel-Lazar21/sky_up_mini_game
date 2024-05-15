import random 
import math
import pandas as pd
import time
import datetime
from Player import Player
from Game_util_tools import *
from Platform import Platform
from Settings import *

class Game():
    def __init__(self,screen,screen_width,screen_height,player_name,player_color,difficulty,volume):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_color = player_color
        self.platforms = [ ]
        self.platforms_img = r"sky_up\IMGS\platforms\grass_plat2.png"
        self.backgrounds = [GAME_UTIL.image_scale(r"sky_up\IMGS\backgrounds\ground.jpg",(self.screen_width,self.screen_height)),
                            GAME_UTIL.image_scale(r"sky_up\IMGS\backgrounds\sky1.jpg",(self.screen_width,self.screen_height)) ]
        self.background_level = 0
        self.next_step = 0

        #de astea am nevoie ca sa poata incepe melodia dar si ca sa pot pune pauza si melodia sa 
        #continue de unde a ramas !
        self.volume = volume # o sa trebuiasca sa i dai volumul din meniu
        self.start_date = datetime.datetime.now()
        self.music = None
        self.passed_wall = False 
        self.game_is_runnig = True
        self.player_name = player_name
        self.player_info_csv = self.read_data()
        self.player_index = self.player_info_csv.index[self.player_info_csv['name'] == self.player_name]
        self.achievements = str(self.player_info_csv.loc[self.player_index, "achievements"]).split(" ")[4].replace('\nName:',"").replace("'","")
        print(self.achievements)
        self.player = Player(self.screen,self.screen_height,self.player_name,self.player_color,
                             self.screen_width//2-30,self.screen_height-50)
        self.able_to_swap_walls = False
        self.high_score = False
        self.score = 0
        self.GAME_MODE = difficulty
        self.platforms_velocity = None
        self.platforms_length = None
        self.game_mode_difficulty()
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.load(self.music)  # Load the music file
        pygame.mixer.music.play(-1)
        self.create_platforms()
        #asa recunsoc pe orice dificultate la ce achievement se afla ca sa i pot da display pe ecran
        self.achievement_targets_dict = {0:10,1:50,2:100,3:250,4:500} 
        self.achievement_box_translate = 150
        self.one_target_reached = False
        self.time_trigger = None
        self.achievements_active = False
        self.target_index = 0
        self.time_touch = None
        self.platform_touched_rec = None
        #SETTINGS
        self.SETTINGS = SETTINGS(self.screen,self.screen_height)
        self.forced_closed = False
        
    def pause_game(self):
        pygame.mixer.music.stop()
        paused_time = (datetime.datetime.now() - self.start_date).total_seconds()
        paused = True
        while paused:
            self.game_graphics()
            self.screen.blit(GAME_UTIL.image_scale(r'sky_up\IMGS\transparent.png',(self.screen_width,self.screen_height)),(0,0))
            GAME_UTIL.show_text(self.screen,"PAUSED",128,"#242424",300,250) 
            #screen.blit(self.screen,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    paused = False
                    self.forced_closed = True
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        time.sleep(0.2)
                        self.volume = self.SETTINGS.volume
                        pygame.mixer.music.set_volume(self.SETTINGS.volume)
                        pygame.mixer.music.play(-1,start = paused_time)
              
                        paused = False   
                        
            self.SETTINGS.check_settings_button()
            self.SETTINGS.draw()
            self.SETTINGS.move_button_settings()
            self.SETTINGS.settings_button.draw()
            self.SETTINGS.volume_control()
            self.SETTINGS.sliders_slide()
            pygame.display.update()
            clock.tick(120)    
            
    def create_platforms(self):
        for i in range(1,7):
            self.platforms.append(Platform(self.screen,self.screen_width,self.screen_height,
                                           self.platforms_img,
                                           random.randrange(100,600,20),
                                           i*100-50,
                                           self.platforms_length,20,
                                           "right" if i%2 == 0 else "left",
                                           self.platforms_velocity))
    #TODO arat-i user-ului la inceput butoanele pe care poate apasa
    def show_controls(self):
        #TODO de lucrat la afisarea controalelor pe ecran la inceput
        controls = GAME_UTIL.image_scale(r"sky_up\IMGS\keyboard.png",(60,100))
        self.screen.blit(controls,(self.screen_width//2-20,self.screen_height-130))
    
    def platforms_fall(self):
        for platform in self.platforms:
            platform.fall()   
    
    def check_touch_time(self):
        if self.time_touch:
            if (datetime.datetime.now() - self.time_touch).total_seconds() > 0.1:
                self.platform_touched_rec.Y -= 10 
                self.player.Y -= 10 
                self.time_touch = 0 
           
    def collide_up(self):
        for platform in self.platforms:
            if self.player.Y + 30 == platform.Y:
                if self.player.X in range(platform.X - 25 ,platform.X + platform.width - 10) :
                    self.player.fall_velocity = 0
                    self.player.sides_velocity = 10  
                    
                    if not self.time_touch and not self.player.is_landing:
                        platform.Y += 10
                        self.platform_touched_rec = platform
                        self.player.Y += 10
                        self.time_touch = datetime.datetime.now()
                        
                    self.player.is_landing = True
                    if not platform.touched :

                        if self.passed_wall:
                            self.score += 3
                            self.passed_wall = False
                        else:
                            self.score += 1
                        platform.touched = True
                        #_____________
                        #aici practic eu fac player-ul sa cada deodata cu platforma pe care s-a asezat!
                        if self.score >= 4:
                            self.player.Y += 100
                            self.platforms_fall()
                            self.background_level += 8
                            #schimba ecranul la multiplu de bck_lvl -1 
                        #______________
                    if platform.dir == "right":
                        self.player.X += platform.velocity
                    elif platform.dir == "left":
                        self.player.X -= platform.velocity
                else:
                    if self.player.is_landing == True:
                        self.player.fall_velocity = 10
                        self.player.sides_velocity = 10 
                        self.player.is_landing = False
                        
                    else:
                        self.passed_wall = False

    def set_platform_img(self):
        if self.score < 83:
            self.platforms_img = rf"sky_up\IMGS\platforms\grass_plat{random.randint(1,2)}.png"
        elif self.score >= 83 and self.score < 163:
            self.platforms_img = rf"sky_up\IMGS\platforms\cloud_plat{random.randint(1,2)}.png"
        elif self.score >= 163:
             self.platforms_img = rf"sky_up\IMGS\platforms\vulcan_plat{random.randint(1,2)}.png"
             
    def collide_down(self):
        for platform in self.platforms:
            if self.player.Y == platform.Y + platform.height and self.player.X in range(platform.X ,platform.X + platform.width):
                return True   
    
    def read_data(self):
        with open("sky_up\saver.csv",'r') as csv_file:
            csv_file.seek(0)
            return pd.read_csv(csv_file)
        
    def save_data(self):
        with open("sky_up\saver.csv",'w') as csv_file:  
            if self.high_score: 
                self.player_info_csv.loc[self.player_index, self.GAME_MODE] = self.score
                self.player_info_csv.loc[self.player_index, "achievements"] = "'" + self.achievements + "'"
            df = pd.DataFrame(self.player_info_csv)
            df.to_csv(csv_file,index = False)
                                      
    def keyboard_input(self):
        key = pygame.key.get_pressed()
        
        if key[pygame.K_LEFT]:
            if self.able_to_swap_walls:
                if self.player.X <= 0 :
                    self.player.X = self.screen_width
                    self.passed_wall = True
                else: 
                    self.player.X -= self.player.sides_velocity
            else:
                if self.player.X <= 0 :
                    self.player.X = 0
                else: 
                    self.player.X -= self.player.sides_velocity
        elif key[pygame.K_RIGHT]:
            if self.able_to_swap_walls:
                if self.player.X >= self.screen_width :
                    self.player.X = 0
                    self.passed_wall = True
                else: 
                    self.player.X += self.player.sides_velocity
            else:
                if self.player.X + 30 >= self.screen_width :
                    self.player.X = self.screen_width-30
                else: 
                    self.player.X += self.player.sides_velocity
        elif key[pygame.K_SPACE]:
            self.pause_game()
    
    def display_settings(self):
        settings_gear = GAME_UTIL.image_scale(r'sky_up\IMGS\settings.png',(64,64))
        self.screen.blit(settings_gear,(self.screen_width-80,16))
        mouse_x,mouse_y = pygame.mouse.get_pos()
        #calculez distanta dintre cursor si centrul imaginii de la setari(un pinion[cerc])
        if math.sqrt((mouse_x  - (self.screen_width - 80 + 32))**2 + (mouse_y - 48)**2) <= 32:
            if pygame.mouse.get_pressed()[0]:
                for i in range(0,100):
                    pygame.draw.rect(self.screen,"#aeaeae",(300,0,400,3*i))
                    self.screen.blit(settings_gear,(self.screen_width-80,16))
                    time.sleep(0.01) 
                    pygame.display.update()
                print("apesi pe setari")
                if self.volume < 1 :
                    self.volume += 0.1
            #TODO implementare concept de bara de setari cu animatie 
            
    def player_on_the_groud(self):
        if self.player.Y == self.screen_height - 50:
            self.player.is_landing = True    
    
    def check_platforms_out_of_screen(self):
        for platform in self.platforms:
            if platform.out_of_screen():
                self.platforms.remove(platform)
                #verific ca platforma generata sa nu se miste exact ca cea anterioara pt ca astfel s-ar putea genera un jump 
                #mult prea greu de executat
                if self.platforms_velocity  == 20:
                    pas = 20
                else:
                    pas = 10    
                    
                new_platform_X = random.randrange(300,700,pas)
                #FIXME PORBLEMA CU RANDOMIZAREA
                if new_platform_X in range(self.platforms[-1].X-100,self.platforms[-1].X+100):
                    if self.platforms[-1].dir == 'right':
                        if self.platforms[-1].X <  self.screen_width-250:
                            new_platform_X += 140
                        else:
                            new_platform_X -= 140
                    else:
                        if self.platforms[-1].X < 250:
                            new_platform_X += 140
                        else:
                            new_platform_X -= 140
                
                self.platforms.append(Platform(self.screen,self.screen_width, self.screen_height,self.platforms_img,new_platform_X,
                                               50,self.platforms_length,20,random.choice(["right","left"]),self.platforms_velocity))
    
    def background_mechanics(self):
        if self.background_level == self.screen_height :
            self.background_level = 0
        #print(self.backgrounds)
        if self.score == 83 and self.next_step == 0:
            self.next_step += 1
            self.backgrounds[0] = (GAME_UTIL.image_scale(r"sky_up\IMGS\backgrounds\sky2.jpg",(self.screen_width,self.screen_height)))
 
        elif self.score == 163 and self.next_step == 1:
            self.next_step += 1
            self.backgrounds[1] = GAME_UTIL.image_scale(r"sky_up\IMGS\backgrounds\space2.jpg",(self.screen_width,self.screen_height))

        elif self.score == 243 and self.next_step == 2:
            self.next_step += 1
            self.backgrounds[0] = GAME_UTIL.image_scale(r"sky_up\IMGS\backgrounds\space1.jpg",(self.screen_width,self.screen_height)) 
              
    def game_mode_difficulty(self):
        if self.GAME_MODE == 'easy':
            self.platforms_length = 200
            self.platforms_velocity = 5
            self.music = my_music[0]
        elif self.GAME_MODE == 'normal':
            self.platforms_length = random.choice([100,150])
            self.platforms_velocity = 5
            self.music = my_music[3]
        elif self.GAME_MODE == 'hard':
            self.platforms_length = 100
            self.platforms_velocity = 10 
            self.music = my_music[1]  
        elif self.GAME_MODE == 'insane':
            self.platforms_length = random.choice([160])
            self.platforms_velocity = 20 
            self.music = my_music[1]  
            
        elif self.GAME_MODE == 'chaotic':
            if self.score >= 4:
                self.platforms_velocity = random.choice([2,5,10,20])
            else:
                self.platforms_velocity = random.choice([2,5,10])

            self.platforms_length = random.choice([100,160,200])
            self.music = my_music[2]
        elif self.GAME_MODE == 'wallY':
            self.music = my_music[1]  
            self.able_to_swap_walls = True
            if self.score >= 4:
                self.platforms_length = random.choice([100,150])
                self.platforms_velocity = random.choice([5,5,10])
            else:
                self.platforms_length = 150
                self.platforms_velocity = 5
        elif self.GAME_MODE == 'progressive':
            pass
            #____________________________________ TODO
            #     if score % 200 == 0: 
            #         self.platforms_velocity = 2 
            #     elif (score-20) % 200 == 0: #20 100 150 200 220 300 350 400
            #         self.platforms_velocity = 5
            #     elif score % 150:
            #         self.platforms_velocity = 20 
            #     elif score % 100 == 0:
            #         self.platforms_velocity = 10  
            #_______________________________________ in lucru...
        elif self.GAME_MODE == 'upside-down':
            #TODO de implementat candva .... versiuni viitoare 
            pass
        elif self.GAME_MODE == 'twist-maina':
            pass
            #TODO de implementat candva .... versiuni viitoare      
          
    def check_set_achievement(self,index):
        self.target_index = index
        if self.achievements[index] == "0" and not self.one_target_reached:
            self.one_target_reached = True
            self.achievements_active = True
            self.achievements = self.achievements[:index] +"1"+ self.achievements[index+1:]
            print(f"Ai atins scorul de {self.achievement_targets_dict[index % 5]} pe dificultatea {self.GAME_MODE}")
            self.time_trigger = datetime.datetime.now()
            print(self.achievements)
            
        
    def draw_achievement_box(self):
        pygame.draw.rect(self.screen,"#ff00ff",(self.screen_width//2-150,10 - self.achievement_box_translate,300,60),4,10)
        pygame.draw.rect(self.screen,"#f5deb3",(self.screen_width//2-146,14 - self.achievement_box_translate,292,52),0,5)
        
        GAME_UTIL.show_text(self.screen,f"Congrats! You've reached"
                            ,25,"#242424",self.screen_width//2-105,20 - self.achievement_box_translate)
        
        GAME_UTIL.show_text(self.screen,f"score {self.achievement_targets_dict[self.target_index % 5]} in {self.GAME_MODE} mode"
                            ,25,"#242424",self.screen_width//2-105,40 - self.achievement_box_translate)
        
        pygame.draw.polygon(screen,"#f5deb3",((self.screen_width//2-154,17 - self.achievement_box_translate),
                                               (self.screen_width//2-154,61 - self.achievement_box_translate),
                                               (self.screen_width//2-201,35 - self.achievement_box_translate)))
        
        pygame.draw.polygon(screen,"#f5deb3",((self.screen_width//2+152,17 - self.achievement_box_translate),
                                               (self.screen_width//2+152,61 - self.achievement_box_translate),
                                               (self.screen_width//2+199,35 - self.achievement_box_translate)))
        
        pygame.draw.polygon(screen,"#ff00ff",((self.screen_width//2-153,16 - self.achievement_box_translate),
                                               (self.screen_width//2-153,62 - self.achievement_box_translate),
                                               (self.screen_width//2-203,35 - self.achievement_box_translate)),3)
        
        pygame.draw.polygon(screen,"#ff00ff",((self.screen_width//2+152,16 - self.achievement_box_translate),
                                               (self.screen_width//2+152,62 - self.achievement_box_translate),
                                               (self.screen_width//2+202,35 - self.achievement_box_translate)),3)
        
        
        #coboara cu date time faci acolo sa stea cam 2 secunde si apoi il faci sa 
        #urce inapoi si sa reinitalizezi valorile date
        pass
    
    def move_achievement_box(self):
        time_passed = (datetime.datetime.now() - self.time_trigger).total_seconds()
        if time_passed > 2:
            self.achievements_active = False
            
        if self.achievements_active:
            if self.achievement_box_translate > 0:
                self.achievement_box_translate -= 5 
        else:  
            if self.achievement_box_translate < 150:
                self.achievement_box_translate += 5      
           
    def check_for_achievements(self):
        #FIXME faza de testing ......
        if self.GAME_MODE == 'easy':
            if self.score in range(10,12) :
                self.check_set_achievement(0)
            elif self.score in range(50,52):
                self.check_set_achievement(1)
            elif self.score in range(100,102):
                self.check_set_achievement(2)
            elif self.score in range(250,252):
                self.check_set_achievement(3)
            elif self.score in range(500,502):              
                self.check_set_achievement(4)  
            else: 
                self.one_target_reached = False
                            
        elif self.GAME_MODE == 'normal':
            if self.score in range(10,12):
                self.check_set_achievement(5)
            elif self.score in range(50,52):
                self.check_set_achievement(6)
            elif self.score in range(100,102):
               self.check_set_achievement(7)
            elif self.score in range(250,252):
                self.check_set_achievement(8)
            elif self.score in range(500,502):
                self.check_set_achievement(9)
            else: 
                self.one_target_reached = False
                
        elif self.GAME_MODE == 'hard':
            if self.score in range(10,12):
                self.check_set_achievement(10)
            elif self.score in range(50,52):
                self.check_set_achievement(11)
            elif self.score in range(100,102):
                self.check_set_achievement(12)
            elif self.score in range(250,252):
                self.check_set_achievement(13)
            elif self.score in range(500,502):
                self.check_set_achievement(14)
            else: 
                self.one_target_reached = False
                
        elif self.GAME_MODE == 'insane':
            if self.score in range(10,12):
                self.check_set_achievement(15)
            elif self.score in range(50,52):
                self.check_set_achievement(16)
            elif self.score in range(100,102):
                self.check_set_achievement(17)
            elif self.score in range(250,252):
                self.check_set_achievement(17)
            elif self.score in range(500,502):
                self.check_set_achievement(19)
            else: 
                self.one_target_reached = False
                
        elif self.GAME_MODE == 'chaotic':
            if self.score in range(10,12):
                self.check_set_achievement(20)
            elif self.score in range(50,52):
                self.check_set_achievement(21)
            elif self.score in range(100,102):
                self.check_set_achievement(22)
            elif self.score in range(250,252):
                self.check_set_achievement(23)
            elif self.score in range(500,502):
                self.check_set_achievement(24)
            else: 
                self.one_target_reached = False
                
        elif self.GAME_MODE == 'wallY':
            if self.score in range(10,12):
                self.check_set_achievement(25)
            elif self.score in range(50,52):
                self.check_set_achievement(26)
            elif self.score in range(100,102):
                self.check_set_achievement(27)
            elif self.score in range(250,252):
                self.check_set_achievement(28)
            elif self.score in range(500,502):
                self.check_set_achievement(29)
            else: 
                self.one_target_reached = False
                
        elif self.GAME_MODE == 'progressive':
            #TODO in lucru.....
            pass
        elif self.GAME_MODE == 'upside-down':
            #TODO in lucru.....
            pass
    
    def show_score(self): 
        GAME_UTIL.show_text(self.screen,f"Score: {self.score}", 64, '#ffd700', 10, 10,1,"#ff0000")
        if self.score > int(str(self.player_info_csv.loc[self.player_index, self.GAME_MODE]).split(" ")[4].replace('\nName:',"")):
            GAME_UTIL.show_text(self.screen,"HIGH SCORE", 32, '#fe03d0', 10, 50,1,"#FFC0CB")
            self.high_score = True
            #FIXME bug rezolvat nu chiar 
    
    def reset_game_attributes(self):
        self.high_score = False
        self.player_info_csv = self.read_data()
        pygame.mixer.music.play(-1,start = 0)
        self.next_step = 0
        self.score = 0
        self.platforms = [ ]
        self.platforms_img = rf"sky_up\IMGS\platforms\grass_plat{random.randint(1,2)}.png" 
        self.create_platforms( )
        self.player.X = self.screen_width//2 - 30
        self.background_level = 0  
        self.start_date = datetime.datetime.now()
        self.backgrounds = [GAME_UTIL.image_scale(r"sky_up\IMGS\backgrounds\ground.jpg",(self.screen_width,self.screen_height)),
                            GAME_UTIL.image_scale(r"sky_up\IMGS\backgrounds\sky1.jpg",(self.screen_width,self.screen_height)) ]   
                   
    def is_game_over(self):
        if self.score >= 4 and self.player.Y + 30 >= self.screen_height - 20 :
            self.save_data()    
            buttons = [ ]
            buttons.append(Button(self.screen,230,350,200,40,"#000000","Play Again",32,"#00ff00","#00ff00",0.5,"#ff0000"))
            buttons.append(Button(self.screen,530,350,200,40,"#000000","Main Menu",32,"#00ff00","#00ff00",0.5,"#ff0000"))
            game_over_run = True
            pygame.mixer.music.set_volume(self.volume/5)
            while game_over_run:
                self.game_graphics()
                self.screen.blit(GAME_UTIL.image_scale(r'sky_up\IMGS\transparent.png',(self.screen_width,self.screen_height)),(0,0))
                GAME_UTIL.show_text(self.screen,"Game Over",128,"#000000",230,150,1,"#ff0000")
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over_run = False
                        self.forced_closed = True
                  
                for button in buttons:
                    button.draw()
                    if button.clicked():
                        if button.text == "Main Menu":
                            self.game_is_runnig = False
                            game_over_run = False
                            pygame.mixer.music.stop()
                        elif button.text == "Play Again":
                            
                            game_over_run = False
                            self.save_data()
                            self.reset_game_attributes()
                            print(self.score)
                pygame.display.update()
                clock.tick(60)
               
            # TODO implementare tabele si grafica pt GAME OVER 
            # buton de main menu si buton de play again
    
    def check_player_jump(self,event):
        if event.key == pygame.K_UP:
            if self.player.is_landing:
                self.player.is_landing = False
                for _ in range(0,20):
                    if self.collide_down():
                        self.player.Y -= 10
                        break
                    self.player.Y -= 10
                self.player.fall_velocity = 10
                self.player.sides_velocity = 10
                        
    def game_graphics(self):
        
        self.screen.blit(self.backgrounds[1],(0,-self.screen_height + self.background_level))
        self.screen.blit(self.backgrounds[0],(0,self.background_level))
        
        self.player.draw()
        for platform in self.platforms:
            platform.draw()
        if self.score < 4:
            ground = GAME_UTIL.image_scale(r"sky_up\IMGS\platforms\grass_platform.png",(self.screen_width,20))
            self.screen.blit(ground,(0,self.screen_height-20))
        self.show_score()
        
        if self.one_target_reached:
            self.draw_achievement_box()
 
  
    def game_engine(self):
        pygame.mixer.music.set_volume(self.volume)
        for platform in self.platforms:
            platform.move()
        self.game_mode_difficulty()
        self.player.fall()
        self.keyboard_input()
        self.collide_up()
        self.collide_down()
        self.player_on_the_groud()
        self.check_platforms_out_of_screen()
        self.background_mechanics()         
        self.is_game_over()
        self.set_platform_img()
        self.check_for_achievements()
        if self.one_target_reached:
            self.move_achievement_box()
        self.check_touch_time()
        
    def run_game(self):
        while self.game_is_runnig:
        
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN: 
                    self.check_player_jump(event)
    
                elif event.type == pygame.QUIT :
                    self.save_data()
                    self.game_is_runnig = False
                    return "forced"
            
            if self.forced_closed:
                self.save_data()
                self.game_is_runnig = False
                return "forced"
             
            self.game_graphics()
            self.game_engine()
            
            clock.tick(60)
            pygame.display.update()
        ######################    
        return self.volume
    #########################
WIDTH = 960
HEIGHT = 640
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.init()
pygame.mixer.init()

def sky_up():
    my_sky_up = Game(screen,WIDTH,HEIGHT,"danutz128","#ff00ff","normal",0.1)
    my_sky_up.run_game()

# TODO continua cu main menu si mai adauga fauture-uri la joc (imagini in loc de figuri geometrice) selectare mod de joc interfata etc...
#TODO LAGUIESTE PANA FACI 8 LA SCOR GEN XD 
#FIXME TODO repara bugul cu butonul de on of sound din joc si repara sa se retina highscore ul si daca bagi pauza la joc sau play again!!!
if __name__ == "__main__":
    sky_up()