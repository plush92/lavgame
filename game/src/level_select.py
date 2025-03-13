import pygame  # Import pygame module
import sys  # Import sys module
from src.scenes.intro import start_intro  # Import IntroScene class
from src.scenes.fight import start_fight  # Import FightScene class
from src.scenes.driving import start_driving  # Import DrivingScene class
from src.scenes.bar.game import start_bar  # Import BarScene class
from src.scenes.date import start_date  # Import DateScene class
from src.scenes.home import start_home  # Import HomeScene class
from src.scenes.end import start_end  # Import EndScene class

WIDTH, HEIGHT = 800, 600  # Screen size
WINDOW_SIZE = (WIDTH, HEIGHT)  # Window size
pygame.display.set_caption("Game")  # Game window title
screen = pygame.display.set_mode(WINDOW_SIZE)  # Screen object

click = False  # Click variable
clock = pygame.time.Clock()  # Clock object

def main_menu():
    """Handles returning to the main menu."""
    print("Back at the main menu!")
    level_select()  # Restart the level select menu

def level_select():  # Level select function
    global click  # Global click variable
    while True:  # Infinite loop
        screen.fill((0, 0, 0))  # Fill screen with black color
        font = pygame.font.Font(None, 36)  # Font object
        text = font.render("Level Select", True, (255, 255, 255))  # Render text
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2.5 - 50))  # Text rectangle
        screen.blit(text, text_rect)  # Draw text on screen

        mx, my = pygame.mouse.get_pos()  # Mouse position

        button_width = 180  # Button width
        button_height = 30  # Button height
        button_spacing = 35  # Button spacing

        button_1 = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height)  # Intro
        button_2 = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + button_spacing, button_width, button_height)  # Fight
        button_3 = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 2 * button_spacing, button_width, button_height)  # Bar
        button_4 = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 3 * button_spacing, button_width, button_height)  # Date
        button_5 = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 4 * button_spacing, button_width, button_height)  # Driving
        button_6 = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 5 * button_spacing, button_width, button_height)  # Home
        button_7 = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 6 * button_spacing, button_width, button_height)  # End

        buttons = [button_1, button_2, button_3, button_4, button_5, button_6, button_7]  # Button list
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 255, 255)]  # Button colors
        labels = ["Intro", "Fight", "Bar", "Date", "Driving", "Home", "End"]  # Button labels

        button_font = pygame.font.Font(None, 30)  # Button font
        for i, button in enumerate(buttons):  # Iterate through buttons
            pygame.draw.rect(screen, colors[i], button)  # Draw button
            button_text = button_font.render(labels[i], True, (0, 0, 0))  # Black text for contrast on buttons
            screen.blit(button_text, (button.x + 10, button.y + 10))  # Draw text on button

        # Event Handling
        for event in pygame.event.get():  # Event loop
            if event.type == pygame.QUIT:  # If window close button is clicked
                pygame.quit()  # Quit pygame
                sys.exit()  # Exit the program

            if event.type == pygame.KEYDOWN:  # If key is pressed
                if event.key == pygame.K_ESCAPE:  # If ESC is pressed
                    print("Returning to main menu...")
                    return  # Exit the function (goes back to main menu)

            if event.type == pygame.MOUSEBUTTONDOWN:  # If mouse button is clicked
                if event.button == 1:  # If left mouse button is clicked
                    click = True  # Set click to True

        # Button Click Handling
        if click:  # Only check click once per loop
            for i, button in enumerate(buttons):
                if button.collidepoint((mx, my)):
                    print(f"{labels[i]} clicked")  # Print button name when clicked
                    if labels[i] == "Intro":
                        start_intro()
                    elif labels[i] == "Fight":
                        start_fight()
                    elif labels[i] == "Driving":
                        start_driving()
                    elif labels[i] == "Bar":
                        start_bar()
                    elif labels[i] == "Date":
                        start_date()
                    elif labels[i] == "Home":
                        start_home()
                    elif labels[i] == "End":
                        start_end()
            click = False  # Reset click after processing

        pygame.display.update()  # Update display
        clock.tick(60)  # Tick clock
