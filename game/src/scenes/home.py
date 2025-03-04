import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Welcome Home")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)

# Player settings
player_x = 400
player_y = 500
PLAYER_SPEED = 5

# Background
background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill(WHITE)

# House exterior
pygame.draw.rect(background, BROWN, (200, 100, 400, 400))
pygame.draw.polygon(background, BLACK, [(200, 100), (400, 20), (600, 100)])

# Door
door_rect = pygame.Rect(350, 350, 100, 150)
pygame.draw.rect(background, (165, 42, 42), door_rect)

# Fonts
font_small = pygame.font.Font(None, 36)
font_large = pygame.font.Font(None, 48)

# Game states
OUTSIDE = 0
AT_DOOR = 1
INSIDE = 2
AT_TABLE = 3
game_state = OUTSIDE

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Wife position
wife_x = 400
wife_y = 200

# Table position
table_rect = pygame.Rect(250, 250, 300, 200)

# Main game loop
def main():
    global player_x, player_y, game_state
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check door interaction
                if game_state == OUTSIDE and door_rect.collidepoint(mouse_pos):
                    game_state = AT_DOOR

        # Player movement
        keys = pygame.key.get_pressed()
        if game_state in [OUTSIDE, AT_DOOR, INSIDE]:
            if keys[pygame.K_LEFT]:
                player_x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT]:
                player_x += PLAYER_SPEED
            if keys[pygame.K_UP]:
                player_y -= PLAYER_SPEED
            if keys[pygame.K_DOWN]:
                player_y += PLAYER_SPEED
        
        # Boundary checks for different game states
        if game_state == OUTSIDE or game_state == AT_DOOR:
            player_x = max(0, min(player_x, SCREEN_WIDTH - 50))
            player_y = max(0, min(player_y, SCREEN_HEIGHT - 50))
        elif game_state == INSIDE:
            # Restrict movement inside the house
            player_x = max(50, min(player_x, SCREEN_WIDTH - 100))
            player_y = max(50, min(player_y, SCREEN_HEIGHT - 100))

            # Check if player reaches table
            if table_rect.collidepoint(player_x + 25, player_y + 25):
                game_state = AT_TABLE
        
        # Clear screen based on game state
        if game_state in [OUTSIDE, AT_DOOR]:
            screen.blit(background, (0, 0))
        else:
            screen.fill(WHITE)
        
        # Draw player
        pygame.draw.rect(screen, (0, 255, 0), (player_x, player_y, 50, 50))
        
        # Game state rendering
        if game_state == OUTSIDE:
            pass
        
        elif game_state == AT_DOOR:
            note_text = font_small.render("Welcome home <3", True, BLACK)
            screen.blit(note_text, (250, 200))
            
            if door_rect.collidepoint(player_x + 25, player_y + 25):
                game_state = INSIDE
        
        elif game_state == INSIDE:
            # Dining setup
            pygame.draw.rect(screen, BROWN, table_rect)  # Table
            pygame.draw.circle(screen, YELLOW, (400, 200), 20)  # Candle
            
            # Wife
            pygame.draw.rect(screen, (255, 192, 203), (wife_x, wife_y, 50, 50))  # Wife character
            
            # Wife's dialogue
            love_text = font_large.render("I love you honey!", True, BLACK)
            screen.blit(love_text, (250, 100))
        
        elif game_state == AT_TABLE:
            # Dining setup
            pygame.draw.rect(screen, BROWN, table_rect)  # Table
            pygame.draw.circle(screen, YELLOW, (400, 200), 20)  # Candle
            
            # Eating animation
            pygame.draw.rect(screen, (0, 255, 0), (player_x, player_y, 50, 50))
            eat_text = font_large.render("Enjoying dinner...", True, BLACK)
            screen.blit(eat_text, (250, 100))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

# Run the game
if __name__ == "__main__":
    main()

def start_home():
    main()  # Runs the driving scene
    import src.main_menu  # Import main menu module
    src.main_menu.main_menu()  # Call the main menu again

# Run the game
if __name__ == "__main__":
    start_home()