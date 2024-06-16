import pygame
from pygame import display, time, draw, QUIT, init, KEYDOWN, K_a, K_s, K_d, K_w
from random import randint
from numpy import sqrt

init()

done = False
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (50, 50, 50)

cols = 25
rows = 25

width = 600
height = 600
wr = width / cols
hr = height / rows
direction = 1

screen = display.set_mode([width, height])
display.set_caption("snake_self")
clock = time.Clock()

def draw_grid():
    for x in range(0, width, int(wr)):
        pygame.draw.line(screen, GRAY, (x, 0), (x, height))
    for y in range(0, height, int(hr)):
        pygame.draw.line(screen, GRAY, (0, y), (width, y))

def getpath(food1, snake1):
    food1.camefrom = []
    for s in snake1:
        s.camefrom = []
    openset = [snake1[-1]]
    closedset = []
    dir_array1 = []
    while 1:
        current1 = min(openset, key=lambda x: x.f)
        openset = [openset[i] for i in range(len(openset)) if not openset[i] == current1]
        closedset.append(current1)
        for neighbor in current1.neighbors:
            if neighbor not in closedset and not neighbor.obstrucle and neighbor not in snake1:
                tempg = neighbor.g + 1
                if neighbor in openset:
                    if tempg < neighbor.g:
                        neighbor.g = tempg
                else:
                    neighbor.g = tempg
                    openset.append(neighbor)
                neighbor.h = sqrt((neighbor.x - food1.x) ** 2 + (neighbor.y - food1.y) ** 2)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.camefrom = current1
        if current1 == food1:
            break
    while current1.camefrom:
        if current1.x == current1.camefrom.x and current1.y < current1.camefrom.y:
            dir_array1.append(2)
        elif current1.x == current1.camefrom.x and current1.y > current1.camefrom.y:
            dir_array1.append(0)
        elif current1.x < current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(3)
        elif current1.x > current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(1)
        current1 = current1.camefrom
    for i in range(rows):
        for j in range(cols):
            grid[i][j].camefrom = []
            grid[i][j].f = 0
            grid[i][j].h = 0
            grid[i][j].g = 0
            grid[i][j].obstrucle = False
    return dir_array1

def draw_path(snake, dir_array):
    path = []
    current = snake[-1]
    for direction in reversed(dir_array):
        if direction == 0:  # down
            next_spot = grid[current.x][current.y + 1]
        elif direction == 1:  # right
            next_spot = grid[current.x + 1][current.y]
        elif direction == 2:  # up
            next_spot = grid[current.x][current.y - 1]
        elif direction == 3:  # left
            next_spot = grid[current.x - 1][current.y]
        path.append(next_spot)
        current = next_spot
    
    for i in range(len(path) - 1):
        start_pos = (path[i].y * wr + wr / 2, path[i].x * hr + hr / 2)
        end_pos = (path[i + 1].y * wr + wr / 2, path[i + 1].x * hr + hr / 2)
        pygame.draw.line(screen, RED, start_pos, end_pos, 2)

class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.camefrom = []
        self.obstrucle = False

    def show(self, color):
        draw.rect(screen, color, [self.y * wr + 2, self.x * hr + 2, wr - 4, hr - 4])

    def add_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < cols - 1:
            self.neighbors.append(grid[self.x][self.y + 1])

grid = [[Spot(i, j) for j in range(cols)] for i in range(rows)]

for i in range(rows):
    for j in range(cols):
        grid[i][j].add_neighbors()

snake = [grid[round(rows / 2)][round(cols / 2)]]
food = grid[randint(0, rows - 1)][randint(0, cols - 1)]
current = snake[-1]
dir_array = getpath(food, snake)
food_array = [food]

while not done:
    clock.tick(12)
    screen.fill(BLACK)
    draw_grid()

    direction = dir_array.pop(-1)
    if direction == 0:  # down
        snake.append(grid[current.x][current.y + 1])
    elif direction == 1:  # right
        snake.append(grid[current.x + 1][current.y])
    elif direction == 2:  # up
        snake.append(grid[current.x][current.y - 1])
    elif direction == 3:  # left
        snake.append(grid[current.x - 1][current.y])
    current = snake[-1]

    if current.x == food.x and current.y == food.y:
        while 1:
            food = grid[randint(0, rows - 1)][randint(0, cols - 1)]
            if not (food.obstrucle or food in snake):
                break
        food_array.append(food)
        dir_array = getpath(food, snake)
    else:
        snake.pop(0)

    draw_path(snake, dir_array)  # Draw the path

    # Draw the snake continuously
    for spot in snake:
        spot.show(WHITE)
    snake[-1].show(WHITE)  # Draw the head of the snake in white

    for i in range(rows):
        for j in range(cols):
            if grid[i][j].obstrucle:
                grid[i][j].show(RED)

    food.show(GREEN)
    display.flip()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == KEYDOWN:
            if event.key == K_w and not direction == 0:
                direction = 2
            elif event.key == K_a and not direction == 1:
                direction = 3
            elif event.key == K_s and not direction == 2:
                direction = 0
            elif event.key == K_d and not direction == 3:
                direction = 1