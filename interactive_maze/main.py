import pygame
import button
from musics import *
from images import *

# Reference
# https://youtu.be/JtiK0DOeI4A

# PYGAME INITIALIZATION
pygame.init()
pygame.mixer.init()

# LOAD MUSIC
pygame.mixer.music.load(JETPACK_JOYRIDE)
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.5)

# GAME WINDOW SIZE
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# CREATE GAME WINDOW
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

# GAME VARIABLES
game_main = False
menu_state = "main"

# BUTTON INSTANCES
# main menu
start_button = button.Button(260, 240, start_img, 0.525)
guide_button = button.Button(260, 340, guide_img, 0.525)
exit_button = button.Button(260, 440, exit_img, 0.525)
back_button = button.Button(312, 468, back_img, 0.3)
# mode menu
easy_button = button.Button(100, 240, easy_mode, 0.45)
medium_button = button.Button(100, 340, medium_mode, 0.45)
hard_button = button.Button(100, 440, hard_mode, 0.45)
random_button = button.Button(400, 240, random_mode, 0.45)
custom_button = button.Button(400, 340, custom_mode, 0.45)
backfrommode_button = button.Button(400, 440, back_img, 0.45)

# GAME LOOP
run = True
while run:
    # background color
    screen.blit(startup_img, (0, 0))

    if game_main == True:
        screen.blit(main_img, (0, 0))
        # check menu state
        if menu_state == "main":
            # draw start screen buttons
            if start_button.draw(screen):
                menu_state = "mode"
            if guide_button.draw(screen):
                menu_state = "guide"
            if exit_button.draw(screen):
                run = False

        # check if the guide menu is open
        if menu_state == "guide":
            screen.blit(guidepage_img, (0, 0))
            if back_button.draw(screen):
                menu_state = "main"

        # check if the mode menu is open
        if menu_state == "mode":
            screen.blit(modepage_img, (0, 0))
            if easy_button.draw(screen):
                import easy_mode
            if medium_button.draw(screen):
                import medium_mode
            if hard_button.draw(screen):
                import hard_mode
            if random_button.draw(screen):
                import random_mode
            if custom_button.draw(screen):
                import custom_mode
            if backfrommode_button.draw(screen):
                menu_state = "main"

    # EVENT HANDLER
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            game_main = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the start_button is clicked
                if start_button.is_clicked(event.pos):
                    menu_state = "mode"
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
