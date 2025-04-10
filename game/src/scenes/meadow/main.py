import pygame
import os
from src.scenes.meadow.character import Character
from src.scenes.meadow.companion import Companion
from src.scenes.meadow.flower import Flower
from src.scenes.meadow.constants import WIDTH, HEIGHT, GREEN, WHITE, BROWN
import random

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Meadow Walk")
    clock = pygame.time.Clock()

    # Resolve the directory for assets
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")

    # Load flower images
    flower_images = [
        pygame.image.load(os.path.join(assets_dir, "flower_f1.png")).convert_alpha(),
        pygame.image.load(os.path.join(assets_dir, "flower_f2.png")).convert_alpha(),
        pygame.image.load(os.path.join(assets_dir, "flower_f3.png")).convert_alpha(),
        pygame.image.load(os.path.join(assets_dir, "flower_f4.png")).convert_alpha(),
    ]

    # Scale flower images
    flower_images = [pygame.transform.scale(img, (30, 30)) for img in flower_images]

    tim_image = pygame.image.load(os.path.join(assets_dir, "tim.png")).convert_alpha()
    tim_image = pygame.transform.scale(tim_image, (100, 100))
    lav_image = pygame.image.load(os.path.join(assets_dir, "lav.png")).convert_alpha()
    lav_image = pygame.transform.scale(lav_image, (50, 50))
    # Create characters
    #parameters = {x, y, color, is_player, image_path, name}
    tim = Character(50, HEIGHT // 2, (255, 0, 0), image_path="tim.png")  # Red character
    lav = Companion(50, HEIGHT // 2, (0, 0, 255), image_path="lav.png")  # Blue companion

    # Create flowers
    flowers = pygame.sprite.Group()
    for _ in range(1250):  # Add 500 flowers
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        flower = Flower(x, y, flower_images)
        flowers.add(flower)

    # Tree and picnic setup
    tree = pygame.image.load(os.path.join(assets_dir, "tree.png")).convert_alpha()
    tree = pygame.transform.scale(tree, (100, 150))
    tree_rect = tree.get_rect(center=(WIDTH - 100, HEIGHT // 2))

    picnic_area = pygame.Rect(WIDTH - 150, HEIGHT // 2 + 100, 100, 50)

    # Dialogue setup
    font = pygame.font.Font(None, 36)
    dialogue = [
        "Lav: What a beautiful day for a picnic!",
        "Tim: I'm glad we could spend this time together.",
        "Lav: Me too. Let's enjoy this moment.",
    ]
    dialogue_index = 0
    show_dialogue = False

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Character movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            tim.rect.y -= tim.speed
        if keys[pygame.K_DOWN]:
            tim.rect.y += tim.speed
        if keys[pygame.K_LEFT]:
            tim.rect.x -= tim.speed
        if keys[pygame.K_RIGHT]:
            tim.rect.x += tim.speed

        # Keep Tim within screen bounds
        tim.rect.clamp_ip(screen.get_rect())

        # Companion follows Tim
        lav.follow(tim)

        # Update flowers
        for flower in flowers:
            flower.update(tim)

        # Check if Tim reaches the tree
        if tim.rect.colliderect(tree_rect):
            show_dialogue = True

        # Drawing
        screen.fill(GREEN)  # Meadow background

        # Draw flowers
        for flower in flowers:
            screen.blit(flower.image, flower.rect)

        # Draw tree and picnic area
        screen.blit(tree, tree_rect)
        pygame.draw.rect(screen, BROWN, picnic_area)

        # Draw characters
        screen.blit(tim.image, tim.rect)
        screen.blit(lav.image, lav.rect)

        # Draw dialogue
        if show_dialogue and dialogue_index < len(dialogue):
            dialogue_text = font.render(dialogue[dialogue_index], True, WHITE)
            screen.blit(dialogue_text, (50, HEIGHT - 100))

            # Advance dialogue on key press
            if keys[pygame.K_SPACE]:
                dialogue_index += 1

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()

def start_end():
    main() 
    import src.main_menu  # Import main menu module
    src.main_menu.main_menu()  # Call the main menu again

# Run the game
if __name__ == "__main__":
    start_end()