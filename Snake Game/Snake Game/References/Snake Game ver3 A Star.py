import pygame
import random
from numpy import sqrt

# Initialize Pygame
pygame.init()

# Set up display
width, height = 640, 480
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Autonomous Snake Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
gray = (50, 50, 50)

# Game settings
block_size = 20
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

# Initialize high score
high_score = 0

# Spot class for A* algorithm
class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.camefrom = None

    def add_neighbors(self, grid):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < len(grid) - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < len(grid[0]) - 1:
            self.neighbors.append(grid[self.x][self.y + 1])

# Function to calculate A* path
def calculate_path(food, snake, grid):
    for row in grid:
        for spot in row:
            spot.f = 0
            spot.g = 0
            spot.h = 0
            spot.camefrom = None

    openset = [snake[-1]]
    closedset = []

    while openset:
        current = min(openset, key=lambda x: x.f)
        openset.remove(current)
        closedset.append(current)

        if current == food:
            path = []
            while current.camefrom:
                path.append(current.camefrom)
                current = current.camefrom
            path.reverse()
            return path

        for neighbor in current.neighbors:
            if neighbor not in closedset and neighbor not in snake:
                tempg = current.g + 1
                if neighbor in openset:
                    if tempg < neighbor.g:
                        neighbor.g = tempg
                else:
                    neighbor.g = tempg
                    openset.append(neighbor)
                    neighbor.h = sqrt((neighbor.x - food.x) ** 2 + (neighbor.y - food.y) ** 2)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.camefrom = current

    return None

# Draw grid function
def draw_grid():
    for x in range(0, width, block_size):
        pygame.draw.line(win, gray, (x, 0), (x, height))
    for y in range(0, height, block_size):
        pygame.draw.line(win, gray, (0, y), (width, y))

# Main game loop
def game_loop():
    global high_score

    game_over = False
    game_close = False

    x = width / 2
    y = height / 2
    x_change = 0
    y_change = 0

    snake = []
    snake_length = 1

    # Initialize snake position
    snake.append(Spot(round(x / block_size), round(y / block_size)))

    # Initial food spawn
    food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, height - block_size) / block_size) * block_size
    food = Spot(round(food_x / block_size), round(food_y / block_size))

    # Create grid of Spot objects
    grid = [[Spot(i, j) for j in range(height // block_size)] for i in range(width // block_size)]

    for row in grid:
        for spot in row:
            spot.add_neighbors(grid)

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
                        if snake_length > high_score:
                            high_score = snake_length
                        game_loop()

        # Calculate path using A*
        path = calculate_path(food, snake, grid)
        if path:
            next_spot = path[0]
            x_change = (next_spot.x - snake[-1].x) * block_size
            y_change = (next_spot.y - snake[-1].y) * block_size

        # Update snake position
        x += x_change
        y += y_change
        snake.append(Spot(round(x / block_size), round(y / block_size)))

        # Check collision with walls or itself
        if x >= width or x < 0 or y >= height or y < 0 or len(snake) != len(set(snake)):
            game_close = True

        # Check if snake eats food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
            food_y = round(random.randrange(0, height - block_size) / block_size) * block_size
            food = Spot(round(food_x / block_size), round(food_y / block_size))
            snake_length += 1

        # Remove tail if not eating food
        else:
            snake.pop(0)

        # Update screen
        win.fill(black)
        draw_grid()
        pygame.draw.rect(win, red, [food_x, food_y, block_size, block_size])
        for spot in snake:
            pygame.draw.rect(win, white, [spot.x * block_size, spot.y * block_size, block_size, block_size])

        pygame.display.update()

        # Clock tick
        clock.tick(15)

    pygame.quit()
    quit()

# Start game loop
game_loop()
