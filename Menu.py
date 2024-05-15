from Game import *
from StartScreen import Start_Screen

class MENU():
    level_buttons = [ ]
    character_buttons = [ ]
    select_player_box_buttons = [ ]
    menu_songs = [r"sky_up\SOUNDS\menu1.wav"]
    diff = ['easy','normal','hard','insane','wallY','chaotic','progressive','upside-down']
  
    def __init__(self,screen,screen_width,screen_height) -> None:
        self.csv_data = self.read_data() 
        self.player_name = "No Selection"
        self.player_index = None
        self.achievements = None
        pygame.mixer.music.load(random.choice(self.menu_songs))  # Load the music file
        pygame.mixer.music.play(-1)
        self.menu_is_running = True
        self.screen = screen
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.diff_index = 0
        #butoane pt select level
        self.level_buttons.append(Button(self.screen,380,550,200,30,'#212121',self.diff[self.diff_index],32,"#ff00ff","#FFD700",0.5,"#ff0000"))
        self.level_buttons.append(Button(self.screen,310,550,50,30,'#212121',"<",25,"#ff00ff","#FFD700",0.5,"#ff0000"))
        self.level_buttons.append(Button(self.screen,600,550,50,30,'#212121',">",25,"#ff00ff","#FFD700",0.5,"#ff0000"))
        self.background = GAME_UTIL.image_scale(r"sky_up\IMGS\backgrounds\space1.jpg",(self.screen_width,self.screen_height))
        self.select_message = ""
        #BUTOANE pentru select player color
        self.player_color_index = 0 
        self.player_color_now = colors[self.player_color_index]
        self.character_buttons.append(Button(self.screen,310,350,50,30,'#212121',"<",25,"#ff00ff","#FFD700",0.5,"#ff0000"))
        self.character_buttons.append(Button(self.screen,600,350,50,30,'#212121',">",25,"#ff00ff","#FFD700",0.5,"#ff0000"))
        self.need_to_unlock_color_message = ""
        self.character_buttons.append(Button(self.screen,380,400,200,30,'#212121',"Custom Color",32,"#ff00ff","#FFD700",0.5,"#ff0000"))
        self.custom_color_RGB = None
        self.custom_color_button_triggered = False
        self.custom_color_height_transform = 100
        self.custom_color_button_X = 380# 310
        self.custom_color_button_width = 200# 340
        self.custom_R_bar_X = 255
        self.custom_G_bar_X = 255
        self.custom_B_bar_X = 255
        #Butoanele pentru selectarea volumului WORKING....
        #SETTINGS INSTANCE
        self.SETTINGS = SETTINGS(self.screen,self.screen_height)
        #butonul pentru select player
        #initializari select player
        #FIXME DE fiecare data cand faci o actiune noua trebe sa resetezi si sa initializezi butoanele 
        self.select_player_button = Button(self.screen,20,20,120,30,'#212121',"Select Player",25,"#ff00ff","#FFD700",0.5,"#ff0000")
        self.select_player_triggered = False
        self.select_player_translate = 290 
        self.edit_delete_buttons_trigger = False
        self.button_select_this = None
        self.button_delete_this = None
        self.last_button_pressed = 2
        self.selected_player = ""
        self.input_triggered =  False
        self.input_rect = None
        self.input_focused = False
        self.input_string = ""
        self.receive_input_type_mesasge = "Hit Enter to submit!"
        self.receive_input_type_mesasge_X_pos = 72
        self.initialize_dataframe_and_select_players()
        self.check_best_score_or_not_implemented()
        #self.volume_buttons.append(Button(self.screen,600,410,50,30,'#212121',">",25,"#ff00ff","#FFD700",0.5,"#ff0000"))
        #TODO o sa cam terbuiasca clasa pentru faza cu setarile ca is la fel si in joc si in meniu gen...
        #faza cu bara unde sa vad toate achievements
        self.achievements_button_triggered  = False
        self.achievements_translate = self.screen_height 
        self.achievements_loaded = False
        self.achievements_button = Button(self.screen,430,20,130,30,'#212121',"Achievements",25,"#ff00ff","#FFD700",0.5,"#ff0000")   
        GAME_UTIL.show_text(self.screen,f"No selection",40,"#00ff00", 720,90,2,"#000000")
        self.selected_difficulty = ""
        #fa sa fie bara aia cu insert la text ca faci cu split insert si join
        
    def read_data(self):
        return pd.read_csv(r"sky_up\saver.csv")
    
    def save_data(self):
        self.csv_data.to_csv("sky_up\saver.csv", index=False)
        
    def draw_select_player(self):
        
        #aici faci faza aia cu selectatul player-ului sau sa creeze unul sau sa il stearega pe unul BAFTA
        pygame.draw.rect(self.screen,"#F5DEB3",(0-self.select_player_translate +5,5,280,self.screen_height-10),border_radius = 20)
        pygame.draw.rect(self.screen,"#212121",(0-self.select_player_translate ,0,290,self.screen_height),width = 10,border_radius = 20)
        for button in self.select_player_box_buttons:
            button.draw()
            

        #GAME_UTIL.show_text(self.screen,f"Select Player",40,"#00ff00",self.select_player_translate  + 672,20,2,"#000000")
        
    def initialize_dataframe_and_select_players(self):
        for index,name in enumerate(self.csv_data['name']):
            self.select_player_box_buttons.append(Button(self.screen,0-self.select_player_translate-60,100 + 70*(index+1),130,
                                                         50,'#212121',name,32,"#ff00ff","#FFD700",0.5,"#ff0000"))
        for index in range(len(self.select_player_box_buttons),5):
            self.select_player_box_buttons.append(Button(self.screen,0-self.select_player_translate-60,100 + 70*(index+1),130,
                                                        50,'#212121',"+ add +",32,"#ff00ff","#FFD700",0.5,"#ff0000"))
            
    def check_select_player_buttons_from_select_box(self):
        for button in self.select_player_box_buttons:
            if button.clicked():

                self.SETTINGS.play_sfx_sound()
                if button.text != "+ add +":
                     
                    self.selected_player = button.text
                    self.button_select_this = Button(self.screen,button.X+145,button.Y-12.5,70,
                                                        30,'#212121',"Select",20,"#ff00ff","#FFD700",0.3,"#ff0000")
                    self.button_delete_this = Button(self.screen,button.X+145,button.Y+37.5,70,
                                                        30,'#212121',"Delete",20,"#ff00ff","#FFD700",0.3,"#ff0000")
                    if self.last_button_pressed == button:
                        
                        self.edit_delete_buttons_trigger = not self.edit_delete_buttons_trigger
                    else:
                        self.edit_delete_buttons_trigger = True 
                    self.input_triggered =  False    
                    self.input_string = "" 
                else:
                    self.edit_delete_buttons_trigger = False 
                    self.input_focused =  True
                    if self.last_button_pressed == button:
                        
                       self.input_triggered = not self.input_triggered
                    else:
                        self.input_triggered =  True

                self.last_button_pressed = button
    #GETTING INPUT FROM THE USER           
    def draw_get_input_form_user_box(self):
        color = "#ff00ff" if self.input_focused else "#f4f4f4"
        #iau stringul si ii dau split apoi iau pozitia la care se afla bara de selectare si exact acolo 
        #inserez caracterul bara "|" apoi dau join inapoi la srting
        self.input_string = self.input_string.replace("|","")
        self.input_string += "|"

        #incearca in input sa te misti cu sagetile in text
        GAME_UTIL.show_text(self.screen,"Enter a nickname",32,"#212121",57,65,0.5,"#ff00ff")
        pygame.draw.rect(self.screen,"#242424",(78,88,144,34),border_radius = 20)
        pygame.draw.rect(self.screen,color,(80,90,140,30),2,20)
        GAME_UTIL.show_text(self.screen,self.input_string ,25,"#f4f4f4",90,97)
        GAME_UTIL.show_text(self.screen,self.receive_input_type_mesasge,25,"#212121",
                            self.receive_input_type_mesasge_X_pos,125,0.5,"#ff00ff")
       
    def write_and_get_input_form_user_box(self):
        input_box_rect = pygame.Rect(80,90,140,30)
        mouse_X,mouse_Y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if input_box_rect.collidepoint(mouse_X,mouse_Y):
                time.sleep(0.2)
                self.SETTINGS.play_sfx_sound()
                self.input_focused = not self.input_focused
                
                #TODO poti sa mai lucrezi o idee la inputuri!!
            else:
                self.input_focused = False
    
    def draw_select_and_delete_buttons(self):
        if self.edit_delete_buttons_trigger:
            pygame.draw.line(self.screen, "#ff00ff", (self.last_button_pressed.X+self.last_button_pressed.width-5,self.last_button_pressed.Y),
                             (self.button_select_this.X,self.button_select_this.Y+10), 5)
            pygame.draw.line(self.screen, "#ff00ff",(self.last_button_pressed.X+self.last_button_pressed.width-5,
                                                     self.last_button_pressed.Y+self.last_button_pressed.height-1) , 
                             (self.button_delete_this.X,self.button_delete_this.Y+10), 5)
            self.button_select_this.draw()
            self.button_delete_this.draw()
                        
    def check_press_select_delete_buttons(self):
        if self.button_select_this and self.button_select_this.clicked():
            self.SETTINGS.play_sfx_sound()
            self.player_name = self.selected_player
            self.player_index = self.csv_data.index[self.csv_data['name'] == self.player_name]
            self.achievements = self.achievements = str(self.csv_data.loc[self.player_index, "achievements"]
                                                         ).split(" ")[4].replace('\nName:',"").replace("'","")
            self.check_if_color_unlocked()
            self.edit_delete_buttons_trigger = False        
  

        if  self.button_delete_this and self.button_delete_this.clicked():
            self.SETTINGS.play_sfx_sound()
            self.csv_data = self.csv_data.drop(self.csv_data[self.csv_data['name'] == self.selected_player].index)
            self.update_players_in_real_time()
            if self.last_button_pressed.text == self.player_name :
                self.player_name = "No Selection"
            self.edit_delete_buttons_trigger = False

    def update_players_in_real_time(self):
        self.save_data()
        self.select_player_box_buttons = [ ]
        self.initialize_dataframe_and_select_players()
        for button in self.select_player_box_buttons:
            button.X += 90       
               
    def check_best_score_or_not_implemented(self):
        if self.level_buttons[0].text in self.diff[-2:]:
            self.select_message = "COMING SOON..."
        else:
            if self.player_name != "No Selection":
                player_index = self.csv_data.index[self.csv_data['name'] == self.player_name]
                best_score_for_selected_difficulty = str(self.csv_data.loc[player_index, self.level_buttons[0].text]).split(" ")[4].replace('\nName:',"")
                
                self.select_message = f"BEST SCORE: {best_score_for_selected_difficulty}" 
            else:
                self.select_message = ""    
    
    def draw_select_character_color_buttons_and_character(self):    
        for button in self.character_buttons:
            button.draw()                
        self.check_player_color_now()
   
        pygame.draw.rect(self.screen,self.player_color_now,(457,342,46,46),border_radius = 10)
        pygame.draw.rect(self.screen,"#505050",(455,340,50,50),border_radius = 10,width = 3)
        GAME_UTIL.show_text(self.screen,self.player_name,40,"#00ff00", 450-len(self.player_name)*5,300,2,"#000000")
        if self.need_to_unlock_color_message:
            self.screen.blit(GAME_UTIL.image_scale(r"sky_up\IMGS\transparent.png",(45,45)),(457.5,342.5))
            self.screen.blit(GAME_UTIL.image_scale(r"sky_up\IMGS\locker.png",(25,25)),(467,350))
            GAME_UTIL.show_text(self.screen,self.need_to_unlock_color_message,20,"#ff0000", 380 - len(self.need_to_unlock_color_message)//2,395,2,"#000000")
            self.character_buttons[2].Y = 420
        else:
            self.character_buttons[2].Y = 400
            #fa ca butonu ala de custom sa fie mai sus daca ai mesaj fa-l mai jos    
        
    def draw_select_level_buttons(self):
        GAME_UTIL.show_text(screen,self.select_message,28,"#f4f4f4",
                            405,590,1,"#ff0000")
        for button in self.level_buttons:
            button.draw()
        
    def check_player_color_now(self):
        if self.custom_color_button_triggered:
            self.player_color_now = self.custom_color_RGB
        else:
            self.player_color_now = colors[self.player_color_index]        
                
    def check_level_buttons(self):
        for button in self.level_buttons:
            self.check_best_score_or_not_implemented()      
            if button.clicked():
                self.SETTINGS.play_sfx_sound()
                if button.text == "<":
                    if self.diff_index == 0:
                        self.level_buttons[0].text = self.diff[-1]
                        self.diff_index = len(self.diff)-1
                        
                    else:
                        self.level_buttons[0].text = self.diff[self.diff_index - 1]
                        self.diff_index -= 1
                            
                elif button.text == ">":
                    if self.diff_index == len(self.diff)-1:
                        self.level_buttons[0].text = self.diff[0]
                        self.diff_index = 0
                        
                    else:
                        self.level_buttons[0].text = self.diff[self.diff_index + 1]
                        self.diff_index += 1 
                     
                #==================================================#   
                #Aicin se face instantierea jocului in functie de ce mod de joc am ales 
                elif button.text not in self.diff[-2:] and not self.achievements_button_triggered:

                    if self.player_name != "No Selection" and not self.need_to_unlock_color_message:
                        if self.custom_color_button_triggered:
                            if self.achievements[13]!= "0":
                                self.select_player_triggered = False
                                self.settings_triggered = False 
                                self.selected_difficulty = button.text
                        else:
                            self.select_player_triggered = False
                            self.settings_triggered = False 
                            self.selected_difficulty = button.text
                            
                    else: 
                        #TODO impelmentare mesaj no player selected!
                        pass
                #==================================================#
    #INITIALIZAREA DE BAZA A JOCULUI
    def initialize_game_update_reset(self):

        if self.selected_difficulty != "":
            if self.SETTINGS.settings_translate + self.select_player_translate == 580:
                ## Main Game will run here !###
                new_game = Game(screen,WIDTH,HEIGHT,self.player_name,self.player_color_now,
                                self.selected_difficulty,self.SETTINGS.volume)
                response = new_game.run_game()
                #############################
                pygame.mixer.music.load(random.choice(self.menu_songs))
                pygame.mixer.music.play(-1)
                self.selected_difficulty = ""
                self.csv_data = self.read_data()
                self.player_index = self.csv_data.index[self.csv_data['name'] == self.player_name]
                self.achievements = self.achievements = str(self.csv_data.loc[self.player_index, "achievements"]
                                                         ).split(" ")[4].replace('\nName:',"").replace("'","") 
 
                if response == "forced":
                    self.menu_is_running = False
                else:
                    self.SETTINGS.volume = response
                    self.SETTINGS.index_volume = int((response/0.01)/5 - 1) + 1
    
    def check_if_color_unlocked(self):
        if self.player_color_index > 4 and self.player_name != "No Selection":
            goal_to_check = my_dict_unlocked_levels[self.player_color_index] 

            if self.achievements[goal_to_check[0]] == "0" :
                self.need_to_unlock_color_message = f"Reach {goal_to_check[2]} in {goal_to_check[1]} mode to unlock!"
            else:
               self.need_to_unlock_color_message = "" 
        else:     
            self.need_to_unlock_color_message = ""
                
    def check_character_buttons(self):
        for button in self.character_buttons:
            if button.clicked():
                self.SETTINGS.play_sfx_sound()
                if button.text == "<" and not self.custom_color_button_triggered:
                    if self.player_color_index == 0:
                        self.player_color_index = len(colors) - 1         
                    else:
                        self.player_color_index -= 1

                elif button.text == ">" and not self.custom_color_button_triggered:
                    if self.player_color_index == len(colors) - 1:
                        self.player_color_index = 0
                    else:
                        self.player_color_index += 1 
                elif button.text == "Custom Color" and self.player_name != "No Selection":

                    self.custom_color_button_triggered = not self.custom_color_button_triggered

                        
                self.check_if_color_unlocked()
    
    def custom_color_box_grow(self):
        if self.custom_color_button_triggered:
            self.player_color_index = 0
            
            self.check_if_color_unlocked()
            if self.custom_color_height_transform > 0:
                self.custom_color_height_transform -= 10
                if self.custom_color_button_X > 310 and self.custom_color_button_width < 340:
                    self.custom_color_button_X -= 7
                    self.custom_color_button_width += 14
        else:
               
            if self.custom_color_height_transform < 100:
                self.custom_color_height_transform += 10 
                if self.custom_color_button_X < 380 and self.custom_color_button_width > 200:
                    self.custom_color_button_X += 7
                    self.custom_color_button_width -= 14  
                
    def check_custom_color_height_transform_draw(self):   
        if self.custom_color_height_transform < 90:
            
            pygame.draw.rect(self.screen,"#242424",(self.custom_color_button_X,self.character_buttons[2].Y + self.character_buttons[2].height + 10,
                                                    self.custom_color_button_width,100 - self.custom_color_height_transform),border_radius=10)
            
            pygame.draw.rect(self.screen,"#f4f4f4",(self.custom_color_button_X,self.character_buttons[2].Y + self.character_buttons[2].height + 10,
                                                    self.custom_color_button_width,100 - self.custom_color_height_transform),border_radius=10,width=3)
            #mai intai verifica in timp real daca el cumva nu are deja utilizatorul sa nu poata pune acelasi nume la 
            #"conturi multiple"
            #TODO fa chestia cu click and drag la culori rgb
            if self.custom_color_height_transform < 60:
                pygame.draw.rect(self.screen,"#f4f4f4",(self.custom_color_button_X+35,self.character_buttons[2].Y + self.character_buttons[2].height + 30,
                                    self.custom_color_button_width - 80,10),2) 
                pygame.draw.line(self.screen,"#ff0000",(self.custom_R_bar_X+347,self.character_buttons[2].Y + self.character_buttons[2].height + 25),
                                 (self.custom_R_bar_X+347,self.character_buttons[2].Y + self.character_buttons[2].height + 45),2)
                GAME_UTIL.show_text(self.screen,"R",25,"#ff0000",self.custom_color_button_X+15,self.character_buttons[2].Y + self.character_buttons[2].height + 25,
                                    2,"#000000")
                if self.custom_color_height_transform < 40:
                    pygame.draw.rect(self.screen,"#f4f4f4",(self.custom_color_button_X+35,self.character_buttons[2].Y + self.character_buttons[2].height + 55,
                                    self.custom_color_button_width -80,10),2)
                    pygame.draw.line(self.screen,"#00ff00",(self.custom_G_bar_X+347,self.character_buttons[2].Y + self.character_buttons[2].height + 50),
                                 (self.custom_G_bar_X+347,self.character_buttons[2].Y + self.character_buttons[2].height + 70),2)  
                    GAME_UTIL.show_text(self.screen,"G",25,"#00ff00",self.custom_color_button_X+15,self.character_buttons[2].Y + self.character_buttons[2].height + 50,
                                    2,"#000000")
                    if self.custom_color_height_transform < 20:
                        pygame.draw.rect(self.screen,"#f4f4f4",(self.custom_color_button_X+35,self.character_buttons[2].Y + self.character_buttons[2].height + 80,
                                    self.custom_color_button_width -80,10),2)    
                        pygame.draw.line(self.screen,"#0000ff",(self.custom_B_bar_X+347,self.character_buttons[2].Y + self.character_buttons[2].height + 75),
                                 (self.custom_B_bar_X+347,self.character_buttons[2].Y + self.character_buttons[2].height + 95),2)  
                        GAME_UTIL.show_text(self.screen,"B",25,"#0000ff",self.custom_color_button_X+15,self.character_buttons[2].Y + self.character_buttons[2].height + 75,
                                    2,"#000000")
                        if self.achievements[13] == "0":
                            locked_img = GAME_UTIL.image_scale(r"sky_up\IMGS\transparent.png",(self.custom_color_button_width,100-self.custom_color_height_transform))
                            locked_lock = GAME_UTIL.image_scale(r"sky_up\IMGS\locker.png",(self.custom_color_button_width//5,(100-self.custom_color_height_transform)//2))
                            self.screen.blit(locked_img,(self.custom_color_button_X,self.character_buttons[2].Y + self.character_buttons[2].height + 10))
                            self.screen.blit(locked_lock,(self.custom_color_button_X+ 135,self.character_buttons[2].Y + self.character_buttons[2].height + 20))
                            GAME_UTIL.show_text(self.screen,"Reach 250 in hard mode to unlock",25,"#ff0000",self.custom_color_button_X+35,
                                                self.character_buttons[2].Y + self.character_buttons[2].height + 80,2,"#000000")
        else:               
            pygame.draw.rect(self.screen,"#242424",(380,self.character_buttons[2].Y + self.character_buttons[2].height + 10,
                                                    200,4),border_radius=10)
            
            pygame.draw.rect(self.screen,"#f4f4f4",(380,self.character_buttons[2].Y + self.character_buttons[2].height + 10,
                                                    200,4),border_radius=10,width=2)
    
    def check_move_and_set_custom_rgb_values(self):
        if self.achievements[13] != "0":
            R_rect = pygame.Rect(self.custom_color_button_X+37,self.character_buttons[2].Y + self.character_buttons[2].height + 30,
                                self.custom_color_button_width -84,10)
            G_rect = pygame.Rect(self.custom_color_button_X+37,self.character_buttons[2].Y + self.character_buttons[2].height + 55,
                                self.custom_color_button_width -84,10)
            B_rect = pygame.Rect(self.custom_color_button_X+37,self.character_buttons[2].Y + self.character_buttons[2].height + 80,
                                self.custom_color_button_width -84,10)
            mouse_X,mouse_Y = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if R_rect.collidepoint(mouse_X,mouse_Y):
                    self.custom_R_bar_X = mouse_X-347
                if G_rect.collidepoint(mouse_X,mouse_Y):
                    self.custom_G_bar_X = mouse_X-347
                if B_rect.collidepoint(mouse_X,mouse_Y):
                    self.custom_B_bar_X = mouse_X-347
                
        self.custom_color_RGB = (self.custom_R_bar_X ,self.custom_G_bar_X,self.custom_B_bar_X)                

    def check_select_player_button(self):
        if self.select_player_button.clicked() :
            self.SETTINGS.play_sfx_sound()
            self.select_player_triggered = not self.select_player_triggered 
    
    def check_if_select_player_button_triggered(self):
        if self.select_player_triggered:
            self.check_select_player_buttons_from_select_box()
            if self.edit_delete_buttons_trigger:
                self.check_press_select_delete_buttons()         
        else:
            self.edit_delete_buttons_trigger = False
            self.input_triggered = False  
            self.input_focused = False  
            self.input_string = ''
    
    def check_achievements_button(self):
        if self.achievements_button.clicked():
            self.SETTINGS.play_sfx_sound()
            self.achievements_button_triggered = not self.achievements_button_triggered 
              
    def move_button_select_player(self):
        if self.select_player_triggered:
            if self.select_player_translate > 0:
                self.select_player_translate -= 29
                self.select_player_button.X += 6.9
                for button in self.select_player_box_buttons:
                    button.X += 38
                
        else:
            if self.select_player_translate < 290:
                self.select_player_translate += 29  
                self.select_player_button.X -= 6.9
                for button in self.select_player_box_buttons:
                    button.X -= 38
                         
    def move_achievements_show_box(self):
        if self.achievements_button_triggered:
            self.select_player_triggered = False
            self.SETTINGS.settings_triggered = False
            self.custom_color_button_triggered = False
            if self.achievements_translate > 0:
                self.achievements_translate -= 40
                self.achievements_button.Y += 34
    
        else:
            if self.achievements_translate < self.screen_height:
                self.achievements_translate += 40  
                self.achievements_button.Y -= 34
        if self.achievements_translate == self.screen_height:
            self.achievements_loaded = False
        elif self.achievements_translate == 0:   
            self.achievements_loaded = True   
                      
    def draw_achievements_show_box(self):
        pygame.draw.rect(self.screen,"#F5DEB3",(20,20 - self.achievements_translate ,
                                                self.screen_width-40,self.screen_height-40),border_radius = 20)
        pygame.draw.rect(self.screen,"#212121",(15 ,15-self.achievements_translate ,
                                                self.screen_width-30,self.screen_height-30),width = 10,border_radius = 20)

    def check_if_achievements_not_loaded_draw(self):
        if not self.achievements_loaded:      
            self.SETTINGS.settings_button.draw()
            
            self.select_player_button.draw()
    
    def check_if_achievements_not_loaded_control(self):
        if not self.achievements_loaded:
            
            self.check_level_buttons()
            self.check_character_buttons()
            self.check_select_player_button()
            self.SETTINGS.check_settings_button()
    
    def check_if_name_already_exists(self):
        for name in self.csv_data["name"]:
            
            if name == self.input_string.replace(" ","").replace("|",""):
                self.receive_input_type_mesasge = "This user already exists!"
                self.receive_input_type_mesasge_X_pos = 50
                return 
            else:
                self.receive_input_type_mesasge = "Hit Enter to submit!"
                self.receive_input_type_mesasge_X_pos = 72
                             
    #INPUT DE LA TASTATURA PT A CREA UN NOU USER           
    def keyboard_input_create_name(self,event):
        # Adaugă caracterele tastate la textul căsuței de input
        if event.key == pygame.K_SPACE and len(self.input_string) < 10:
            self.input_string += ' '
        elif event.key == pygame.K_BACKSPACE :
            self.input_string = self.input_string[:-2]
            self.check_if_name_already_exists()
        elif event.key == pygame.K_KP_ENTER:
            if self.receive_input_type_mesasge == "Hit Enter to submit!":
                if self.input_string.replace(" ","") != "|":
                    self.input_string = self.input_string[:-1]
                    self.create_new_player()
                else:
                    self.receive_input_type_mesasge = "Please insert something!"
                    self.receive_input_type_mesasge_X_pos = 50
        elif len(self.input_string) < 10:
            self.input_string += event.unicode   
            self.check_if_name_already_exists()
            print(self.input_string)   
            
    def create_new_player(self):
        new_player = {'name': self.input_string.replace(" ",""),
                      'easy': 0,
                      'normal': 0,
                      'hard': 0,
                      'insane': 0,
                      'chaotic': 0,
                      'wallY': 0,
                      'achievements':"'00000000000000000000000000000000000'"}
        
        self.csv_data = self.csv_data._append(new_player,ignore_index = True)
        self.input_string = ''
        self.input_triggered = False
        self.update_players_in_real_time()
             
    def menu_graphics(self):
        
        self.draw_select_level_buttons()
        self.draw_select_character_color_buttons_and_character()    
        self.draw_select_player()
        self.SETTINGS.draw() 
        self.check_if_achievements_not_loaded_draw() 
        self.draw_select_and_delete_buttons() 
        self.check_custom_color_height_transform_draw()
        if self.input_triggered:
            self.draw_get_input_form_user_box()  
        self.draw_achievements_show_box()
        self.achievements_button.draw()
                  
    def menu_engine(self):
        pygame.mixer.music.set_volume(self.SETTINGS.volume)
        self.check_if_achievements_not_loaded_control()      
        self.SETTINGS.move_button_settings()
        self.move_button_select_player()    
        self.check_achievements_button()
        self.move_achievements_show_box()
        self.SETTINGS.sliders_slide()
        if self.SETTINGS.settings_triggered:
            self.SETTINGS.volume_control() 
        self.check_if_select_player_button_triggered()            
        if self.input_triggered:
            self.write_and_get_input_form_user_box()
        if self.custom_color_button_triggered:
            self.check_move_and_set_custom_rgb_values()
        
        self.custom_color_box_grow()
        self.initialize_game_update_reset()
            
    def run_menu(self):
        entry_screen = Start_Screen(self.screen,self.screen_width,self.screen_height)
        close_response = entry_screen.start_screen_run()
        if close_response == "forced":
            self.menu_is_running = False
        frame_index = 0 
        while self.menu_is_running:
            self.screen.blit(Start_Screen.frames[frame_index], (0, 0))
            frame_index = (frame_index + 1) % len(Start_Screen.frames)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu_is_running = False
                if self.input_focused:    
                    if event.type == pygame.KEYDOWN:
                        self.keyboard_input_create_name(event)
                            
            self.menu_graphics()
            self.menu_engine()
            clock.tick(120)
            pygame.display.update()
            # TODO implementarea meniului de baza si posibil si o mini baza de bate pe csv
            #TODO baga sa faci volum controlabil si in timpul jocului sa poti sa faci ceva setari...

WIDTH = 960
HEIGHT = 640
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Sky up")

def main_menu():
    my_menu = MENU(screen,WIDTH,HEIGHT)

    my_menu.run_menu()
  
if __name__ == "__main__":
    main_menu()
    