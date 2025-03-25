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

class Player: # Player class for the hammer-wielding character
    def __init__(self): # Initialize the player
        self.pos = Vector2(WIDTH // 2, HEIGHT - 100) # Starting position at the bottom center of the screen
        self.hammer_img = self._create_hammer_image() # Create the hammer image, call the _create_hammer_image function
        self.stamina = 100 # Player's stamina
        self.max_stamina = 100 # Maximum stamina
        self.hammer_angle = 0 # Angle of the hammer
        self.swinging = False # Flag for swinging animation
        self.swing_timer = 0 # Timer for swinging animation
        self.cooldown = False # Flag for cooldown
        self.cooldown_timer = 0 # Timer for cooldown
        
    def _create_hammer_image(self): # Create a simple hammer shape
        surf = pygame.Surface((60, 20), pygame.SRCALPHA) # Create a transparent surface, SRCALPHA for transparency, RGBA for color, and RGB for no transparency, no alpha channel
        pygame.draw.rect(surf, GRAY, (0, 5, 40, 10)) # Draw the handle of the hammer, (surface, color, (x, y, width, height)) 
        pygame.draw.rect(surf, (50, 50, 50), (40, 0, 20, 20)) # Draw the head of the hammer 
        return surf
        
    def update(self, dt): # Update the player's position and state based on time
        mouse_pos = pygame.mouse.get_pos() # Get the mouse position (x, y) on the screen 
        # Point hammer toward mouse
        direction = Vector2(mouse_pos) - self.pos # Calculate the direction vector from the player to the mouse 
        self.hammer_angle = direction.angle_to(Vector2(1, 0)) # Calculate the angle of the hammer based on the direction vector
        
        # Handle swinging animation
        if self.swinging: # If the player is swinging the hammer 
            self.swing_timer += dt # Increment the swing timer
            if self.swing_timer >= 300: # If the swing timer reaches 300 milliseconds 
                self.swinging = False # Stop swinging
                self.swing_timer = 0 # Reset the swing timer
                self.cooldown = True # Start the cooldown
                self.cooldown_timer = 0 # Reset the cooldown timer
                
        # Handle cooldown
        if self.cooldown: # If the player is in cooldown
            self.cooldown_timer += dt # Increment the cooldown timer
            self.stamina += dt * 0.05  # Recover stamina during cooldown
            if self.cooldown_timer >= 1000:  # 1 second cooldown
                self.cooldown = False # End cooldown
                
        # Cap stamina
        self.stamina = min(self.max_stamina, self.stamina) # Cap the stamina at the maximum value
        
    def move(self, direction): # Move the player in a direction
        speed = 5 # Movement speed
        self.pos += direction * speed # Move the player in the specified direction with the specified speed
        # Keep player within bounds
        self.pos.x = max(50, min(WIDTH - 50, self.pos.x)) # Keep the player within the left and right bounds
        self.pos.y = max(HEIGHT // 2, min(HEIGHT - 50, self.pos.y)) # Keep the player within the top and bottom bounds
        
    def swing(self): # Swing the hammer
        if not self.cooldown and not self.swinging and self.stamina >= 20: # If not in cooldown, not swinging, and enough stamina
            self.swinging = True # Start swinging
            self.stamina -= 20 # Reduce stamina
            return True # Swing successful
        return False # Swing unsuccessful
        
    def draw(self): # Draw the player, hammer, and stamina bar
        # Draw player
        pygame.draw.circle(screen, GREEN, (int(self.pos.x), int(self.pos.y)), 20) # Draw the player as a green circle
        
        # Draw hammer
        rotated_hammer = pygame.transform.rotate(self.hammer_img, self.hammer_angle) # Rotate the hammer image based on the hammer angle
        hammer_pos = self.pos + Vector2(30, 0).rotate(-self.hammer_angle) # Calculate the position of the hammer
        hammer_rect = rotated_hammer.get_rect(center=hammer_pos) # Get the rectangle of the rotated hammer centered at the hammer position
        screen.blit(rotated_hammer, hammer_rect) # Blit the rotated hammer to the screen at the hammer position
        
        # Draw stamina bar
        bar_width = 100 # Width of the stamina bar
        bar_height = 10 # Height of the stamina bar
        stamina_rect = pygame.Rect(self.pos.x - bar_width // 2, self.pos.y + 30, bar_width, bar_height) # Rectangle for the stamina bar
        pygame.draw.rect(screen, RED, stamina_rect) # Draw the stamina bar
        fill_width = int(bar_width * (self.stamina / self.max_stamina)) # Calculate the width of the filled portion of the stamina bar
        fill_rect = pygame.Rect(self.pos.x - bar_width // 2, self.pos.y + 30, fill_width, bar_height) # Rectangle for the filled portion
        pygame.draw.rect(screen, GREEN, fill_rect) # Draw the filled portion of the stamina bar
        pygame.draw.rect(screen, BLACK, stamina_rect, 1) # Draw the outline of the stamina bar