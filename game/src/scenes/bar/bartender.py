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
GRAY = (100, 100, 100)
WALLS = create_labyrinth_walls()

class Bartender:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 40)
        self.color = GRAY
    
    def draw(self, screen):
        # Draw bartender body
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw head
        pygame.draw.circle(screen, self.color, (self.rect.centerx, self.rect.top - 10), 15)