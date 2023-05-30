import pygame
import random
import colors
import tkinter as tk
from queue import Queue
from config_levels import *

pygame.font.init()

# BASE INITIALIZATION
gap = WIDTH // ROWS_HARD
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Treasure Hunt")

# 'CELL' CLASS
# Cell inside maze
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
    
    # GET POSITION (X and Y)
    def get_pos(self):
        return self.row, self.col
    
    # RESET TO BASE MAZE
    def reset(self):
        self.color = colors.WHITE
        self.previous = None
    
    # CHECK IS BARRIER OR NOT
    def is_barrier(self):
        return self.color is None

    # DRAW STARTING POINT
    def make_start(self):
        self.color = None
        WIN.blit(IMAGES_HARD['monkey_start'], (self.x + (gap // 2) - (IMAGES_HARD['monkey_start'].get_width() // 2), \
                self.y + (gap // 2) - (IMAGES_HARD['monkey_start'].get_height() // 2)))

    # DRAW STEP-BY-STEP OF BFS ALGORITHM
    def make_closed(self):
        self.color = colors.RED
    def make_open(self):
        self.color = colors.GREEN
    
    # DRAW BARRIER / WALL
    def make_barrier(self):
        self.color = None
        WIN.blit(IMAGES_HARD['barrier_img'], (self.x, self.y))

    # DRAW END / FINISH POINT
    def make_end(self):
        self.color = colors.TURQUOISE

    # DRAW PATH USING 'DOT' OR 'PELLET'
    def make_path(self):
        self.color = None
        WIN.blit(IMAGES_HARD['dot_img'], (self.x + (gap // 2), self.y + (gap // 2)))

    # DRAW CELL
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        if self.has_coin:
            win.blit(IMAGES_HARD['banana_coin'], (self.x + (gap // 2) - (IMAGES_HARD['banana_coin'].get_width() // 2), \
                    self.y + (gap // 2) - (IMAGES_HARD['banana_coin'].get_height() // 2)))
        if self.has_monster:
            win.blit(IMAGES_HARD['monster'], (self.x + (gap // 2) - (IMAGES_HARD['monster'].get_width() // 2),\
                    self.y + (gap // 2) - (IMAGES_HARD['monster'].get_height() // 2)))

    # UPDATE NEIGHBORS WHILE RUN THE BFS ALGORITHM
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

# FUNCTION TO SHOW RESULT USING TKINTER
def show_result(txt):
    window = tk.Tk()
    window.title("Result")

    label = tk.Label(window, text=txt, font=("Arial", 30))
    label.config(font=("Arial", 36))
    label.pack()
    window.mainloop()

# BFS ALGORITHM IMPLEMENTATION
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

# RECONSTRUCT PATH AFTER ARRIVE IN FINISH POINT
# if there is no path, this function is not called
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

# CREATE GRID DEPEND ON HOW MANY ROWS & WIDTH
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

# DRAW LINE TO CREATE GRID
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, colors.GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, colors.GREY, (j * gap, 0), (j * gap, width))

# DRAWING ASSETS INSIDE MAZE
def draw(win, grid, rows, width):
    for row in grid:
        for spot in row:
            if spot.color is not None:  # Hanya gambar sel yang memiliki warna
                spot.draw(win)
                if spot.is_barrier():
                    WIN.blit(IMAGES_HARD['barrier_img'], (spot.x, spot.y))
                elif spot.has_coin:
                    WIN.blit(IMAGES_HARD['banana_coin'], (spot.x + (spot.width // 2) - (IMAGES_HARD['banana_coin'].get_width() // 2),
                            spot.y + (spot.width // 2) - (IMAGES_HARD['banana_coin'].get_height() // 2)))
                elif spot.has_monster:
                    WIN.blit(IMAGES_HARD['monster'], (spot.x + (spot.width // 2) - (IMAGES_HARD['monster'].get_width() // 2),
                            spot.y + (spot.width // 2) - (IMAGES_HARD['monster'].get_height() // 2)))

    draw_grid(win, rows, width)
    pygame.display.update()

# EVENT HANDLER TO GET POSITION OF CLICKED MOUSE
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

# FUNCTION TO GENERATE RANDOM MAZE
def generate_random_maze(grid, start, end):
    for row in grid:
        for spot in row:
            if spot != start and spot != end:
                if random.random() < 0.3:  # Adjust the probability of barriers here
                    spot.make_barrier()

    coin_count = 0
    while coin_count < COIN_LIMIT_HARD:
        row = random.randint(0, len(grid) - 1)
        col = random.randint(0, len(grid[0]) - 1)
        spot = grid[row][col]
        if spot != start and spot != end and not spot.is_barrier() and not spot.has_coin and not spot.has_monster:
            spot.has_coin = True
            coin_count += 1

    monster_count = 0
    while monster_count < MONSTER_LIMIT_HARD:
        row = random.randint(0, len(grid) - 1)
        col = random.randint(0, len(grid[0]) - 1)
        spot = grid[row][col]
        if spot != start and spot != end and not spot.is_barrier() and not spot.has_coin and not spot.has_monster:
            spot.has_monster = True
            monster_count += 1

# DRIVER CODE
def main(win, width):
    grid = make_grid(ROWS_HARD, width)

    start = None
    end = None

    # Add this line to generate a random maze
    generate_random_maze(grid, start, end)
    
    # GAME LOOP
    run = True
    while run:
        draw(win, grid, ROWS_HARD, width)
        # FOR EVERY EVENT IN GAME
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # IF LEFT BUTTON OF MOUSE CLICKED
            # FIRST CLICK: PUT START POINT
            # SECOND CLICK: PUT END POINT
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS_HARD, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            # IF RIGHT BUTTON OF MOUSE CLICKED
            # ERASE / RESET CLICKED SPOT
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS_HARD, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                # START THE GAME IF SPACE IS CLICKED
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    bfs(lambda: draw(win, grid, ROWS_HARD, width), grid, start, end)

                # RESET IF BACKSPACE
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS_HARD, width)

    pygame.quit()

main(WIN, WIDTH)
