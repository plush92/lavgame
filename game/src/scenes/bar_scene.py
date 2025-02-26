import pygame

# Initialize Pygame
pygame.init()

# Game window setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PvP Fight Scene")

# Clock to control frame rate
clock = pygame.time.Clock()

# Character setup
player1 = pygame.Rect(100, 400, 50, 100)  # Player 1 position and size
player2 = pygame.Rect(650, 400, 50, 100)  # Player 2 position and size

# Health setup
health1 = 100
health2 = 100

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Game loop flag
running = True

def handle_controls(player, keys):
    # Spacebar to strike
    if keys[pygame.K_SPACE]:
        strike(player)
    # Down arrow to dodge
    if keys[pygame.K_DOWN]:
        dodge(player)

def strike(player):
    global strike_lands
    strike_lands = False
    # Basic strike logic: Check if within range of opponent
    if player == player1 and player1.colliderect(player2):
        strike_lands = True
    elif player == player2 and player2.colliderect(player1):
        strike_lands = True

def dodge(player):
    # Dodge mechanic: simply move the player
    if player == player1:
        player.x += 10  # Example movement, you can make it more complex
    elif player == player2:
        player.x -= 10  # Example movement, you can make it more complex

def update_health():
    strike_lands = False
    global health1, health2
    if strike_lands:
        if player1.colliderect(player2):
            health2 -= 10  # Player 2 gets damaged
        elif player2.colliderect(player1):
            health1 -= 10  # Player 1 gets damaged

def draw_health():
    pygame.draw.rect(screen, GREEN, (50, 50, health1, 20))  # Player 1 health bar
    pygame.draw.rect(screen, GREEN, (WIDTH - 150, 50, health2, 20))  # Player 2 health bar

# Main game loop
while running:
    screen.fill(BLACK)  # Clear screen

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()  # Get the state of all keys

    # Handle player controls
    handle_controls(player1, keys)
    handle_controls(player2, keys)

    # Update health after a strike
    update_health()

    # Draw characters (you can replace these with images)
    pygame.draw.rect(screen, RED, player1)
    pygame.draw.rect(screen, BLUE, player2)

    # Draw health bars
    draw_health()

    pygame.display.flip()  # Update the display
    clock.tick(60)  # Limit the frame rate to 60 FPS

pygame.quit()
