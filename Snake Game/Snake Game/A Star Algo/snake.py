import pygame
from random import randint
from board import Board
from pathfinding import get_path, draw_path

class SnakeGame:
    def __init__(self):
        self.board = Board()
        self.snake = [self.board.grid[self.board.rows // 2][self.board.cols // 2]]
        self.food = self.board.grid[randint(0, self.board.rows - 1)][randint(0, self.board.cols - 1)]
        self.current = self.snake[-1]
        self.dir_array = get_path(self.food, self.snake)
        self.food_array = [self.food]
        self.clock = pygame.time.Clock()
        self.done = False

    def run(self):
        while not self.done:
            self.clock.tick(12)
            self.board.screen.fill(self.board.BLACK)
            self.board.draw_grid()

            direction = self.dir_array.pop(-1)
            if direction == 0:  # down
                self.snake.append(self.board.grid[self.current.x][self.current.y + 1])
            elif direction == 1:  # right
                self.snake.append(self.board.grid[self.current.x + 1][self.current.y])
            elif direction == 2:  # up
                self.snake.append(self.board.grid[self.current.x][self.current.y - 1])
            elif direction == 3:  # left
                self.snake.append(self.board.grid[self.current.x - 1][self.current.y])
            self.current = self.snake[-1]

            if self.current.x == self.food.x and self.current.y == self.food.y:
                while True:
                    self.food = self.board.grid[randint(0, self.board.rows - 1)][randint(0, self.board.cols - 1)]
                    if not (self.food.obstacle or self.food in self.snake):
                        break
                self.food_array.append(self.food)
                self.dir_array = get_path(self.food, self.snake)
            else:
                self.snake.pop(0)

            draw_path(self.snake, self.dir_array, self.board.screen, self.board.wr, self.board.hr)  # Draw the path

            # Draw the snake continuously
            for spot in self.snake:
                spot.show(self.board.WHITE)
            self.snake[-1].show(self.board.WHITE)  # Draw the head of the snake in white

            for i in range(self.board.rows):
                for j in range(self.board.cols):
                    if self.board.grid[i][j].obstacle:
                        self.board.grid[i][j].show(self.board.RED)

            self.food.show(self.board.GREEN)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.done = True
                elif event.type == KEYDOWN:
                    if event.key == K_w and not direction == 0:
                        direction = 2
                    elif event.key == K_a and not direction == 1:
                        direction = 3
                    elif event.key == K_s and not direction == 2:
                        direction = 0
                    elif event.key == K_d and not direction == 3:
                        direction = 1
