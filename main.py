import pygame
import numpy as np

class Cell:
    def __init__(self, is_al):
        self.is_avalible = is_al
        self.C = 0
        self.f_eq = [0.0, 0.0, 0.0, 0.0]  #lewo, góra, prawo, dół
        self.f_in = [0.0, 0.0, 0.0, 0.0]
        self.f_out = [0.0, 0.0, 0.0, 0.0]

    def set_C(self, c):
        self.C = c

#Parametry modelu
CELL_SIZE = 4
GRID_WIDTH = 50
GRID_HEIGHT = 50
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

#Siatka komórek
grid = [[Cell(True) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
w = [0.25, 0.25, 0.25, 0.25]

def eq_function():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                for i in range(4):
                    grid[y][x].f_eq[i] = grid[y][x].C * w[i]

def out_function():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                for i in range(4):
                    grid[y][x].f_out[i] = grid[y][x].f_eq[i]

def collision():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                #Inicjalizacja sąsiadów
                neighbours = [-1.0, -1.0, -1.0, -1.0]

                #Górny sąsiad
                if y > 0 and grid[y-1][x].is_avalible:
                    neighbours[0] = grid[y-1][x].f_out[2]

                #Dolny sąsiad
                if y < GRID_HEIGHT-1 and grid[y+1][x].is_avalible:
                    neighbours[2] = grid[y+1][x].f_out[0]

                #Lewy sąsiad
                if x > 0 and grid[y][x-1].is_avalible:
                    neighbours[1] = grid[y][x-1].f_out[3]

                #Prawy sąsiad
                if x < GRID_WIDTH-1 and grid[y][x+1].is_avalible:
                    neighbours[3] = grid[y][x+1].f_out[1]

                #Aktualizacja f_in
                for i in range(4):
                    if neighbours[i] == -1.0:
                        grid[y][x].f_in[i] = grid[y][x].f_out[i]  # odbicie
                    else:
                        grid[y][x].f_in[i] = neighbours[i]

def update_C():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x].is_avalible:
                grid[y][x].C = sum(grid[y][x].f_in)

def init_grid():
    #Inicjalizacja warunków brzegowych i początkowych
    for x in range(GRID_WIDTH):
        grid[0][x] = Cell(False)
        grid[GRID_HEIGHT - 1][x] = Cell(False)
    for y in range(GRID_HEIGHT):
        grid[y][0] = Cell(False)
        grid[y][GRID_WIDTH - 1] = Cell(False)

    barrier_x = GRID_WIDTH // 4

    for y in range(GRID_HEIGHT):
        if GRID_HEIGHT // 2 - 10 <= y <= GRID_HEIGHT // 2 + 10:
            continue
        grid[y][barrier_x] = Cell(False)

    #Lewa część siatki
    for y in range(1, GRID_HEIGHT - 1):
        for x in range(1, barrier_x):
            temp = Cell(True)
            temp.set_C(1.0)
            grid[y][x] = temp

    #Prawa część siatki
    for y in range(1, GRID_HEIGHT - 1):
        for x in range(barrier_x + 1, GRID_WIDTH - 1):
            temp = Cell(True)
            temp.set_C(0.5)
            grid[y][x] = temp

def draw_board(screen):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if not grid[y][x].is_avalible:
                color = (255, 0, 255)  #Ścianki
            else:
                intensity = int(np.clip(grid[y][x].C, 0, 1) * 255)
                color = (intensity, intensity, 0)
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    init_grid()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Aktualizacja planszy
        eq_function()
        out_function()
        collision()
        update_C()

        # Rysowanie planszy
        screen.fill((0, 0, 0))
        draw_board(screen)

        pygame.display.flip()
        clock.tick(300)

    pygame.quit()

main()
