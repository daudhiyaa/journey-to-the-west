import pygame.image as img
import pygame.transform as transform

DOT_SIZE = 0.3
BANANA_SIZE = 0.6
OTHER_SIZE = 0.7

WIDTH = 800

# EASY_MODE
ROWS_EASY = 15
gap_easy = WIDTH // ROWS_EASY

COIN_LIMIT_EASY = 15
MONSTER_LIMIT_EASY = 15

IMAGES_EASY = {
  'dot_img' : transform.scale(img.load("assets/img/dot_img.png"), (gap_easy * DOT_SIZE, gap_easy * DOT_SIZE)),
  'banana_coin' : transform.scale(img.load("assets/img/banana_coin.png"), (int(gap_easy * BANANA_SIZE), int(gap_easy * BANANA_SIZE))),
  'barrier_img' : transform.scale(img.load("assets/img/brick_barrier.png"), (gap_easy, gap_easy)),
  'monkey_start' : transform.scale(img.load("assets/img/monkey_start.png"), (int(gap_easy * OTHER_SIZE), int(gap_easy * OTHER_SIZE))),
  'book_end' : transform.scale(img.load("assets/img/book_end.png"), (int(gap_easy * OTHER_SIZE), int(gap_easy * OTHER_SIZE))),
  'monster' : transform.scale(img.load("assets/img/monster.png"), (int(gap_easy * OTHER_SIZE), int(gap_easy * OTHER_SIZE))),
}

# MEDIUM_MODE
ROWS_MEDIUM = 30
gap_medium = WIDTH // ROWS_MEDIUM

COIN_LIMIT_MEDIUM = 30
MONSTER_LIMIT_MEDIUM = 30

IMAGES_MEDIUM = {
  'dot_img' : transform.scale(img.load("assets/img/dot_img.png"), (gap_medium * DOT_SIZE, gap_medium * DOT_SIZE)),
  'banana_coin' : transform.scale(img.load("assets/img/banana_coin.png"), (int(gap_medium * BANANA_SIZE), int(gap_medium * BANANA_SIZE))),
  'barrier_img' : transform.scale(img.load("assets/img/brick_barrier.png"), (gap_medium, gap_medium)),
  'monkey_start' : transform.scale(img.load("assets/img/monkey_start.png"), (int(gap_medium * OTHER_SIZE), int(gap_medium * OTHER_SIZE))),
  'book_end' : transform.scale(img.load("assets/img/book_end.png"), (int(gap_medium * OTHER_SIZE), int(gap_medium * OTHER_SIZE))),
  'monster' : transform.scale(img.load("assets/img/monster.png"), (int(gap_medium * OTHER_SIZE), int(gap_medium * OTHER_SIZE))),
}

# HARD_MODE
ROWS_HARD = 50
gap_hard = WIDTH // ROWS_HARD

COIN_LIMIT_HARD = 50
MONSTER_LIMIT_HARD = 50

IMAGES_HARD = {
  'dot_img' : transform.scale(img.load("assets/img/dot_img.png"), (gap_hard * DOT_SIZE, gap_hard * DOT_SIZE)),
  'banana_coin' : transform.scale(img.load("assets/img/banana_coin.png"), (int(gap_hard * BANANA_SIZE), int(gap_hard * BANANA_SIZE))),
  'barrier_img' : transform.scale(img.load("assets/img/brick_barrier.png"), (gap_hard, gap_hard)),
  'monkey_start' : transform.scale(img.load("assets/img/monkey_start.png"), (int(gap_hard * OTHER_SIZE), int(gap_hard * OTHER_SIZE))),
  'book_end' : transform.scale(img.load("assets/img/book_end.png"), (int(gap_hard * OTHER_SIZE), int(gap_hard * OTHER_SIZE))),
  'monster' : transform.scale(img.load("assets/img/monster.png"), (int(gap_hard * OTHER_SIZE), int(gap_hard * OTHER_SIZE))),
}