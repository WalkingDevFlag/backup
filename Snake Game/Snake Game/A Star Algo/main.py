import pygame
from pygame import display, time, QUIT, init, KEYDOWN, K_a, K_s, K_d, K_w
from snake import SnakeGame

init()

def main():
    pygame.init()

    snake_game = SnakeGame()
    snake_game.run()

if __name__ == "__main__":
    main()
