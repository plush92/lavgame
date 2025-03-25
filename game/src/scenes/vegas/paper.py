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
font_small = pygame.font.SysFont('Arial', 12)
font_medium = pygame.font.SysFont('Arial', 28)
font_large = pygame.font.SysFont('Arial', 36)

# Game states
STATE_DIALOGUE = 0
STATE_WALL_GAME = 1
STATE_ENDING = 2
game_state = STATE_DIALOGUE

class Paper: # Paper class for the divorce papers
    def __init__(self): # Initialize the paper
        self.pos = Vector2(random.randint(100, WIDTH - 100), random.randint(-200, -50)) # Random position at the top of the screen, (x, y), 100 to WIDTH-100 for x, -200 to -50 for y
        self.vel = Vector2(random.uniform(-1, 1), random.uniform(1, 3)) # Random velocity downwards with slight horizontal movement, negative for up, positive for down, 0 for no movement, 1 for slow, 3 for fast
        self.rotation = random.randint(0, 360) # Random rotation angle. 0 is upright, 90 is sideways, 180 is upside down, 270 is other sideways, 360 is upright again, etc.
        self.rot_speed = random.uniform(-2, 2) # Random rotation speed. Negative for counter-clockwise, positive for clockwise, 0 for no rotation, and 2 for fast rotation, 0.5 for slow
        self.size = Vector2(60, 80) # Size of the paper 
        self.paper_img = self._create_paper_image() # Create the paper image, call the _create_paper_image function 
        
    def _create_paper_image(self): 
        # Create a simple paper with text and lines 
        surf = pygame.Surface((int(self.size.x), int(self.size.y)), pygame.SRCALPHA) # Create a transparent surface, SRCALPHA for transparency, RGBA for color, and RGB for no transparency, no alpha channel
        pygame.draw.rect(surf, WHITE, (0, 0, int(self.size.x), int(self.size.y))) # Draw a white rectangle for the paper, (surface, color, (x, y, width, height)), (0, 0) is the top left corner, (size.x, size.y) is the bottom right corner
        pygame.draw.rect(surf, BLACK, (0, 0, int(self.size.x), int(self.size.y)), 1) # Draw a black outline for the paper, (surface, color, (x, y, width, height), thickness), 1 for thin outline
        
        # Add "DIVORCE" text to the paper
        text = font_small.render("DIVORCE", True, BLACK) # Render the text "DIVORCE" with the font_small font and black color
        surf.blit(text, (int(self.size.x/2 - text.get_width()/2), 10)) # Blit the text to the surface at the center horizontally and 10 pixels from the top
        
        # Add some lines for text
        for i in range(3): # Loop 3 times
            pygame.draw.line(surf, BLACK, (10, 30 + i*15), (int(self.size.x) - 10, 30 + i*15), 1) # Draw a line from (10, 30 + i*15) to (size.x - 10, 30 + i*15), 1 for thin line
            # 30 + i*15 is the vertical position of the line, 30 for the first line, 45 for the second line, 60 for the third line
            # i*15 is the spacing between lines, 0 for the first line, 15 for the second line, 30 for the third line
            # 10 is the left margin, size.x - 10 is the right margin
            # (10, 30 + i*15) is the start position, (size.x - 10, 30 + i*15) is the end position
            # 1 is the thickness of the line
            # BLACK is the color of the line
        
        return surf # Return the paper surface
        
    def update(self): # Update the paper position and rotation
        self.pos += self.vel # Add the velocity to the position, move the paper, (x, y) + (x, y) = (x + x, y + y), (1, 2) + (3, 4) = (1 + 3, 2 + 4) = (4, 6)
        self.rotation += self.rot_speed # Add the rotation speed to the rotation angle, rotate the paper, 0 + 2 = 2, 90 + (-2) = 88, 180 + 0 = 180, 270 + 2 = 272
        return self.pos.y > HEIGHT + 100 # Return True if the paper is below the screen, False if the paper is still on the screen
        
    def draw(self): # Draw the paper on the screen
        rotated = pygame.transform.rotate(self.paper_img, self.rotation) # Rotate the paper image by the rotation angle, create a new rotated image
        pos = (int(self.pos.x), int(self.pos.y)) # Convert the position to integers, (x, y), (1.5, 2.7) = (1, 2)
        rect = rotated.get_rect(center=pos) # Get the rectangle of the rotated image centered at the position, (center=(x, y))
        screen.blit(rotated, rect) # Blit the rotated image to the screen at the rectangle position, (image, position), (rotated, rect)
        # The rotated image will be drawn centered at the position