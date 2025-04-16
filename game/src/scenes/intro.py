import pygame
import time
from src.scene_wait_for_continue import scene_wait_for_continue

def fade_text(screen, text, font, color, background, duration=1, fade_speed=60): #duration = 2, fade_speed = 6
    lines = text.split('\n')  # Split the text into multiple lines
    line_height = font.get_height()  # Get the height of each line
    
    for alpha in range(0, 256, fade_speed):
        screen.fill(background)
        
        # Render each line and adjust the vertical position
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + i * line_height))
            text_surface.set_alpha(alpha)
            screen.blit(text_surface, text_rect)
        
        pygame.display.update()
        pygame.time.delay(30)
    
    time.sleep(duration)
    
    for alpha in range(255, -1, -fade_speed):
        screen.fill(background)
        
        # Render each line again during fade-out
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + i * line_height))
            text_surface.set_alpha(alpha)
            screen.blit(text_surface, text_rect)
        
        pygame.display.update()
        pygame.time.delay(30)

def fade_out(screen, background, fade_speed=5):
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill(background)
    
    for alpha in range(0, 256, fade_speed):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(30)

def game_intro():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Intro")
    
    font = pygame.font.Font(None, 50)
    background_color = (155, 228, 225)
    black = (0, 0, 0)
    
    fade_text(screen, "Oh...hi Tim", font, black, background_color)
    fade_text(screen, "I was wondering how to celebrate the man\n who has everything on his birthday….. ", font, black, background_color)
    fade_text(screen, "And I thought maybe the best gift would be… ", font, black, background_color)
    fade_text(screen, "us", font, black, background_color)

    fade_out(screen, background_color)

    result = scene_wait_for_continue(screen)
    
    if result == "continue":
        # from game.src.scenes.fight.fight import start_fight  # Import FightScene class  # Import the fight scene module
        # start_fight()  # Start the fight scene
        return "continue"

def start_intro():
    game_intro()
    # import src.main_menu  # Import main menu module
    # src.main_menu.main_menu()  # Call the main menu again

# Run the game
if __name__ == "__main__":
    start_intro()
