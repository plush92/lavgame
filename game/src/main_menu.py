import pygame
pygame.init()
import sys
from src.level_select import level_select
from src.scenes.intro import start_intro  # Import IntroScene class
from src.scenes.fight.Game import start_fight  # Import FightScene class
from src.scenes.driving.driving import start_driving  # Import DrivingScene class
from src.scenes.bar.game import start_bar  # Import BarScene class
from src.scenes.date.date import start_date  # Import DateScene class
from src.scenes.vegas.vegas import start_vegas  # Import VegasScene class
from src.scenes.meadow.main import start_end  # Import EndScene class

WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)
pygame.display.set_caption("Game")
screen = pygame.display.set_mode(WINDOW_SIZE)

click = False
clock = pygame.time.Clock()

def main_menu():
    global click
    while True:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render("Main Menu", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2.5 - 50))
        screen.blit(text, text_rect)

        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        button_2 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)
        button_3 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 200, 200, 50)

        pygame.draw.rect(screen, (255, 0, 0), button_1)  # Red button
        pygame.draw.rect(screen, (0, 255, 0), button_2)  # Green button
        pygame.draw.rect(screen, (0, 0, 255), button_3)  # Blue button

        # Text inside buttons
        button_font = pygame.font.Font(None, 30)
        button_1_text = button_font.render("Start", True, (255, 255, 255))
        button_2_text = button_font.render("Exit", True, (255, 255, 255))
        button_3_text = button_font.render("Level Select", True, (255, 255, 255))
        screen.blit(button_1_text, (WIDTH // 2 - 50, HEIGHT // 2 + 15))
        screen.blit(button_2_text, (WIDTH // 2 - 25, HEIGHT // 2 + 115))
        screen.blit(button_3_text, (WIDTH // 2 - 50, HEIGHT // 2 + 215))

        # Button interactions
        if button_1.collidepoint((mx, my)):
            if click:
                game()  # Start the game and play scenes in order
        if button_2.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        if button_3.collidepoint((mx, my)):
            if click:
                level_select()

        click = False  # Reset click after checking buttons

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)

def game():
    """Plays all scenes in order."""
    scenes = [
        start_intro,
        start_fight,
        start_bar,
        start_date,
        start_vegas,
        start_driving,
        start_end
    ]

    for scene in scenes:
        result = scene()  # Call each scene function
        if result == "exit":  # Allow scenes to signal an exit
            pygame.quit()
            sys.exit()

    main_menu()  # Return to the main menu after all scenes