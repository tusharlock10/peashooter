import math

import pygame
from constants import ID_COLOR_MAP, SCREEN_HEIGHT, SCREEN_WIDTH


class Spaceship:
    def __init__(
        self,
        ship_id,
        width=50,
        height=50,
        speed=5,
        health=100,
        start_x=SCREEN_WIDTH // 2,
        start_y=SCREEN_HEIGHT // 2,
    ):
        self.ship_id = ship_id
        self.x = start_x
        self.y = start_y
        self.width = width
        self.height = height
        self.speed = speed
        self.health = health
        self.color = ID_COLOR_MAP[ship_id]

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

        self.x = max(min(self.x + x_move, SCREEN_WIDTH - self.width), 0)
        self.y = max(min(self.y + y_move, SCREEN_HEIGHT - self.height), 0)

    def get_data(self):
        return f"{self.x},{self.y}"

    def get_darker_color(self):
        return tuple(max(component // 2, 0) for component in self.color)

    def get_position(self):
        return self.x, self.y