import pygame
from spot import Spot

class Board:
    def __init__(self):
        self.cols = 25
        self.rows = 25
        self.width = 600
        self.height = 600
        self.wr = self.width / self.cols
        self.hr = self.height / self.rows
        self.screen = pygame.display.set_mode([self.width, self.height])
        pygame.display.set_caption("snake_self")
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.GRAY = (50, 50, 50)

        self.grid = [[Spot(i, j) for j in range(self.cols)] for i in range(self.rows)]

    def draw_grid(self):
        for x in range(0, self.width, int(self.wr)):
            pygame.draw.line(self.screen, self.GRAY, (x, 0), (x, self.height))
        for y in range(0, self.height, int(self.hr)):
            pygame.draw.line(self.screen, self.GRAY, (0, y), (self.width, y))
