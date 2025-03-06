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

# Character class
class Character:
    def __init__(self, x, y, color, is_player=False):
        self.x = x
        self.y = y
        self.color = color
        self.width = 50
        self.height = 50
        self.speed = 5
        self.health = 100
        self.is_player = is_player
        self.punching = False
        self.punch_timer = 0

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        
        # Draw punch effect when punching
        if self.punching:
            punch_color = (255, 165, 0)  # Orange
            punch_size = 10
            pygame.draw.rect(surface, punch_color, 
                             (self.x + self.width, self.y, punch_size, self.height))

    def move_towards_mouse(self):
        if self.is_player:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle = math.atan2(mouse_y - self.y, mouse_x - self.x)
            self.x += math.cos(angle) * self.speed
            self.y += math.sin(angle) * self.speed

    def check_collision(self, other):
        # Simple rectangle collision
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + self.height > other.y)

def main():
    # Initialize Pygame
    pygame.init()

    # Screen setup
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dad Fight!")

    # Game setup
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

    # Create characters
    player = Character(100, HEIGHT//2, BLUE, is_player=True)
    dad = Character(WIDTH - 200, HEIGHT//2, RED)

     # Instruction text
    instruction_text1 = small_font.render("Move mouse to move character", True, GRAY)
    instruction_text2 = small_font.render("Click to punch!", True, GRAY)

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Punch on mouse click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                player.punching = True
                player.punch_timer = 10  # Punch duration
                
                # Check if punch hits dad
                if player.check_collision(dad):
                    dad.health -= 20  # More damage when punching
        
        # Clear the screen
        screen.fill(WHITE)
        
        # Move player towards mouse
        player.move_towards_mouse()
        
        # Simple dad AI: move randomly
        dad.x += random.choice([-1, 0, 1]) * dad.speed
        dad.y += random.choice([-1, 0, 1]) * dad.speed
        
        # Keep characters in screen bounds
        player.x = max(0, min(player.x, WIDTH - player.width))
        player.y = max(0, min(player.y, HEIGHT - player.height))
        dad.x = max(0, min(dad.x, WIDTH - dad.width))
        dad.y = max(0, min(dad.y, HEIGHT - dad.height))
        
        # Collision damage
        if player.check_collision(dad):
            player.health -= 1  # Small damage when touching
        
        # Punch timer
        if player.punch_timer > 0:
            player.punch_timer -= 1
        else:
            player.punching = False
        
        # Draw health bars
        pygame.draw.rect(screen, GREEN, (10, 10, player.health * 2, 20))
        pygame.draw.rect(screen, GREEN, (WIDTH - 210, 10, dad.health * 2, 20))
        
        # Draw characters
        player.draw(screen)
        dad.draw(screen)

        # Draw instruction text at the bottom
        screen.blit(instruction_text1, (WIDTH//2 - instruction_text1.get_width()//2, HEIGHT - 50))
        screen.blit(instruction_text2, (WIDTH//2 - instruction_text2.get_width()//2, HEIGHT - 25))
        
        # Game over conditions
        if player.health <= 0 or dad.health <= 0:
            # Display game over text
            game_over_text = font.render("Game Over!", True, BLACK)
            screen.blit(game_over_text, (WIDTH//2 - 100, HEIGHT//2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False
        
        # Update display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(60)

    # Quit the game
    pygame.quit()
    sys.exit()

def start_fight():
    main()  # This runs the fight scene when called

if __name__ == "__main__":
    start_fight()
