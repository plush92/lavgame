import pygame
import random
import math
import sys
import os

# Define the assets directory
assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../src/assets"))

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

# Character class
class Character:
    def __init__(self, x, y, color, is_player=False, image_path=None, name=None):
        self.x = x
        self.y = y
        self.color = color
        self.width = 60
        self.height = 50
        self.speed = 3
        self.health = 100
        self.is_player = is_player
        self.punching = False
        self.punch_timer = 0
        self.direction = 1  # 1 for right, -1 for left
        self.image = None
        self.name = name
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  # Add rect attribute
        if image_path:
            self.load_image(image_path)
        else:
            self.create_placeholder_image()  # Create a placeholder if no image is provided

    def load_image(self, path):
        try:
            # Construct the full path to the image using assets_dir
            full_path = os.path.join(assets_dir, path)
            print(f"Loading image from: {full_path}")  # Debugging
            self.image = pygame.image.load(full_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            # Create flipped version for left direction
            self.image_flipped = pygame.transform.flip(self.image, True, False)
            print(f"Successfully loaded image: {full_path}")  # Debugging
        except pygame.error as e:
            print(f"Error loading image {full_path}: {e}")
            self.create_placeholder_image()  # Use a placeholder if the image fails to load

    def create_placeholder_image(self):
        """Create a placeholder image if the actual image fails to load."""
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.image_flipped = pygame.transform.flip(self.image, True, False)

    def draw(self, surface):
        if self.image:
            # Use the appropriate image based on direction
            img_to_draw = self.image if self.direction == -1 else self.image_flipped
            surface.blit(img_to_draw, (self.rect.x, self.rect.y))
        else:
            # Draw rectangle for player or if image failed to load
            pygame.draw.rect(surface, self.color, self.rect)
            
            # Eyes (to show direction)
            eye_color = WHITE
            eye_size = 10
            eye_offset = 15 if self.direction == 1 else 25
            pygame.draw.circle(surface, eye_color, (self.rect.x + eye_offset, self.rect.y + 15), eye_size)
        
        # Draw punch effect when punching
        if self.punching:
            punch_color = (255, 165, 0)  # Orange
            punch_size = 20
            if self.direction == 1:  # Facing right
                pygame.draw.rect(surface, punch_color, 
                                 (self.rect.x + self.width, self.rect.y + self.height//3, punch_size, self.height//3))
            else:  # Facing left
                pygame.draw.rect(surface, punch_color, 
                                 (self.rect.x - punch_size, self.rect.y + self.height//3, punch_size, self.height//3))

    def move(self, dx, dy, props):
        # Tentatively update position
        new_x = self.rect.x + dx * self.speed
        new_y = self.rect.y + dy * self.speed

        print(f"Tentative position: ({new_x}, {new_y})")  # Debugging

        # Check collisions with props
        for prop in props:
            if prop.type == "floor" and not prop.check_collision(new_x, new_y, self.width, self.height):
                print(f"Collision with floor at ({new_x}, {new_y}), movement restricted")
                return  # Cancel movement
            if prop.type == "table" and prop.check_collision(new_x, new_y, self.width, self.height):
                print(f"Collision with table at ({new_x}, {new_y}), movement restricted")
                return  # Cancel movement

        # If no collisions, update position
        self.rect.x = new_x
        self.rect.y = new_y
        print(f"Player moved to ({self.rect.x}, {self.rect.y})")  # Debugging

        # Update direction based on movement
        if dx > 0:
            self.direction = 1  # Facing right
        elif dx < 0:
            self.direction = -1  # Facing left

    def check_collision(self, x, y, width, height):
        collision = (self.rect.x < x + width and
                    self.rect.x + self.width > x and
                    self.rect.y < y + height and
                    self.rect.y + self.height > y)
        print(f"Checking collision with {self.type}: {collision} (Player: x={x}, y={y}, width={width}, height={height}, Prop: x={self.rect.x}, y={self.rect.y}, width={self.width}, height={self.height})")  # Debugging
        return collision