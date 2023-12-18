import math

import pygame
from constants import ID_COLOR_MAP, NetworkEvents


class Bullet:
    def __init__(self, ship_id, x, y, direction, radius=7, speed=12, damage=10):
        self.ship_id = ship_id
        self.x = x
        self.y = y
        self.radius = radius
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.color = self.get_darker_color(ship_id)

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

    def get_bullet_data(self):
        return {
            "ship_id": self.ship_id,
            "x": self.x,
            "y": self.y,
            "direction": self.direction,
        }

    def create_bullet_network_event(self):
        event = NetworkEvents.CREATE_BULLET.value
        event["value"] = self.get_bullet_data()
        return event

    @staticmethod
    def get_darker_color(ship_id):
        color = ID_COLOR_MAP[ship_id]
        dark_color = tuple(max(component // 2, 0) for component in color)
        return dark_color

    @staticmethod
    def normalize_direction(direction):
        if direction[0] != 0 and direction[1] != 0:
            return [component / math.sqrt(2) for component in direction]
        return direction
