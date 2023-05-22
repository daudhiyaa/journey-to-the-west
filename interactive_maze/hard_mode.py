import pygame
import random
import math
from queue import Queue
import pygame.image as img
import pygame.transform as transform
import tkinter as tk

# Reference
# https://youtu.be/JtiK0DOeI4A

pygame.font.init()

WIDTH = 800
ROWS = 50
gap = WIDTH // ROWS
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Treasure Hunt")

COIN_LIMIT = 50
MONSTER_LIMIT = 40

font_size = 50
font_color = (255, 255, 255)  # White
font_style = pygame.font.Font(None, font_size)  # None for default system font

# Create a text surface
text = "Hello, Pygame!"

# color
RED = (102, 0, 0)
GREEN = (51, 102, 0)
BLUE = (0, 255, 0)
yellow_start = (242, 242, 0)  # start point
WHITE = (0, 0, 0)  # base
blue_barrier = (34, 34, 232)  # barrier
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# load image
dot_img = img.load("assets/dot_img.png")
dot_img = transform.scale(dot_img, (gap * 0.3, gap * 0.3))
banana_coin = pygame.image.load("assets/banana_coin.png")
banana_coin = pygame.transform.scale(banana_coin, (int(gap * 0.6), int(gap * 0.6)))
barrier_img = pygame.image.load("assets/brick_barrier.png")
barrier_img = pygame.transform.scale(barrier_img, (gap, gap))
monkey_start = pygame.image.load("assets/monkey_start.png")
monkey_start = pygame.transform.scale(monkey_start, (int(gap * 0.7), int(gap * 0.7)))
book_end = pygame.image.load("assets/book_end.png")
book_end = pygame.transform.scale(book_end, (int(gap * 0.7), int(gap * 0.7)))
monster = pygame.image.load("assets/monster.png")
monster = pygame.transform.scale(monster, (int(gap * 0.7), int(gap * 0.7)))

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.previous = None
        self.has_coin = False
        self.has_monster = False


    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color is None

    def is_start(self):
        return self.color is None

    def is_end(self):
        return self.color is None

    def reset(self):
        self.color = WHITE
        self.previous = None

    def make_start(self):
        self.color = None
        WIN.blit(monkey_start, (self.x + (gap // 2) - (monkey_start.get_width() // 2), self.y + (gap // 2) - (monkey_start.get_height() // 2)))

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = None
        WIN.blit(barrier_img, (self.x, self.y))

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = None
        WIN.blit(dot_img, (self.x + (gap // 2), self.y + (gap // 2)))

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        if self.has_coin:
            win.blit(banana_coin, (self.x + (gap // 2) - (banana_coin.get_width() // 2), self.y + (gap // 2) - (banana_coin.get_height() // 2)))
        if self.has_monster:
            win.blit(monster, (self.x + (gap // 2) - (monster.get_width() // 2), self.y + (gap // 2) - (monster.get_height() // 2)))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def bfs(draw, grid, start, end):
    visited = set()
    queue = Queue()
    queue.put(start)
    visited.add(start)

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.get()

        if current == end:
            reconstruct_path(current, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                queue.put(neighbor)
                visited.add(neighbor)
                neighbor.previous = current
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    # Create a Tkinter window
    window = tk.Tk()

    # Set the window title
    window.title("Result")

    # Create a Label widget
    label = tk.Label(window, text='Path is not found', font=("Arial", 30))

    # Resize the label
    label.config(font=("Arial", 36))

    # Place the label using pack() or grid() method
    # Using pack():
    label.pack()

    # OR
    # Using grid():
    # label.grid(row=0, column=0)

    # Start the Tkinter event loop
    window.mainloop()
    return False

def reconstruct_path(current, draw):
    cnt = 0
    while current.previous:
        cnt += 1
        current = current.previous
        if current.has_coin:
            cnt -= 1
        if current.has_monster:
            cnt += 1
        current.make_path()
        draw()
    print ('Cost = ', cnt)
    text_surface = font_style.render('Your cost is ' + str(cnt), True, font_color)
    # Get the dimensions of the text surface
    text_width, text_height = text_surface.get_size()
    background_surface = pygame.Surface((text_width, text_height))
    background_surface.fill((0, 0, 0))

    # Blit the text surface onto the background surface
    background_surface.blit(text_surface, (0, 0))

    # Calculate the position to center the text on the window
    x = (WIDTH) // 3
    y = (WIDTH) // 3

    # Blit the text surface onto the window
    # WIN.blit(background_surface, (x, y))

    # Create a Tkinter window
    window = tk.Tk()

    # Set the window title
    window.title("Result")

    # Create a Label widget
    label = tk.Label(window, text='Your cost is ' + str(cnt), font=("Arial", 30))

    # Resize the label
    label.config(font=("Arial", 36))

    # Place the label using pack() or grid() method
    # Using pack():
    label.pack()

    # OR
    # Using grid():
    # label.grid(row=0, column=0)

    # Start the Tkinter event loop
    window.mainloop()
    

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    for row in grid:
        for spot in row:
            if spot.color is not None:  # Hanya gambar sel yang memiliki warna
                spot.draw(win)
                if spot.is_barrier():
                    WIN.blit(barrier_img, (spot.x, spot.y))
                elif spot.has_coin:
                    WIN.blit(banana_coin, (spot.x + (spot.width // 2) - (banana_coin.get_width() // 2),
                                        spot.y + (spot.width // 2) - (banana_coin.get_height() // 2)))
                elif spot.has_monster:
                    WIN.blit(monster, (spot.x + (spot.width // 2) - (monster.get_width() // 2),
                                        spot.y + (spot.width // 2) - (monster.get_height() // 2)))

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def generate_random_maze(grid, start, end):
    for row in grid:
        for spot in row:
            if spot != start and spot != end:
                if random.random() < 0.3:  # Adjust the probability of barriers here
                    spot.make_barrier()
    coin_count = 0
    while coin_count < COIN_LIMIT:
        row = random.randint(0, len(grid) - 1)
        col = random.randint(0, len(grid[0]) - 1)
        spot = grid[row][col]
        if spot != start and spot != end and not spot.is_barrier() and not spot.has_coin and not spot.has_monster:
            spot.has_coin = True
            coin_count += 1
    monster_count = 0
    while monster_count < MONSTER_LIMIT:
        row = random.randint(0, len(grid) - 1)
        col = random.randint(0, len(grid[0]) - 1)
        spot = grid[row][col]
        if spot != start and spot != end and not spot.is_barrier() and not spot.has_coin and not spot.has_monster:
            spot.has_monster = True
            monster_count += 1


def main(win, width):
    grid = make_grid(ROWS, width)

    start = None
    end = None

    generate_random_maze(grid, start, end)  # Add this line to generate a random maze

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                # RESET IF BACKSPACE
                if event.key == pygame.K_BACKSPACE:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH)