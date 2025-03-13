import pygame
import random
import sys
import time
from src.scenes.bar.walls import create_labyrinth_walls

# Screen Setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bar Escape: Hometown Honkey Tonk")
# Create the walls
WALLS = create_labyrinth_walls()

class Collectable:
    def __init__(self, x, y, type_name, color):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.collected = False
        self.type = type_name
        self.color = color
    
    def draw(self, screen):
        if not self.collected:
            pygame.draw.rect(screen, self.color, self.rect)