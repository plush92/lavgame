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

class Paper:
    def __init__(self):
        self.pos = Vector2(random.randint(100, WIDTH - 100), random.randint(-200, -50))
        self.vel = Vector2(random.uniform(-1, 1), random.uniform(1, 3))
        self.rotation = random.randint(0, 360)
        self.rot_speed = random.uniform(-2, 2)
        self.size = Vector2(60, 80)
        self.paper_img = self._create_paper_image()
        
    def _create_paper_image(self):
        # Create a simple paper with text
        surf = pygame.Surface((int(self.size.x), int(self.size.y)), pygame.SRCALPHA)
        pygame.draw.rect(surf, WHITE, (0, 0, int(self.size.x), int(self.size.y)))
        pygame.draw.rect(surf, BLACK, (0, 0, int(self.size.x), int(self.size.y)), 1)
        
        # Add "DIVORCE" text to the paper
        text = font_small.render("DIVORCE", True, BLACK)
        surf.blit(text, (int(self.size.x/2 - text.get_width()/2), 10))
        
        # Add some lines for text
        for i in range(3):
            pygame.draw.line(surf, BLACK, (10, 30 + i*15), (int(self.size.x) - 10, 30 + i*15), 1)
        
        return surf
        
    def update(self):
        self.pos += self.vel
        self.rotation += self.rot_speed
        return self.pos.y > HEIGHT + 100
        
    def draw(self):
        rotated = pygame.transform.rotate(self.paper_img, self.rotation)
        pos = (int(self.pos.x), int(self.pos.y))
        rect = rotated.get_rect(center=pos)
        screen.blit(rotated, rect)
