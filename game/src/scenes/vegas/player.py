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

class Player:
    def __init__(self):
        self.pos = Vector2(WIDTH // 2, HEIGHT - 100)
        self.hammer_img = self._create_hammer_image()
        self.stamina = 100
        self.max_stamina = 100
        self.hammer_angle = 0
        self.swinging = False
        self.swing_timer = 0
        self.cooldown = False
        self.cooldown_timer = 0
        
    def _create_hammer_image(self):
        # Create a simple hammer shape
        surf = pygame.Surface((60, 20), pygame.SRCALPHA)
        pygame.draw.rect(surf, GRAY, (0, 5, 40, 10))  # Handle
        pygame.draw.rect(surf, (50, 50, 50), (40, 0, 20, 20))  # Head
        return surf
        
    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        # Point hammer toward mouse
        direction = Vector2(mouse_pos) - self.pos
        self.hammer_angle = direction.angle_to(Vector2(1, 0))
        
        # Handle swinging animation
        if self.swinging:
            self.swing_timer += dt
            if self.swing_timer >= 300:  # 300ms swing animation
                self.swinging = False
                self.swing_timer = 0
                self.cooldown = True
                self.cooldown_timer = 0
                
        # Handle cooldown
        if self.cooldown:
            self.cooldown_timer += dt
            self.stamina += dt * 0.05  # Recover stamina during cooldown
            if self.cooldown_timer >= 1000:  # 1 second cooldown
                self.cooldown = False
                
        # Cap stamina
        self.stamina = min(self.max_stamina, self.stamina)
        
    def move(self, direction):
        speed = 5
        self.pos += direction * speed
        # Keep player within bounds
        self.pos.x = max(50, min(WIDTH - 50, self.pos.x))
        self.pos.y = max(HEIGHT // 2, min(HEIGHT - 50, self.pos.y))
        
    def swing(self):
        if not self.cooldown and not self.swinging and self.stamina >= 20:
            self.swinging = True
            self.stamina -= 20
            return True
        return False
        
    def draw(self):
        # Draw player
        pygame.draw.circle(screen, GREEN, (int(self.pos.x), int(self.pos.y)), 20)
        
        # Draw hammer
        rotated_hammer = pygame.transform.rotate(self.hammer_img, self.hammer_angle)
        hammer_pos = self.pos + Vector2(30, 0).rotate(-self.hammer_angle)
        hammer_rect = rotated_hammer.get_rect(center=hammer_pos)
        screen.blit(rotated_hammer, hammer_rect)
        
        # Draw stamina bar
        bar_width = 100
        bar_height = 10
        stamina_rect = pygame.Rect(self.pos.x - bar_width // 2, self.pos.y + 30, bar_width, bar_height)
        pygame.draw.rect(screen, RED, stamina_rect)
        fill_width = int(bar_width * (self.stamina / self.max_stamina))
        fill_rect = pygame.Rect(self.pos.x - bar_width // 2, self.pos.y + 30, fill_width, bar_height)
        pygame.draw.rect(screen, GREEN, fill_rect)
        pygame.draw.rect(screen, BLACK, stamina_rect, 1)
