import pygame
import random
import math
import sys
import os

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

WIDTH, HEIGHT = 800, 600

class Kitchen:
    def __init__(self):
        self.image = None

    def load_image(self, path):
        try:
            self.image = pygame.image.load(path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            self.image = None
    
    def load_kitchen_image(self):
        image = self.load_image("assets/kitchen.png")
        # assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))  # Path to the assets directory
        kitchen_image = pygame.image.load("assets/kitchen.png")  # Load the highway top image
        return pygame.transform.scale(kitchen_image, (WIDTH, 100))  # Scale the image to fit the screen width

# Kitchen Props Class
class KitchenProp:
    def __init__(self, x, y, width, height, color, prop_type, image_path=None, render_image=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.type = prop_type  # "fridge", "table", "cabinet"
        self.image = None
        self.render_image = render_image
        if image_path:
            self.load_image(image_path)

    def load_image(self, path):
        try:
            self.image = pygame.image.load(path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            self.image = None
    
    def load_kitchen_image(self):
        image = self.load_image("assets/kitchen.png")
        # assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))  # Path to the assets directory
        kitchen_image = pygame.image.load("assets/kitchen.png")  # Load the highway top image
        return pygame.transform.scale(kitchen_image, (WIDTH, 100))  # Scale the image to fit the screen width

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

            if self.type == "kitchen":
                self.load_kitchen_image
            
            # Add details based on type
            if self.type == "fridge":
                # Door handle
                self.load_image("assets/fridge.png")
            elif self.type == "table":
                # Table legs
                leg_width = 10
                leg_height = 30
                pygame.draw.rect(surface, self.color, (self.x, self.y + self.height, leg_width, leg_height))
                pygame.draw.rect(surface, self.color, (self.x + self.width - leg_width, self.y + self.height, leg_width, leg_height))
                pygame.draw.rect(surface, self.color, (self.x, self.y + self.height + leg_height, self.width, 5))

            elif self.type == "cabinet":
                # Cabinet handles
                
                self.load_image("assets/cabinet.png")

    def check_collision(self, character):
        return (self.x < character.x + character.width and
                self.x + self.width > character.x and
                self.y < character.y + character.height and
                self.y + self.height > character.y)