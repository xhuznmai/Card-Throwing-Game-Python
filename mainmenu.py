import pygame
import sys
from main import *



def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Main Menu")

#Game Variables
game_paused = False
menu_state = "main"


#Font Define
font = pygame.font.SysFont("arialblack", 30)

#Font Color define
TEXT_COL = ("black")

#button image load
resume_img = pygame.image.load("img/play_button.png").convert_alpha()
option_img = pygame.image.load("img/option_button.png").convert_alpha()
quit_img = pygame.image.load("img/quit_button.png").convert_alpha()
option_menu_img = pygame.image.load("img/background.png")
back_button_img = pygame.image.load("img/back_button.png")
#creat button instances
resume_button = Button(screen_width/2 - resume_img.get_width()/2, 125, resume_img, 1)
option_button = Button(screen_width/2 - option_img.get_width()/2, 125 + resume_img.get_height(), option_img, 1)
quit_button = Button(screen_width/2 - quit_img.get_width()/2, 125 + resume_img.get_height() + option_img.get_height(), quit_img, 1)
back_button = Button(screen_width/2 - back_button_img.get_width()/2, 125, back_button_img, 1)
#Main menu Loop
run = True
while run:
    screen.fill("purple")
    screen.blit(option_menu_img, (0, 0))

    #Check if game is paused
    if game_paused == True:
        #check menu state
        if menu_state == "main":
            #draw menu button
            if resume_button.draw(screen):
                game_paused = False
            if option_button.draw(screen):
                menu_state = "option"
                pygame.display.set_caption("Option")
            if quit_button.draw(screen):
                run = False
        if menu_state == "option":
            #draw option menu
            if back_button.draw(screen):
                menu_state = "main"
    else:
        draw_text("Press ESC to pause", font, TEXT_COL, 0, 0)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Pause")
                game_paused = True

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()

pygame.quit()