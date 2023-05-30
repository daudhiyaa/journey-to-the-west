import pygame
import colors
from queue import Queue
from config_levels import *

# BASE INITIALIZATION
gap = WIDTH // ROWS_MEDIUM
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
        self.color = colors.YELLOW

    # DRAW STEP-BY-STEP OF BFS ALGORITHM
    def make_closed(self):
        self.color = colors.RED
    def make_open(self):
        self.color = colors.GREEN
    
    # DRAW BARRIER / WALL
    def make_barrier(self):
        self.color = None
        WIN.blit(IMAGES_MEDIUM['barrier_img'], (self.x, self.y))

    # DRAW END / FINISH POINT
    def make_end(self):
        self.color = colors.TURQUOISE

    # DRAW PATH USING 'DOT' OR 'PELLET'
    def make_path(self):
        self.color = None
        WIN.blit(IMAGES_MEDIUM['dot_img'], (self.x + (gap // 2), self.y + (gap // 2)))

    # DRAW CELL
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

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

    return False

# RECONSTRUCT PATH AFTER ARRIVE IN FINISH POINT
# if there is no path, this function is not called
def reconstruct_path(current, draw):
    while current.previous:
        current = current.previous
        current.make_path()
        draw()

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
                    WIN.blit(IMAGES_MEDIUM['barrier_img'], (spot.x, spot.y))

    draw_grid(win, rows, width)
    pygame.display.update()

# EVENT HANDLER TO GET POSITION OF CLICKED MOUSE
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

# DRIVER CODE
def main(win, width):
    grid = make_grid(ROWS_MEDIUM, width)

    start = None
    end = None

    # GAME LOOP
    run = True
    while run:
        draw(win, grid, ROWS_MEDIUM, width)
        # FOR EVERY EVENT IN GAME
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # IF LEFT BUTTON OF MOUSE CLICKED
            # FIRST CLICK: PUT START POINT
            # SECOND CLICK: PUT END POINT
            # ELSE: DRAW BARRIER
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS_MEDIUM, width)
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
                row, col = get_clicked_pos(pos, ROWS_MEDIUM, width)
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

                    bfs(lambda: draw(win, grid, ROWS_MEDIUM, width), grid, start, end)

                # RESET IF BACKSPACE
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS_MEDIUM, width)

    pygame.quit()

main(WIN, WIDTH)
