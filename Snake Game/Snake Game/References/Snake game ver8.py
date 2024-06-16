import pygame
import random
from numpy import sqrt

# Initialize Pygame
pygame.init()

# Set up display
width, height = 640, 480
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game with A* Pathfinding")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
gray = (50, 50, 50)
green = (0, 255, 0)
blue = (0, 0, 255)

# Game settings
block_size = 20
cols = width // block_size
rows = height // block_size
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

# Initialize high score
high_score = 0

# Game over message
def game_over_message():
    msg = font.render("Game Over! Press R to Restart", True, red)
    win.blit(msg, [width / 6, height / 3])

# Draw grid
def draw_grid():
    for x in range(0, width, block_size):
        pygame.draw.line(win, gray, (x, 0), (x, height))
    for y in range(0, height, block_size):
        pygame.draw.line(win, gray, (0, y), (width, y))

# Spot class for A* pathfinding
class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.camefrom = None
        self.obstrucle = False

    def add_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < cols - 1:
            self.neighbors.append(grid[self.x][self.y + 1])

# Create grid for A* pathfinding
grid = [[Spot(i, j) for j in range(cols)] for i in range(rows)]
for i in range(rows):
    for j in range(cols):
        grid[i][j].add_neighbors()

# A* pathfinding function
def getpath(food, snake):
    for s in snake:
        s.camefrom = None
    openset = [snake[-1]]
    closedset = []
    while openset:
        current = min(openset, key=lambda x: x.f)
        if current == food:
            break
        openset.remove(current)
        closedset.append(current)
        for neighbor in current.neighbors:
            if neighbor in closedset or neighbor in snake:
                continue
            temp_g = current.g + 1
            if neighbor not in openset:
                openset.append(neighbor)
            elif temp_g >= neighbor.g:
                continue
            neighbor.camefrom = current
            neighbor.g = temp_g
            neighbor.h = sqrt((neighbor.x - food.x) ** 2 + (neighbor.y - food.y) ** 2)
            neighbor.f = neighbor.g + neighbor.h
    path = []
    while current.camefrom:
        path.append(current)
        current = current.camefrom
    path.reverse()
    return path

# Main game loop
def game_loop():
    global high_score
    
    game_over = False
    game_close = False

    snake = [grid[rows // 2][cols // 2]]
    snake_length = 1

    # Initial food spawn
    food = grid[random.randrange(0, rows)][random.randrange(0, cols)]
    path = getpath(food, snake)

    while not game_over:

        while game_close:
            win.fill(black)
            game_over_message()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        if path:
            next_move = path.pop(0)
            snake.append(next_move)
            if len(snake) > snake_length:
                del snake[0]
        else:
            game_close = True

        x = snake[-1].x * block_size
        y = snake[-1].y * block_size
        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        win.fill(black)
        draw_grid()

        pygame.draw.rect(win, green, [food.x * block_size, food.y * block_size, block_size, block_size])
        for segment in snake:
            pygame.draw.rect(win, white, [segment.x * block_size, segment.y * block_size, block_size, block_size])

        if snake[-1] == food:
            food = grid[random.randrange(0, rows)][random.randrange(0, cols)]
            snake_length += 1
            path = getpath(food, snake)

        pygame.display.update()
        clock.tick(15)

    pygame.quit()
    quit()

game_loop()
