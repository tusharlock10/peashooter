import math

import pygame


class Bullet:
    def __init__(self, x, y, radius, color, direction, speed=10):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.speed = speed

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move(self):
        normalized_direction = self.normalize_direction(self.direction)
        self.x += normalized_direction[0] * self.speed
        self.y += normalized_direction[1] * self.speed

    def off_screen(self, width, height):
        return self.x < 0 or self.x > width or self.y < 0 or self.y > height

    def get_data(self):
        return f"{self.x},{self.y},{self.direction[0]},{self.direction[1]}"

    @staticmethod
    def normalize_direction(direction):
        if direction[0] != 0 and direction[1] != 0:
            return [component / math.sqrt(2) for component in direction]
        return direction
