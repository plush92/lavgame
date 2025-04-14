import pygame
import random
import math
import sys
import os
from src.scenes.fight.character import Character
from src.scenes.fight.kitchen import Kitchen
from src.scenes.fight.dialogue import DialogSystem
from src.scenes.fight.fridgeitem import FridgeItem
from src.scenes.fight.kitchen import Kitchen

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

#door - 111x202
#table - 309x142
#fridge - 88x223
#floor - 728-368

# Kitchen Props Class
# Items around the kitchen for collision detection
class KitchenProp:
    def __init__(self, x, y, width, height, prop_type, image_path=None, render_image=False):
        self.x = x  # X position of the prop
        self.y = y  # Y position of the prop
        self.width = width  # Width of the prop
        self.height = height  # Height of the prop
        self.type = prop_type  # "fridge", "table", "cabinet"
        self.image = None  # Image of the prop
        self.render_image = render_image  # Whether to render the image or not
        if image_path:
            self.load_image(image_path)

    def load_image(self, path):
        try:
            self.image = pygame.image.load(path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            self.image = None

    def draw_debug(self, surface):
        """
        Draws the collision box as a rectangle for debugging purposes.

        Args:
            surface (pygame.Surface): The surface to draw on.
        """
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.width, self.height), 2)  # Red outline

    def draw(self, surface):
        """
        Draws the prop only if it has an image or for debugging purposes.
        """
        if self.render_image and self.image:
            surface.blit(self.image, (self.x, self.y))  # Draw the image if available
        else:
            # Skip drawing if no image and not debugging
            pass

    def check_collision(self, x, y, width, height):
        return (self.x < x + width and
                self.x + self.width > x and
                self.y < y + height and
                self.y + self.height > y)
    
    def create_game_objects():
        """Create all game objects including characters and collision props."""
        # Create dialog system
        dialog_system = DialogSystem(WIDTH, HEIGHT)
        
        # Create characters
        player = Character(100, HEIGHT // 2, BLUE, is_player=True, image_path="mc_walk_f1.png", name="Tim")
        dad = Character(WIDTH - 250, HEIGHT // 2, RED, is_player=False, image_path="dad.png", name="Dad")

        # Create kitchen background
        kitchen = Kitchen(WIDTH, HEIGHT, "assets/kitchen.png")
        
        # Define collision props (manually eyeballed positions)
        #(x, y, width, height) - make slightly smaller to account for player box
        door = KitchenProp(665, 25, 90, 180, prop_type="door")  #x, y, width, height, color, type
        table = KitchenProp(275, 325, 240, 110, prop_type="table")  #original 309, 142
        fridge = KitchenProp(710, 300, 50, 200, prop_type="fridge") # original 88, 223
        floor = KitchenProp(100, 272, 675, 290, prop_type="floor")  # original 728, 368

        props = [door, table, fridge, floor]
        # Return all objects
        return dialog_system, player, dad, kitchen, [door, table, fridge, floor]