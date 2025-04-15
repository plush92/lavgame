import pygame  # Import the Pygame library for graphics and game development
import random  # Import random for potential randomness in behavior (not used yet)
import math  # Import math for angle calculations
import os

# Screen Setup
SCREEN_WIDTH = 800  # Define screen width
SCREEN_HEIGHT = 600  # Define screen height
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create the game window
pygame.display.set_caption("Bar Escape: Hometown Honkey Tonk")  # Set the window title

class Bouncer:
    def __init__(self, x, y, image_path=None):
        """Initialize the bouncer character.""" 
        self.x = x  # Initial x-coordinate of the bouncer
        self.y = y  # Initial y-coordinate of the bouncer
        self.speed = 1.5  # Speed of the bouncer
        self.width = 50  # Width of the bouncer
        self.height = 50  # Height of the bouncer
        self.rect = pygame.Rect(x, y, self.width, self.height)  # Create a rectangle to represent the bouncer's position
        self.direction = 1  # Direction of movement (1 for right, -1 for left)
        self.can_move = False  # Flag to determine if the bouncer can move
        self.stuck_timer = 0  # Timer to track how long the bouncer is stuck
        self.last_position = (x, y)  # Store the last position of the bouncer
        self.image = None  # Placeholder for the bouncer's image
        if image_path:  # If an image path is provided
            self.load_image(image_path)  # Load the image

    def load_image(self, path):
        """Load the bouncer's image from the given path."""
        try:
            self.image = pygame.image.load(path).convert_alpha()  # Load the image with transparency
            self.image = pygame.transform.scale(self.image, (self.width, self.height))  # Scale the image to fit the bouncer's dimensions
            self.image_flipped = pygame.transform.flip(self.image, True, False)  # Create a flipped version for left direction
        except pygame.error as e:  # Handle errors if the image fails to load
            print(f"Error loading image {path}: {e}")
            self.image = None  # Set the image to None if loading fails

    def draw(self, surface):
        """Draw the bouncer on the given surface."""
        if self.image:  # If an image is loaded
            img_to_draw = self.image_flipped if self.direction == -1 else self.image  # Choose the correct image based on direction
            surface.blit(img_to_draw, (self.x, self.y))  # Draw the image at the bouncer's position

    def start_moving(self):
        """Allow the bouncer to start moving."""
        self.can_move = True  # Set the movement flag to True

    def move_towards_player(self, player, walls):
        """Move directly toward the player while avoiding walls."""
        if not self.can_move:
            return

        # Store the current position to check if we're stuck
        original_x = self.rect.x
        original_y = self.rect.y

        # Get the center points for more accurate targeting
        target_x = player.rect.centerx
        target_y = player.rect.centery
        current_x = self.rect.centerx
        current_y = self.rect.centery

        # Calculate direction vector toward player
        dx = target_x - current_x
        dy = target_y - current_y

        # Update facing direction for image
        if abs(dx) > 0.1:  # Only change direction with meaningful horizontal movement
            self.direction = 1 if dx > 0 else -1

        # Normalize direction vector
        distance = max(1, (dx**2 + dy**2) ** 0.5)
        dx = (dx / distance) * self.speed
        dy = (dy / distance) * self.speed

        # Try to move horizontally
        self.rect.x += dx
        x_collision = False
        for wall in walls:
            if self.rect.colliderect(wall):
                x_collision = True
                self.rect.x = original_x
                break

        # Try to move vertically
        self.rect.y += dy
        y_collision = False
        for wall in walls:
            if self.rect.colliderect(wall):
                y_collision = True
                self.rect.y = original_y
                break

        # If we're colliding in both directions, try to find a way around
        if x_collision and y_collision:
            self.stuck_timer += 1
            
            if self.stuck_timer > 10:  # If stuck for several frames
                # Try 4 alternate directions (clockwise)
                possible_moves = [
                    (self.speed, 0),      # Right
                    (0, self.speed),      # Down
                    (-self.speed, 0),     # Left
                    (0, -self.speed)      # Up
                ]
                
                for move_x, move_y in possible_moves:
                    self.rect.x = original_x + move_x
                    self.rect.y = original_y + move_y
                    
                    if not any(self.rect.colliderect(wall) for wall in walls):
                        # Found a valid move, reset stuck timer
                        self.stuck_timer = 0
                        break
                    else:
                        # Revert move and try the next option
                        self.rect.x = original_x
                        self.rect.y = original_y
        else:
            # We moved successfully, reset stuck timer
            self.stuck_timer = 0

        # Keep the bouncer within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # Update the drawing coordinates
        self.x = self.rect.x
        self.y = self.rect.y
        
        # Update last position
        self.last_position = (self.rect.x, self.rect.y)
