import pygame # Import pygame module
import sys # Import sys module

WIDTH, HEIGHT = 800, 600 # Screen size
WINDOW_SIZE = (WIDTH, HEIGHT) # Window size
pygame.display.set_caption("Game") # Game window title
screen = pygame.display.set_mode(WINDOW_SIZE) # Screen object

click = False # Click variable
clock = pygame.time.Clock() # Clock object

def level_select(): # Level select function
    global click # Global click variable
    while True: # Infinite loop
        screen.fill((0, 0, 0)) # Fill screen with black color
        font = pygame.font.Font(None, 36) # Font object
        text = font.render("Level Select", True, (255, 255, 255)) # Render text
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2.5 - 50)) # Text rectangle
        screen.blit(text, text_rect) # Draw text on screen

        mx, my = pygame.mouse.get_pos() # Mouse position

        button_width = 180 # Button width
        button_height = 30 # Button height
        button_spacing = 35 # Button spacing

        button_1 = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height) # Intro
        button_2 = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + button_spacing, button_width, button_height) # Fight
        button_3 = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 2 * button_spacing, button_width, button_height) # Bar
        button_4 = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 3 * button_spacing, button_width, button_height) # Date
        button_5 = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 4 * button_spacing, button_width, button_height) # Driving
        button_6 = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 5 * button_spacing, button_width, button_height) # Home
        button_7 = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 6 * button_spacing, button_width, button_height) # End

        buttons = [button_1, button_2, button_3, button_4, button_5, button_6, button_7] # Button list
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 255, 255)] # Button colors
        labels = ["Intro", "Fight", "Bar", "Date", "Driving", "Home", "End"] # Button labels

        button_font = pygame.font.Font(None, 30) # Button font
        for i, button in enumerate(buttons): # Iterate through buttons
            pygame.draw.rect(screen, colors[i], button) # Draw button
            button_text = button_font.render(labels[i], True, (0, 0, 0))  # Black text for contrast on buttons
            screen.blit(button_text, (button.x + 10, button.y + 10)) # Draw text on button

            if button.collidepoint((mx, my)) and click: # Check if button is clicked
                print(f"Button {i + 1} clicked") # Print button number
                # Add your logic for each button

        for event in pygame.event.get(): # Event loop
            if event.type == pygame.QUIT: # If window close button is clicked
                pygame.quit() # Quit pygame
                sys.exit() # Exit the program
            if event.type == pygame.KEYDOWN: # If key is pressed
                if event.key == pygame.K_SPACE: # If SPACE key is pressed
                    pass # Do nothing
            if event.type == pygame.MOUSEBUTTONDOWN: # If mouse button is clicked
                if event.button == 1: # If left mouse button is clicked
                    click = True # Set click to True

        pygame.display.update() # Update display
        clock.tick(60) # Tick clock
        click = False  # Reset click after checking buttons
