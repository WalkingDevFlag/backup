import pygame

class Snake:
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size

        # Initial position of the snake
        self.x = self.width / 2
        self.y = self.height / 2
        self.x_change = 0
        self.y_change = 0

        self.body = []
        self.length = 1

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.x_change == 0:
                self.x_change = -self.block_size
                self.y_change = 0
            elif event.key == pygame.K_RIGHT and self.x_change == 0:
                self.x_change = self.block_size
                self.y_change = 0
            elif event.key == pygame.K_UP and self.y_change == 0:
                self.y_change = -self.block_size
                self.x_change = 0
            elif event.key == pygame.K_DOWN and self.y_change == 0:
                self.y_change = self.block_size
                self.x_change = 0

    def update(self):
        # Update snake position
        self.x += self.x_change
        self.y += self.y_change

        # Update snake body
        snake_head = [self.x, self.y]
        self.body.append(snake_head)
        if len(self.body) > self.length:
            del self.body[0]

    def draw(self, window):
        # Draw the snake
        for segment in self.body:
            pygame.draw.rect(window, (255, 255, 255), [segment[0], segment[1], self.block_size, self.block_size])

    def head_position(self):
        return (self.x, self.y)

    def grow(self):
        self.length += 1

    def check_collision(self):
        # Check for wall collisions
        if self.x >= self.width or self.x < 0 or self.y >= self.height or self.y < 0:
            return True

        # Check for collisions with itself
        for segment in self.body[:-1]:
            if segment == [self.x, self.y]:
                return True

        return False
