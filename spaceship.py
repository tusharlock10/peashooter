import math

import pygame


class Spaceship:
    def __init__(
        self, x, y, width, height, color, screen_width, screen_height, speed=5
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = speed
        self.health = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def move(self, keys):
        x_move, y_move = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x_move -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x_move += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            y_move -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            y_move += self.speed

        # Normalize diagonal movement
        if x_move != 0 and y_move != 0:
            x_move /= math.sqrt(2)
            y_move /= math.sqrt(2)

        self.x = max(min(self.x + x_move, self.screen_width - self.width), 0)
        self.y = max(min(self.y + y_move, self.screen_height - self.height), 0)

    def get_data(self):
        return f"{self.x},{self.y}"

    def get_darker_color(self):
        return tuple(max(component // 2, 0) for component in self.color)

    def get_position(self):
        return self.x, self.y
