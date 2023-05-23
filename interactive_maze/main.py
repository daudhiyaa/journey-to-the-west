import pygame
import button
from musics import *

# Reference
# https://youtu.be/JtiK0DOeI4A

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load(JETPACK_JOYRIDE)
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

# game variables
game_main = False
menu_state = "main"

# define colours
TEXT_COL = (0, 0, 0)

# load images
# background
startup_img = pygame.image.load("assets/img/startup_img.png")
guidepage_img = pygame.image.load("assets/img/guide_page.png")
main_img = pygame.image.load("assets/img/main_img.png")
modepage_img = pygame.image.load("assets/img/mode_page.png")
# main menu
start_img = pygame.image.load("assets/img/start_img.png")
guide_img = pygame.image.load("assets/img/guide_img.png")
exit_img = pygame.image.load("assets/img/exit_img.png")
back_img = pygame.image.load("assets/img/back_img.png")
# mode menu
easy_mode = pygame.image.load("assets/img/easy_mode.png")
medium_mode = pygame.image.load("assets/img/medium_mode.png")
hard_mode = pygame.image.load("assets/img/hard_mode.png")
random_mode = pygame.image.load("assets/img/random_mode.png")
custom_mode = pygame.image.load("assets/img/custom_mode.png")

# create button instances
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


# game loop
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
                # import algo_bfs  # Import the algo.py program here
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

    # event handler
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
