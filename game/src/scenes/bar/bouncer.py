import pygame
import random
import sys
import time
from src.scenes.bar.walls import create_labyrinth_walls

# Screen Setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bar Escape: Hometown Honkey Tonk")
# Create the walls
WALLS = create_labyrinth_walls()

class Bouncer:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed = 1.5  # Increased base speed for better pursuit
        self.can_move = False
        self.move_start_time = None
        self.path_finding_timer = 0
        self.stuck_timer = 0
        self.last_position = (x, y)
        self.path_direction = None
        self.alternative_routes = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.current_route_index = 0
        self.route_attempt_time = 0

    def start_moving(self):
        self.can_move = True
        self.move_start_time = time.time()

    def move_towards_player(self, player, walls):
        if not self.can_move:
            return

        # Check if bouncer is stuck
        current_pos = (self.rect.x, self.rect.y)
        if abs(current_pos[0] - self.last_position[0]) < 2 and abs(current_pos[1] - self.last_position[1]) < 2:
            self.stuck_timer += 1
        else:
            self.stuck_timer = 0
            
        # Update pathfinding direction periodically or when stuck
        self.path_finding_timer += 1
        if self.path_finding_timer >= 60 or self.stuck_timer >= 30:  # Update direction every second or when stuck
            self.path_finding_timer = 0
            
            # Calculate direct direction to player
            direct_x = 1 if player.rect.x > self.rect.x else -1 if player.rect.x < self.rect.x else 0
            direct_y = 1 if player.rect.y > self.rect.y else -1 if player.rect.y < self.rect.y else 0
            
            # If stuck, try alternative routes
            if self.stuck_timer >= 10:
                self.stuck_timer = 0
                # Try a different direction from our alternatives list
                self.current_route_index = (self.current_route_index + 1) % len(self.alternative_routes)
                self.path_direction = self.alternative_routes[self.current_route_index]
                self.route_attempt_time = time.time()
            else:
                # Prioritize the larger distance axis
                x_dist = abs(player.rect.x - self.rect.x)
                y_dist = abs(player.rect.y - self.rect.y)
                
                if x_dist > y_dist:
                    self.path_direction = (direct_x, 0)
                else:
                    self.path_direction = (0, direct_y)
        
        # If we've been trying an alternative route for too long, go back to direct pursuit
        if self.path_direction in self.alternative_routes and time.time() - self.route_attempt_time > 1.5:
            # Calculate direct direction to player
            direct_x = 1 if player.rect.x > self.rect.x else -1 if player.rect.x < self.rect.x else 0
            direct_y = 1 if player.rect.y > self.rect.y else -1 if player.rect.y < self.rect.y else 0
            
            x_dist = abs(player.rect.x - self.rect.x)
            y_dist = abs(player.rect.y - self.rect.y)
            
            if x_dist > y_dist:
                self.path_direction = (direct_x, 0)
            else:
                self.path_direction = (0, direct_y)

        # Apply movement based on current path direction
        dx, dy = 0, 0
        if self.path_direction:
            dx = self.path_direction[0] * self.speed
            dy = self.path_direction[1] * self.speed
        
        # Try to move horizontally
        if dx != 0:
            proposed_rect = self.rect.copy()
            proposed_rect.x += dx
            
            collision = False
            for wall in walls:
                if proposed_rect.colliderect(wall):
                    collision = True
                    break
                    
            if not collision:
                self.rect.x += dx
            else:
                # If horizontal movement is blocked, try vertical
                self.path_direction = (0, 1 if player.rect.y > self.rect.y else -1)
                        
        # Try to move vertically
        if dy != 0:
            proposed_rect = self.rect.copy()
            proposed_rect.y += dy
            
            collision = False
            for wall in walls:
                if proposed_rect.colliderect(wall):
                    collision = True
                    break
                    
            if not collision:
                self.rect.y += dy
            else:
                # If vertical movement is blocked, try horizontal
                self.path_direction = (1 if player.rect.x > self.rect.x else -1, 0)
                
        # Keep bouncer in screen bounds and handle boundary collisions
        if self.rect.left < 20:
            self.rect.left = 20
            self.path_direction = (1, 0)  # Move right
        elif self.rect.right > SCREEN_WIDTH - 20:
            self.rect.right = SCREEN_WIDTH - 20
            self.path_direction = (-1, 0)  # Move left
            
        if self.rect.top < 20:
            self.rect.top = 20
            self.path_direction = (0, 1)  # Move down
        elif self.rect.bottom > SCREEN_HEIGHT - 20:
            self.rect.bottom = SCREEN_HEIGHT - 20
            self.path_direction = (0, -1)  # Move up
        
        # Store current position for stuck detection
        self.last_position = (self.rect.x, self.rect.y)