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

# Fridge Minigame Items
class FridgeItem:
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.item_type = item_type  # "tortellini" or "other"
        
        # Assign color based on type
        if item_type == "tortellini":
            self.color = YELLOW
        else:
            # Random food colors
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
            self.color = random.choice(colors)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        
        # Add some visual distinction for tortellini
        if self.item_type == "tortellini":
            # Draw pasta shape
            pygame.draw.circle(surface, (220, 200, 150), (self.x + self.width//2, self.y + self.height//2), self.width//3)
            pygame.draw.circle(surface, self.color, (self.x + self.width//2, self.y + self.height//2), self.width//4)
        else:
            # Draw generic food shape - Fix: Ensure color values don't go below 0
            darker_color = (max(0, self.color[0]-40), max(0, self.color[1]-40), max(0, self.color[2]-40))
            pygame.draw.rect(surface, darker_color, (self.x + 5, self.y + 5, self.width - 10, self.height - 10))