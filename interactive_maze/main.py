import pygame
import button

pygame.init()

#create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

#game variables
game_main = False
menu_state = "main"

#define fonts
header_font = pygame.font.Font("assets/fraunces_semibolditalic.ttf", 65)
text_font = pygame.font.Font("assets/fraunces_regular.ttf", 40)


#define colours
TEXT_COL = (0, 0, 0)

#load button images
start_img = pygame.image.load("assets/start_img.png").convert_alpha()
guide_img = pygame.image.load("assets/guide_img.png").convert_alpha()
exit_img = pygame.image.load("assets/exit_img.png").convert_alpha()
back_img = pygame.image.load("assets/back_img.png").convert_alpha()
guidepage_img = pygame.image.load("assets/guide_page.png").convert_alpha()
bg = pygame.image.load("assets/bg.png").convert_alpha()

#create button instances
start_button = button.Button(125, 190, start_img, 0.525)
guide_button = button.Button(435, 190, guide_img, 0.525)
exit_button = button.Button(300, 350, exit_img, 0.5)
back_button = button.Button(340, 500, back_img, 0.2)


def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#game loop
run = True
while run:

  #background color
  screen.blit(bg, (0, 0))

  if game_main == True:
    #check menu state
    if menu_state == "main":
      draw_text("TREASURE HUNT", header_font, TEXT_COL, 135, 85)
      #draw start screen buttons
      if start_button.draw(screen):
        import algo  # Import the astar.py program here
      if guide_button.draw(screen):
        menu_state = "guide"
      if exit_button.draw(screen):
        run = False

    #check if the guide menu is open
    if menu_state == "guide":
       screen.blit(guidepage_img, (0, 0))
       if back_button.draw(screen):
         menu_state = "main"
  else:
    draw_text("TREASURE HUNT", header_font, TEXT_COL, 135, 220)
    draw_text("Press ANY key", text_font, TEXT_COL, 275, 290)


  #event handler
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      game_main = True
      if event.type == pygame.MOUSEBUTTONDOWN:
        if start_button.is_clicked(event.pos):  # Check if the start_button is clicked
            import algo  # Import the algo.py program here
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

pygame.quit()
