import pygame  # Import the Pygame library for graphics and game development
import random  # Import random for potential randomness in behavior (not used yet)
import heapq   # Import heapq for implementing the priority queue in A* algorithm

# Screen Setup
SCREEN_WIDTH = 800  # Define screen width
SCREEN_HEIGHT = 600  # Define screen height
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create the game window
pygame.display.set_caption("Bar Escape: Hometown Honkey Tonk")  # Set the window title

class Bouncer:
    def __init__(self, x, y):
        """Initialize the bouncer character."""
        self.rect = pygame.Rect(x, y, 20, 20) # initialize bouncer location
        self.speed = 1.5 # speed
        self.can_move = False
        self.stuck_timer = 0
        self.last_position = (x, y)

    def start_moving(self):
        """Allow the bouncer to start moving."""
        self.can_move = True

    def move_towards_player(self, player, walls):
        """Move directly toward the player while avoiding walls."""
        if not self.can_move:
            return

        # Calculate direction vector
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y

        # Normalize direction vector
        distance = max(1, (dx**2 + dy**2) ** 0.5)
        dx = (dx / distance) * self.speed
        dy = (dy / distance) * self.speed

        # Try moving in the intended direction
        self.rect.x += dx
        self.rect.y += dy

        # Check for collision with walls
        for wall in walls:
            if self.rect.colliderect(wall):
                # If colliding, revert movement
                self.rect.x -= dx
                self.rect.y -= dy

                # Randomly choose an alternative direction
                angle = random.uniform(0, 360)  # Pick a random direction
                dx = self.speed * pygame.math.Vector2(1, 0).rotate(angle).x
                dy = self.speed * pygame.math.Vector2(1, 0).rotate(angle).y
                self.rect.x += dx
                self.rect.y += dy
                break  # Stop checking after one collision adjustment

        # Ensure bouncer stays in bounds
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
