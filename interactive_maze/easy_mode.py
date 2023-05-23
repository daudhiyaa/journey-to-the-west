import pygame
import random
import colors
import tkinter as tk
from queue import Queue
from config_levels import *

pygame.font.init()

gap = WIDTH // ROWS_EASY
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Treasure Hunt")

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = colors.WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.previous = None
        self.has_coin = False
        self.has_monster = False

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == colors.RED

    def is_open(self):
        return self.color == colors.GREEN

    def is_barrier(self):
        return self.color is None

    def is_start(self):
        return self.color is None

    def is_end(self):
        return self.color is None

    def reset(self):
        self.color = colors.WHITE
        self.previous = None

    def make_start(self):
        self.color = None
        WIN.blit(IMAGES_EASY['monkey_start'], (self.x + (gap // 2) - (IMAGES_EASY['monkey_start'].get_width() // 2), \
                self.y + (gap // 2) - (IMAGES_EASY['monkey_start'].get_height() // 2)))

    def make_closed(self):
        self.color = colors.RED

    def make_open(self):
        self.color = colors.GREEN

    def make_barrier(self):
        self.color = None
        WIN.blit(IMAGES_EASY['barrier_img'], (self.x, self.y))

    def make_end(self):
        self.color = colors.TURQUOISE

    def make_path(self):
        self.color = None
        WIN.blit(IMAGES_EASY['dot_img'], (self.x + (gap // 2), self.y + (gap // 2)))

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        if self.has_coin:
            win.blit(IMAGES_EASY['banana_coin'], (self.x + (gap // 2) - (IMAGES_EASY['banana_coin'].get_width() // 2), \
                    self.y + (gap // 2) - (IMAGES_EASY['banana_coin'].get_height() // 2)))
        if self.has_monster:
            win.blit(IMAGES_EASY['monster'], (self.x + (gap // 2) - (IMAGES_EASY['monster'].get_width() // 2),\
                    self.y + (gap // 2) - (IMAGES_EASY['monster'].get_height() // 2)))

    def update_neighbors(self, grid):
        self.neighbors = []
        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        # RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self ):
        return False

def show_result(txt):
    window = tk.Tk()
    window.title("Result")

    label = tk.Label(window, text=txt, font=("Arial", 30))
    label.config(font=("Arial", 36))
    label.pack()
    window.mainloop()

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

    show_result("Path is not found")
    return False

def reconstruct_path(current, draw):
    cost = 0
    while current.previous:
        cost += 1
        current = current.previous
        if current.has_coin:
            cost -= 1
        if current.has_monster:
            cost += 1
        current.make_path()
        draw()
    show_result('Your cost is ' + str(cost))

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
        pygame.draw.line(win, colors.GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, colors.GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    for row in grid:
        for spot in row:
            if spot.color is not None:  # Hanya gambar sel yang memiliki warna
                spot.draw(win)
                if spot.is_barrier():
                    WIN.blit(IMAGES_EASY['barrier_img'], (spot.x, spot.y))
                elif spot.has_coin:
                    WIN.blit(IMAGES_EASY['banana_coin'], (spot.x + (spot.width // 2) - (IMAGES_EASY['banana_coin'].get_width() // 2),
                            spot.y + (spot.width // 2) - (IMAGES_EASY['banana_coin'].get_height() // 2)))
                elif spot.has_monster:
                    WIN.blit(IMAGES_EASY['monster'], (spot.x + (spot.width // 2) - (IMAGES_EASY['monster'].get_width() // 2),
                            spot.y + (spot.width // 2) - (IMAGES_EASY['monster'].get_height() // 2)))

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
    while coin_count < COIN_LIMIT_EASY:
        row = random.randint(0, len(grid) - 1)
        col = random.randint(0, len(grid[0]) - 1)
        spot = grid[row][col]
        if spot != start and spot != end and not spot.is_barrier() and not spot.has_coin and not spot.has_monster:
            spot.has_coin = True
            coin_count += 1

    monster_count = 0
    while monster_count < MONSTER_LIMIT_EASY:
        row = random.randint(0, len(grid) - 1)
        col = random.randint(0, len(grid[0]) - 1)
        spot = grid[row][col]
        if spot != start and spot != end and not spot.is_barrier() and not spot.has_coin and not spot.has_monster:
            spot.has_monster = True
            monster_count += 1

def main(win, width):
    grid = make_grid(ROWS_EASY, width)

    start = None
    end = None

    # Add this line to generate a random maze
    generate_random_maze(grid, start, end)

    run = True
    while run:
        draw(win, grid, ROWS_EASY, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS_EASY, width)
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
                row, col = get_clicked_pos(pos, ROWS_EASY, width)
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

                    bfs(lambda: draw(win, grid, ROWS_EASY, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS_EASY, width)

                # RESET IF BACKSPACE
                if event.key == pygame.K_BACKSPACE:
                    start = None
                    end = None
                    grid = make_grid(ROWS_EASY, width)

    pygame.quit()

main(WIN, WIDTH)
