import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRID_COLOR = (50, 50, 50)

# Screen and grid settings
cols = 25
rows = 25
width = 600
height = 600
wr = width / cols
hr = height / rows

# Initialize screen
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.camefrom = None
        self.obstacle = False

    def show(self, color):
        pygame.draw.rect(screen, color, [self.x * wr + 2, self.y * hr + 2, wr - 4, hr - 4])

    def add_neighbors(self, grid):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])

# Create grid of Spot objects
grid = [[Spot(i, j) for j in range(cols)] for i in range(rows)]
for i in range(rows):
    for j in range(cols):
        grid[i][j].add_neighbors(grid)

# Function to find path using A* algorithm
def find_path(start, goal):
    open_set = [start]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = min(open_set, key=lambda x: f_score.get(x, float('inf')))
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path
        
        open_set.remove(current)
        
        for neighbor in current.neighbors:
            if neighbor.obstacle:
                continue
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if neighbor not in open_set:
                    open_set.append(neighbor)
    
    return []

# Heuristic function (Euclidean distance)
def heuristic(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

# Initialize snake and food
snake = [grid[rows // 2][cols // 2]]
food = grid[random.randint(0, rows - 1)][random.randint(0, cols - 1)]
path = find_path(snake[-1], food)

# Main loop
running = True
while running:
    clock.tick(12)
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move snake
    if path:
        next_move = path.pop(0)
        snake.append(next_move)
        if next_move == food:
            food = grid[random.randint(0, rows - 1)][random.randint(0, cols - 1)]
            path = find_path(snake[-1], food)
        else:
            snake.pop(0)
    else:
        running = False

    # Draw grid
    for row in grid:
        for spot in row:
            color = RED if spot.obstacle else GRID_COLOR
            pygame.draw.rect(screen, color, [spot.x * wr, spot.y * hr, wr, hr], 1)

    # Draw snake
    for segment in snake:
        segment.show(WHITE)

    # Draw food
    food.show(GREEN)

    # Draw path
    for i in range(len(path) - 1):
        pygame.draw.line(screen, RED, (path[i].x * wr + wr / 2, path[i].y * hr + hr / 2),
                         (path[i + 1].x * wr + wr / 2, path[i + 1].y * hr + hr / 2), 3)

    # Update display
    pygame.display.flip()

pygame.quit()
