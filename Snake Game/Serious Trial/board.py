import pygame
import random

class Board:
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.food_x, self.food_y = self.generate_food_position()

        # Colors
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.gray = (50, 50, 50)

    def draw_grid(self, window):
        for x in range(0, self.width, self.block_size):
            pygame.draw.line(window, self.gray, (x, 0), (x, self.height))
        for y in range(0, self.height, self.block_size):
            pygame.draw.line(window, self.gray, (0, y), (self.width, y))

    def draw_food(self, window):
        pygame.draw.rect(window, self.red, [self.food_x, self.food_y, self.block_size, self.block_size])

    def generate_food_position(self):
        x = round(random.randrange(0, self.width - self.block_size) / self.block_size) * self.block_size
        y = round(random.randrange(0, self.height - self.block_size) / self.block_size) * self.block_size
        return x, y
