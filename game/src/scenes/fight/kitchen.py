import pygame
import random
import math
import sys

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
LIGHT_BLUE = (135, 206, 235)
BROWN = (139, 69, 19)
LIGHT_GRAY = (220, 220, 220)
YELLOW = (255, 255, 0)

# Game states
KITCHEN = 0
FRIDGE_MINIGAME = 1
DIALOG = 2
FIGHTING = 3
GAME_OVER = 4

class Kitchen:
    def __init__(self, width, height, image_path):
        self.width = width
        self.height = height
        self.image = None
        self.image_path = image_path
        self.load_image()

    def load_image(self):
        try:
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except pygame.error as e:
            print(f"Error loading kitchen background image {self.image_path}: {e}")
            self.image = None

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, (0, 0))
        else:
            # Fallback to a solid color if the image fails to load
            pygame.draw.rect(surface, LIGHT_GRAY, (0, 0, self.width, self.height))