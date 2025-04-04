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

# Character class
class Character:
    def __init__(self, x, y, color, is_player=False, image_path=None, name=None):
        self.x = x
        self.y = y
        self.color = color
        self.width = 75
        self.height = 75
        self.speed = 4
        self.health = 100
        self.is_player = is_player
        self.punching = False
        self.punch_timer = 0
        self.direction = 1  # 1 for right, -1 for left
        self.image = None
        self.name = name
        if image_path:
            self.load_image(image_path)

    def load_image(self, path):
        try:
            self.image = pygame.image.load(path).convert()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            # Create flipped version for left direction
            self.image_flipped = pygame.transform.flip(self.image, True, False)
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            self.image = None

    def draw(self, surface):
        if self.image:
            # Use the appropriate image based on direction
            img_to_draw = self.image_flipped if self.direction == -1 else self.image
            surface.blit(img_to_draw, (self.x, self.y))
        else:
            # Draw rectangle for player or if image failed to load
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
            
            # Eyes (to show direction)
            eye_color = WHITE
            eye_size = 10
            eye_offset = 15 if self.direction == 1 else 25
            pygame.draw.circle(surface, eye_color, (self.x + eye_offset, self.y + 15), eye_size)
        
        # Draw punch effect when punching
        if self.punching:
            punch_color = (255, 165, 0)  # Orange
            punch_size = 20
            if self.direction == 1:  # Facing right
                pygame.draw.rect(surface, punch_color, 
                                (self.x + self.width, self.y + self.height//3, punch_size, self.height//3))
            else:  # Facing left
                pygame.draw.rect(surface, punch_color, 
                                (self.x - punch_size, self.y + self.height//3, punch_size, self.height//3))

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        # Update direction based on movement
        if dx > 0:
            self.direction = 1
        elif dx < 0:
            self.direction = -1

    def check_collision(self, other):
        # Simple rectangle collision
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + self.height > other.y)
                
    def can_punch(self, other):
        # Check if in range to punch
        punch_range = 60
        if self.direction == 1:  # Facing right
            return (other.x > self.x and 
                    other.x - self.x < punch_range and
                    abs(self.y - other.y) < self.height)
        else:  # Facing left
            return (other.x < self.x and 
                    self.x - other.x < punch_range and
                    abs(self.y - other.y) < self.height)