import pygame
import os
from src.scenes.meadow.character import Character
from src.scenes.meadow.companion import Companion
from src.scenes.meadow.flower import Flower
from src.scenes.meadow.letter import Button, Letter
from src.scenes.meadow.constants import WIDTH, HEIGHT, GREEN, WHITE, BROWN, BLACK
import random

def load_letter_text(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return ""

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Meadow Walk")
    clock = pygame.time.Clock()

    assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../src/assets"))

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
    tim = Character(390, 680, (255, 0, 0), image_path="tim.png")  # Red character
    lav = Companion(380, 700, (0, 0, 255), image_path="lav.png")  # Blue companion

    # Create flowers
    flowers = pygame.sprite.Group()
    for _ in range(1400):  # Add 1400 flowers
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        flower = Flower(x, y, flower_images)
        flowers.add(flower)

    # create meadow image
    meadow = pygame.image.load(os.path.join(assets_dir, "meadow1.png")).convert_alpha()
    meadow = pygame.transform.scale(meadow, (WIDTH, HEIGHT))
    # render at the bottom
    meadow_rect = meadow.get_rect(topleft=(0, HEIGHT - 225))

    # Tree and picnic setup
    tree = pygame.image.load(os.path.join(assets_dir, "tree.png")).convert_alpha()
    tree = pygame.transform.scale(tree, (150, 175))
    tree_rect = tree.get_rect(center=(150, 75))

    # load picnic image
    picnic_image = pygame.image.load(os.path.join(assets_dir, "picnic.png")).convert_alpha()
    picnic_image = pygame.transform.scale(picnic_image, (80, 60))
    picnic_rect = picnic_image.get_rect(center=(40, 110))

    # Dialogue setup
    font = pygame.font.Font(None, 36)
    dialogue = [
        "Lav: What a beautiful day",
        "Tim: I'm glad we could spend this time together.",
        "Lav: Me too.",  # Fixed missing comma
        "Lav: I have so much to say",
    ]
    dialogue_index = 0
    show_dialogue = False
    key_pressed = False

    # Initialize the read letter button
    read_letter_button = Button(WIDTH // 2 - 75, HEIGHT - 100, 150, 50, "Read Letter", font, (200, 200, 200), (255, 255, 255))
    
    # Initialize the letter
    # Try to load letter text from file, otherwise use default text
    letter_file_path = os.path.join(assets_dir, "lettertext.txt")
    try:
        letter_text = load_letter_text(letter_file_path)
        letter = Letter(letter_text)
    except:
        # Use default letter text from Letter class
        letter = Letter()

    reading_letter = False

    # Game loop
    running = True
    while running:
        # Handle events
        current_event = None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if reading_letter:
                letter.handle_navigation(event)
            
            # Handle button click
            if dialogue_index >= len(dialogue) and not reading_letter:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if read_letter_button.is_clicked(event):
                        reading_letter = True

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
        # Draw picnic area
        screen.blit(picnic_image, picnic_rect)

        # Draw meadow background
        screen.blit(meadow, meadow_rect)

        # Draw characters
        screen.blit(tim.image, tim.rect)
        screen.blit(lav.image, lav.rect)

        # Process dialogue
        if show_dialogue:
            if dialogue_index < len(dialogue):
                # Draw a transparent purple border around the dialogue text
                dialogue_box_surface = pygame.Surface((WIDTH - 80, 80), pygame.SRCALPHA)  # Create a surface with alpha
                dialogue_box_surface.fill((128, 0, 128, 100))  # Semi-transparent purple
                screen.blit(dialogue_box_surface, (40, HEIGHT - 120))  # Blit the surface onto the screen

                # Draw a subtle light purple border
                pygame.draw.rect(screen, (200, 200, 255), pygame.Rect(40, HEIGHT - 120, WIDTH - 80, 80), 2)

                # Display current dialogue line
                dialogue_text = font.render(dialogue[dialogue_index], True, WHITE)
                screen.blit(dialogue_text, (50, HEIGHT - 100))

                # Advance dialogue on spacebar press
                if keys[pygame.K_SPACE] and not key_pressed:
                    dialogue_index += 1
                    key_pressed = True
                elif not keys[pygame.K_SPACE]:
                    key_pressed = False
            else:
                # If dialogue is finished, show the "Read Letter" button
                read_letter_button.draw(screen)

        # Add "Walk to the picnic" instructions
        if not show_dialogue and not reading_letter:
            instructions_text = font.render("Walk to the picnic", True, BLACK)
            instructions_rect = instructions_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(instructions_text, instructions_rect)

        # Draw the letter if we're reading it
        if reading_letter:
            letter.draw(screen)
            letter.handle_navigation

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def start_end():
    main() 
    import src.main_menu  # Import main menu module
    src.main_menu.main_menu()  # Call the main menu again

# Run the game
if __name__ == "__main__":
    main()