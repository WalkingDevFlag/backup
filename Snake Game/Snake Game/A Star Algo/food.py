import pygame
from random import randint
from board import Board

class Food:
    def __init__(self, board):
        self.board = board
        self.food = self.board.grid[randint(0, self.board.rows - 1)][randint(0, self.board.cols - 1)]

    def generate_food(self):
        while True:
            self.food = self.board.grid[randint(0, self.board.rows - 1)][randint(0, self.board.cols - 1)]
            if not (self.food.obstacle or self.food in self.snake):
                break
