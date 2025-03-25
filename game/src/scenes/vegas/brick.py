import pygame
import sys
import random
import time
from pygame.math import Vector2

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tim and Lav in Vegas")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
BRICK_COLOR = (165, 42, 42)
GRAY = (150, 150, 150)

# Fonts
font_small = pygame.font.SysFont('Arial', 20)
font_medium = pygame.font.SysFont('Arial', 28)
font_large = pygame.font.SysFont('Arial', 36)

# Game states
STATE_DIALOGUE = 0
STATE_WALL_GAME = 1
STATE_ENDING = 2
game_state = STATE_DIALOGUE

class Brick:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.health = 100
        self.cracked = False
        
    def hit(self, damage):
        self.health -= damage
        if self.health <= 50:
            self.cracked = True
        return self.health <= 0
        
    def draw(self):
        if self.cracked:
            pygame.draw.rect(screen, (120, 30, 30), self.rect)
            # Draw crack lines
            start_pos = (self.rect.x + 5, self.rect.y + 5) # Top left
            end_pos = (self.rect.x + self.rect.width - 5, self.rect.y + self.rect.height - 5) # Bottom right
            pygame.draw.line(screen, BLACK, start_pos, end_pos, 2) # Main crack
            pygame.draw.line(screen, BLACK, # Secondary crack
                            (self.rect.x + self.rect.width - 5, self.rect.y + 5), # Top right
                            (self.rect.x + 5, self.rect.y + self.rect.height - 5), 2) # Bottom left
        else: # Draw normal brick
            pygame.draw.rect(screen, BRICK_COLOR, self.rect) # Draw brick
        pygame.draw.rect(screen, BLACK, self.rect, 2) # Draw outline
