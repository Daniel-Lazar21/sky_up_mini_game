import pygame
from pygame import mixer
import datetime
my_sounds = [r"sky_up\SOUNDS\click_sound.wav"]

my_music = [r"sky_up\SOUNDS\The Calling.wav",r"sky_up\SOUNDS\Final Battle.wav",
            r"sky_up\SOUNDS\Dry Out.wav",r"sky_up\SOUNDS\Can't Let Go.wav"]

colors = ["#f4f4f4", "#aeaeae", "#ffe4c4", "#9ACD32","#0f03ff","#ff6ec7","#61de2a","#880808",
           "#ffc18c","#0e4a92","#FFA500","#ff00ff","#FFD700","#242424", "#b9f2ff","#7f00ff","#40e0d0"]

my_dict_unlocked_levels = {5 : [0 , "easy" , 10],
                           6 : [5 , "normal" , 10],
                           7 : [10 , "hard" , 10],
                           8 : [15 , "insane" , 10],
                           9 : [20 , "wallY" , 10],
                           10 : [25 , "chaotic" , 10],
                           11 : [1 , "easy" , 50],
                           12 : [6 , "normal" , 50],
                           13 : [11 , "hard" , 50],
                           14 : [16 , "insane" , 50],
                           15 : [21 , "wallY" , 50],
                           16 : [26 , "chaotic" , 50]}

clock = pygame.time.Clock()
class GAME_UTIL():
    def image_scale(img:str , size: tuple):
        scale_img = pygame.image.load(img)
        return pygame.transform.scale(scale_img ,size)

    def show_text(screen,text,size,color,x_pos,y_pos,outline_size = 0,outline_color = "#f4f4f4"):
        myfont = pygame.font.Font(None,size)
        this_text = myfont.render(text,True ,color)
        #daca dau dimensiunea conturului si culoarea le deseneaza !
        if outline_size:
            outline_text = myfont.render(text, True, outline_color)
            # Desenează textul cu contur
            screen.blit(outline_text, (x_pos-outline_size, y_pos-outline_size))
            screen.blit(outline_text, (x_pos+outline_size, y_pos-outline_size))
            screen.blit(outline_text, (x_pos-outline_size, y_pos+outline_size))
            screen.blit(outline_text, (x_pos+outline_size, y_pos+outline_size))
            screen.blit(outline_text, (x_pos-outline_size, y_pos))
            screen.blit(outline_text, (x_pos+outline_size, y_pos))
            screen.blit(outline_text, (x_pos, y_pos+outline_size))
            screen.blit(outline_text, (x_pos, y_pos+outline_size))
        screen.blit(this_text,(x_pos ,y_pos))
    # metoda care ma ajuta sa iau dimensiunile pe care textul meu o sa le aiba in vederea ocuparii unui spatiu specific
    def get_text_size(text,size):
        this_font = pygame.font.Font(None,size)
        return this_font.size(text)   
