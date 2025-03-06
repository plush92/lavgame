import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Picnic Adventure")

# Colors
GREEN = (34, 139, 34)
BLUE = (64, 164, 223)
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
PINK = (255, 192, 203)

# Character class
class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((20, 20))  # Reduced size from 40x40 to 20x20
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3
        self.connected = True

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Flower class for decorative elements
class Flower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def main():
    # Sprite groups
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    flowers = pygame.sprite.Group()

    # Create characters
    character1 = Character(100, SCREEN_HEIGHT // 2, (255, 0, 0))  # Red character
    character2 = Character(130, SCREEN_HEIGHT // 2, (0, 0, 255))  # Blue character
    all_sprites.add(character1, character2)

    # Create water obstacles with more varied and potentially narrower paths
    for _ in range(25):  # Increased number of obstacles
        width = random.randint(5, 40)  # Narrower minimum width
        height = random.randint(30, 150)  # Slightly adjusted height range
        x = random.randint(200, SCREEN_WIDTH - 100)
        y = random.randint(0, SCREEN_HEIGHT - height)
        obstacle = Obstacle(x, y, width, height, BLUE)
        all_sprites.add(obstacle)
        obstacles.add(obstacle)

    # Create decorative flowers
    for _ in range(200):  # Increased number of flowers
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        flower = Flower(x, y)
        all_sprites.add(flower)
        flowers.add(flower)

    # Game variables
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    game_won = False

    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Character movement
        keys = pygame.key.get_pressed()
        
        # Character 1 movement (WASD)
        if keys[pygame.K_w]:
            character1.rect.y -= character1.speed
        if keys[pygame.K_s]:
            character1.rect.y += character1.speed
        if keys[pygame.K_a]:
            character1.rect.x -= character1.speed
        if keys[pygame.K_d]:
            character1.rect.x += character1.speed

        # Character 2 movement (Arrow keys)
        if keys[pygame.K_UP]:
            character2.rect.y -= character2.speed
        if keys[pygame.K_DOWN]:
            character2.rect.y += character2.speed
        if keys[pygame.K_LEFT]:
            character2.rect.x -= character2.speed
        if keys[pygame.K_RIGHT]:
            character2.rect.x += character2.speed

        # Keep characters within screen
        character1.rect.clamp_ip(screen.get_rect())
        character2.rect.clamp_ip(screen.get_rect())

        # Check for collision between characters and obstacles
        if pygame.sprite.spritecollide(character1, obstacles, False) or \
           pygame.sprite.spritecollide(character2, obstacles, False):
            # Reset characters if they hit water
            character1.rect.x = 100
            character1.rect.y = SCREEN_HEIGHT // 2
            character2.rect.x = 130
            character2.rect.y = SCREEN_HEIGHT // 2

        # Check for arrival at picnic spot (top right corner)
        if (character1.rect.right > SCREEN_WIDTH - 50 and 
            character1.rect.top < 100 and 
            character2.rect.right > SCREEN_WIDTH - 50 and 
            character2.rect.top < 100):
            game_won = True
            running = False

        # Drawing
        screen.fill(GREEN)  # Green background for field
        
        # Draw flowers
        for flower in flowers:
            screen.blit(flower.image, flower.rect)

        # Draw obstacles
        for obstacle in obstacles:
            screen.blit(obstacle.image, obstacle.rect)

        # Draw characters
        screen.blit(character1.image, character1.rect)
        screen.blit(character2.image, character2.rect)

        # Draw picnic area indicator
        pygame.draw.rect(screen, BROWN, (SCREEN_WIDTH - 50, 0, 50, 100))

        pygame.display.flip()
        clock.tick(60)

    # Game end screen
    if game_won:
        screen.fill(GREEN)
        win_text = font.render("You made it to the picnic!", True, WHITE)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, 
                               SCREEN_HEIGHT // 2 - win_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()

def start_end():
    main()  # Runs the driving scene
    import src.main_menu  # Import main menu module
    src.main_menu.main_menu()  # Call the main menu again

# Run the game
if __name__ == "__main__":
    start_end()