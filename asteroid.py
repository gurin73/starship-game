import pygame
import random


SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
RED = (255, 0, 0)


# астероиды
import pygame
import random

RED = (255, 0, 0)
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

class Asteroid:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = -self.height
        self.speed = random.randint(2, 4)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):  # <-- Добавил параметр screen
        pygame.draw.rect(screen, RED, self.rect)

    def move(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)
