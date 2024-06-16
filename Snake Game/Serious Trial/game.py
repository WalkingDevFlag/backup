import pygame
from snake import Snake
from board import Board

class Game:
    def __init__(self):
        self.initialize()

    def initialize(self):
        # Initialize Pygame
        pygame.init()

        # Set up display
        self.width, self.height = 640, 480
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")

        # Game settings
        self.block_size = 20
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 35)

        # Initialize snake and board
        self.snake = Snake(self.width, self.height, self.block_size)
        self.board = Board(self.width, self.height, self.block_size)

    def run(self):
        game_over = False
        game_close = False

        while not game_over:
            while game_close:
                self.window.fill(self.board.black)
                self.show_game_over_message()
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = True
                        game_close = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        elif event.key == pygame.K_r:
                            self.initialize()
                            game_close = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                self.snake.handle_input(event)

            self.snake.update()

            # Check for collisions
            if self.snake.check_collision():
                game_close = True

            # Check if snake eats food
            if self.snake.head_position() == (self.board.food_x, self.board.food_y):
                self.board.food_x, self.board.food_y = self.board.generate_food_position()
                self.snake.grow()

            # Draw the game
            self.window.fill(self.board.black)
            self.board.draw_grid(self.window)
            self.board.draw_food(self.window)
            self.snake.draw(self.window)
            pygame.display.update()

            # Control the game speed
            self.clock.tick(15)

        pygame.quit()
        quit()

    def show_game_over_message(self):
        game_over_text = self.font.render("Game Over! Press R to Restart", True, self.board.red)
        self.window.blit(game_over_text, [self.width / 6, self.height / 3])
