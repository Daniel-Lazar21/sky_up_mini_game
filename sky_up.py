import pygame
from Menu import MENU
from Game import Game

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Sky up")

WIDTH = 960
HEIGHT = 640
screen = pygame.display.set_mode((WIDTH,HEIGHT))


def sky_up():
    my_sky_up = Game(screen,WIDTH,HEIGHT,"alex12","normal")
    my_sky_up.run_game()

def main_menu():
    my_menu = MENU(screen,WIDTH,HEIGHT)
    my_menu.run_menu()
  
# TODO continua cu main menu si mai adauga fauture-uri la joc (imagini in loc de figuri geometrice) selectare mod de joc interfata etc...
if __name__ == "__main__":
    main_menu()

# TODO mai trebuie mult si bine de lucrat la meniu ca sa arate ok si ca atunci cnd tu apesi pe butonul d eplay as ti zica select
# difficulty si cand tii hover pe buton sa ti zica si detalliile modului de joc 
# ar trebui pe meniu adaugata imagine de fundal si ceva sunet clasic de meniu 
# apoi sa nu uitam de setari si sa nu uitam de posibilitatea de a selecta caracterul tau 
# adauga sunete si la nivele 
# adauga sunet cand sari si cand mori la fel 
#ar tebui in jocul de baza adaugati asterozi care in coliziune cu player ul sa i scada din viata(bara de viata) 
# si daca e lovit de 3 ori sa moara
