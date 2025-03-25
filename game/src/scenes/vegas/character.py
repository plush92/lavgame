import pygame
import sys
import random
import time
from pygame.math import Vector2
from src.scenes.vegas.brick import Brick
from src.scenes.vegas.paper import Paper
from src.scenes.vegas.player import Player
from src.scenes.vegas.wall import Wall

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

class Character: # Character class for the player and enemies in the wall game scene
    def __init__(self, name, x, y, color): # Initialize the character with a name, position, and color
        self.name = name # Name of the character
        self.pos = Vector2(x, y) # Position of the character, (x, y) coordinates on the screen
        self.color = color # Color of the character (RGB tuple) 
        self.size = 40 
        
    def draw(self): # Draw the character on the screen 
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.size) # Draw a circle for the character, (surface, color, (x, y), radius)
        # int(self.pos.x) and int(self.pos.y) are the center of the circle, self.size is the radius
        # The circle is filled with the character's color and at its position with the specified size
        name_text = font_small.render(self.name, True, WHITE) # Render the character's name with the font_small font and white color 
        screen.blit(name_text, (int(self.pos.x - name_text.get_width() / 2), # Blit the name text to the screen at the center horizontally and 10 pixels above the character
                               int(self.pos.y + self.size + 5))) # pos.y + size is the bottom of the circle, +5 is the margin between the circle and text