import pygame
import sys
import random
import time
import math
from pygame.math import Vector2
from src.scenes.vegas.paper import Paper
from src.scenes.vegas.wall import Wall

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tim and Lav in Vegas")
clock = pygame.time.Clock()

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

class Character(pygame.sprite.Sprite):
    def __init__(self, name, x, y, color, image_path=None):
        super().__init__()
        self.name = name
        self.image_path = image_path  # Path to the character's image
        self.image = pygame.Surface((50, 50))  # Default surface if no image is provided
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Load the character's image if a path is provided
        if self.image_path:
            self.load_image()

        # Animation variables
        self.swinging = False
        self.swing_timer = 0
        self.swing_duration = 500  # ms
        self.hammer_image = pygame.Surface((30, 10))
        self.hammer_image.fill((150, 75, 0))  # Brown hammer
        self.hammer_rect = self.hammer_image.get_rect()
        
        # Movement variables
        self.speed = 200  # Speed in pixels per second
        self.has_hit_wall_this_swing = False

    def load_image(self):
        """Load the character's image from the given path."""
        try:
            loaded_image = pygame.image.load(self.image_path).convert_alpha()
            self.image = pygame.transform.scale(loaded_image, (50, 50))  # Scale to fit the character size
        except pygame.error as e:
            print(f"Error loading image for {self.name}: {e}")
            # Fallback to default surface if loading fails
            self.image.fill((255, 0, 0))  # Fill with red to indicate an error

    def swing(self):
        """Start swinging the hammer if not already swinging"""
        if not self.swinging:
            self.swinging = True
            self.swing_timer = pygame.time.get_ticks()
            self.has_hit_wall_this_swing = False
            return True
        return False

    def check_wall_hit(self, wall):
        """Check if the hammer hits the wall"""
        if wall.is_destroyed or self.has_hit_wall_this_swing:
            return False
        if self.swinging and wall.rect.colliderect(self.hammer_rect):
            # Only count hits at the peak of the swing (around 250ms in)
            swing_progress = pygame.time.get_ticks() - self.swing_timer
            if 200 <= swing_progress <= 300:
                self.has_hit_wall_this_swing = True
                return True
        return False

    def move(self, dt):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed * dt
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed * dt
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed * dt

        # Update position
        self.rect.x += dx
        self.rect.y += dy
        
        # Keep within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def update(self, dt):
        # Update swing animation
        if self.swinging:
            elapsed = pygame.time.get_ticks() - self.swing_timer
            if elapsed > self.swing_duration:
                self.swinging = False
            
            # Update hammer position based on swing animation
            self._update_hammer_position(elapsed)
            
        self.move(dt)
        if not self.swinging:
            self.has_hit_wall_this_swing = False
    
    def _update_hammer_position(self, elapsed):
        """Update the hammer position based on the swing animation progress"""
        # Calculate swing progress (0 to 1)
        progress = min(1.0, elapsed / self.swing_duration)
        
        # Use sine function for smooth back-and-forth swing motion
        # Maps 0-1 to 0-π so we get a half sine wave
        angle = -90 + (progress * 180)  # -90 to 90 degrees
        
        # Convert to radians
        angle_rad = angle * (math.pi / 180)
        
        # Calculate hammer position
        hammer_length = 50  # Length of the hammer from character center
        
        # Calculate offset from character center
        offset_x = hammer_length * math.cos(angle_rad)
        offset_y = hammer_length * math.sin(angle_rad)
        
        # Position hammer at end of calculated position
        self.hammer_rect.center = (
            self.rect.centerx + offset_x,
            self.rect.centery + offset_y
        )

    def draw(self, surface, dt, offset_x=0, offset_y=0):
        # Draw character with shake effect
        adjusted_rect = self.rect.move(offset_x, offset_y)
        surface.blit(self.image, adjusted_rect)

        # Draw name (adjusted for shake)
        font = pygame.font.SysFont('Arial', 16)
        name_text = font.render(self.name, True, BLACK)
        name_rect = name_text.get_rect(centerx=adjusted_rect.centerx, bottom=adjusted_rect.top - 5)
        surface.blit(name_text, name_rect)

        # Draw hammer if swinging (adjusted for shake)
        if self.swinging:
            elapsed = pygame.time.get_ticks() - self.swing_timer
            progress = min(1.0, elapsed / self.swing_duration)
            angle = -90 + (progress * 180)  # -90 to 90 degrees

            # Rotate hammer image
            rotated_hammer = pygame.transform.rotate(self.hammer_image, -angle)
            rotated_rect = rotated_hammer.get_rect(center=self.hammer_rect.center)

            # Apply offset to hammer
            rotated_rect.x += offset_x
            rotated_rect.y += offset_y

            # Draw rotated hammer
            surface.blit(rotated_hammer, rotated_rect)
