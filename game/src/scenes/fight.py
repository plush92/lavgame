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

# Character class
class Character:
    def __init__(self, x, y, color, is_player=False, image_path=None):
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
        if image_path:
            self.load_image(image_path)

    def load_image(self, path):
        try:
            self.image = pygame.image.load(path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            # Create flipped version for left direction
            self.image_flipped = pygame.transform.flip(self.image, True, False)
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            self.image = None

    def draw(self, surface):
        if self.image and not self.is_player:
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

# Dialog class
class DialogSystem:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.dialog_index = 0
        self.active = True
        self.dialogs = [
            {"speaker": "Son", "text": "Dad, I need to borrow the car tonight."},
            {"speaker": "Dad", "text": "No way! Your grades are terrible!"},
            {"speaker": "Son", "text": "That's so unfair! Everyone else gets to go!"},
            {"speaker": "Dad", "text": "Life isn't fair. Maybe you should study more."},
            {"speaker": "Son", "text": "You never listen to me!"},
            {"speaker": "Dad", "text": "That's it! I've had enough of your attitude!"},
        ]

    def draw(self, surface):
        if not self.active or self.dialog_index >= len(self.dialogs):
            return False
            
        # Dialog box
        box_height = 150
        pygame.draw.rect(surface, WHITE, (50, self.height - box_height - 50, self.width - 100, box_height))
        pygame.draw.rect(surface, BLACK, (50, self.height - box_height - 50, self.width - 100, box_height), 2)
        
        dialog = self.dialogs[self.dialog_index]
        
        # Speaker label
        speaker_text = self.font.render(dialog["speaker"] + ":", True, 
                                      BLUE if dialog["speaker"] == "Son" else RED)
        surface.blit(speaker_text, (70, self.height - box_height - 40))
        
        # Dialog text - with word wrap
        words = dialog["text"].split(' ')
        line = ""
        y_offset = 0
        for word in words:
            test_line = line + word + " "
            text_width = self.font.size(test_line)[0]
            if text_width < self.width - 150:
                line = test_line
            else:
                text = self.font.render(line, True, BLACK)
                surface.blit(text, (70, self.height - box_height - 5 + y_offset))
                y_offset += 30
                line = word + " "
        
        text = self.font.render(line, True, BLACK)
        surface.blit(text, (70, self.height - box_height - 5 + y_offset))
        
        # Continue prompt
        continue_text = self.small_font.render("Press SPACE to continue...", True, GRAY)
        surface.blit(continue_text, (self.width - 230, self.height - 80))
        
        return True

    def next_dialog(self):
        self.dialog_index += 1
        if self.dialog_index >= len(self.dialogs):
            self.active = False
            return False
        return True

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
    
    # Game states
    DIALOG = 0
    FIGHTING = 1
    GAME_OVER = 2
    game_state = DIALOG

    # Create dialog system
    dialog_system = DialogSystem(WIDTH, HEIGHT)

    # Create characters (positioned for dialog initially)
    player = Character(200, HEIGHT//2, BLUE, is_player=True)
    dad = Character(WIDTH - 250, HEIGHT//2, RED, is_player=False, image_path="assets/dennehy.png")
    
    # Movement boundaries
    PLAY_AREA_TOP = HEIGHT // 4
    PLAY_AREA_BOTTOM = HEIGHT * 3 // 4
    PLAY_AREA_LEFT = WIDTH // 4
    PLAY_AREA_RIGHT = WIDTH * 3 // 4

    # Instruction text
    instruction_text1 = small_font.render("Use ARROW KEYS to move", True, GRAY)
    instruction_text2 = small_font.render("Press SPACE to punch!", True, GRAY)

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_state == DIALOG:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if not dialog_system.next_dialog():
                        game_state = FIGHTING
                        # Reset positions for fight
                        player.x = WIDTH // 3
                        player.y = HEIGHT // 2
                        dad.x = 2 * WIDTH // 3
                        dad.y = HEIGHT // 2
            
            elif game_state == FIGHTING:
                # Punch on space bar
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    player.punching = True
                    player.punch_timer = 10  # Punch duration
                    
                    # Check if punch hits dad and is in range
                    if player.can_punch(dad):
                        dad.health -= 10
                        # Knockback effect
                        if player.direction == 1:  # Facing right
                            dad.x += 20
                        else:  # Facing left
                            dad.x -= 20
        
        # Clear the screen
        if game_state == DIALOG:
            screen.fill(LIGHT_BLUE)  # Living room background
        else:
            screen.fill(WHITE)
        
        # Handle different game states
        if game_state == DIALOG:
            # Draw characters for dialog
            player.draw(screen)
            dad.draw(screen)
            
            # Draw and process dialog
            dialog_system.draw(screen)
            
        elif game_state == FIGHTING:
            # Player movement with arrow keys
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_LEFT]:
                dx = -1
            if keys[pygame.K_RIGHT]:
                dx = 1
            if keys[pygame.K_UP]:
                dy = -1
            if keys[pygame.K_DOWN]:
                dy = 1
            
            player.move(dx, dy)
            
            # Dad AI: jitter and move in the middle section of screen
            dad_target_x = WIDTH // 2 + random.randint(-100, 100)
            dad_target_y = HEIGHT // 2 + random.randint(-80, 80)
            
            # Move dad towards target
            dad_dx = 0
            dad_dy = 0
            if dad.x < dad_target_x:
                dad_dx = 0.5
            elif dad.x > dad_target_x:
                dad_dx = -0.5
            if dad.y < dad_target_y:
                dad_dy = 0.5
            elif dad.y > dad_target_y:
                dad_dy = -0.5
                
            dad.move(dad_dx, dad_dy)
            
            # Dad occasionally tries to punch player
            if random.random() < 0.01 and dad.can_punch(player):
                dad.punching = True
                dad.punch_timer = 10
                player.health -= 5
            
            # Keep characters in play area
            player.x = max(PLAY_AREA_LEFT, min(player.x, PLAY_AREA_RIGHT - player.width))
            player.y = max(PLAY_AREA_TOP, min(player.y, PLAY_AREA_BOTTOM - player.height))
            dad.x = max(PLAY_AREA_LEFT, min(dad.x, PLAY_AREA_RIGHT - dad.width))
            dad.y = max(PLAY_AREA_TOP, min(dad.y, PLAY_AREA_BOTTOM - dad.height))
            
            # Punch timer
            if player.punch_timer > 0:
                player.punch_timer -= 1
            else:
                player.punching = False
                
            if dad.punch_timer > 0:
                dad.punch_timer -= 1
            else:
                dad.punching = False
            
            # Draw play area boundary
            pygame.draw.rect(screen, GRAY, 
                            (PLAY_AREA_LEFT, PLAY_AREA_TOP, 
                             PLAY_AREA_RIGHT - PLAY_AREA_LEFT, 
                             PLAY_AREA_BOTTOM - PLAY_AREA_TOP), 2)
            
            # Draw health bars
            pygame.draw.rect(screen, BLACK, (10, 10, 204, 24), 2)
            pygame.draw.rect(screen, GREEN, (12, 12, player.health * 2, 20))
            
            pygame.draw.rect(screen, BLACK, (WIDTH - 214, 10, 204, 24), 2)
            pygame.draw.rect(screen, GREEN, (WIDTH - 212, 12, dad.health * 2, 20))
            
            player_label = small_font.render("Son", True, BLUE)
            dad_label = small_font.render("Dad", True, RED)
            screen.blit(player_label, (10, 40))
            screen.blit(dad_label, (WIDTH - 214, 40))
            
            # Draw characters
            player.draw(screen)
            dad.draw(screen)

            # Draw instruction text at the bottom
            screen.blit(instruction_text1, (WIDTH//2 - instruction_text1.get_width()//2, HEIGHT - 50))
            screen.blit(instruction_text2, (WIDTH//2 - instruction_text2.get_width()//2, HEIGHT - 25))
            
            # Game over conditions
            if player.health <= 0 or dad.health <= 0:
                game_state = GAME_OVER
                
        elif game_state == GAME_OVER:
            # Display game over text
            if player.health <= 0:
                outcome_text = font.render("Dad wins! You're grounded!", True, RED)
            else:
                outcome_text = font.render("You win! Dad respects you now!", True, BLUE)
                
            game_over_text = font.render("Game Over!", True, BLACK)
            restart_text = small_font.render("Press R to restart or Q to quit", True, GRAY)
            
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
            screen.blit(outcome_text, (WIDTH//2 - outcome_text.get_width()//2, HEIGHT//2))
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
            
            # Restart or quit
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                # Reset game
                player.health = 100
                dad.health = 100
                dialog_system.dialog_index = 0
                dialog_system.active = True
                game_state = DIALOG
                player.x = 200
                player.y = HEIGHT//2
                dad.x = WIDTH - 250
                dad.y = HEIGHT//2
            elif keys[pygame.K_q]:
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