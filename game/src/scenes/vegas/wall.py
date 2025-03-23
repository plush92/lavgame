import pygame
import sys
import random
import time
from pygame.math import Vector2
from src.scenes.vegas.brick import Brick

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

class Wall:
    def __init__(self):
        self.bricks = []
        brick_width = 40
        brick_height = 20
        wall_x = WIDTH // 2 - (brick_width * 3) // 2
        
        # Create brick pattern
        for row in range(15):
            for col in range(3):
                # Stagger the bricks in alternating rows
                offset = brick_width // 2 if row % 2 else 0
                x = wall_x + col * brick_width + offset
                y = 100 + row * brick_height
                self.bricks.append(Brick(x, y, brick_width, brick_height))
    
    def draw(self):
        for brick in self.bricks:
            brick.draw()
            
    def hit(self, x, y):
        hit_any = False
        for brick in self.bricks[:]:
            if brick.rect.collidepoint(x, y):
                if brick.hit(random.randint(30, 60)):
                    self.bricks.remove(brick)
                hit_any = True
                break
        return hit_any, len(self.bricks) == 0
