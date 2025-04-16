import pygame
WIDTH, HEIGHT = 800, 600  # Screen size
WINDOW_SIZE = (WIDTH, HEIGHT)  # Window size
screen = pygame.display.set_mode(WINDOW_SIZE)  # Screen object

# def scene_wait_for_continue(screen):
#     pygame.init()
#     screen = pygame.display.set_mode((800, 600))
#     font = pygame.font.Font(None, 50)
    
#     black = (0, 0, 0)
#     white = (255, 255, 255)
#     button_color = (200, 200, 200)  # Light gray
#     button_hover = (170, 170, 170)  # Darker gray on hover

#     screen.fill(white)

#     # Button dimensions
#     button_width, button_height = 200, 60
#     center_x = (screen.get_width() - button_width) // 2

#     # Button positions
#     continue_y = 250
#     main_menu_y = continue_y + 80
#     exit_y = main_menu_y + 80

#     # Create button rects
#     continue_button = pygame.Rect(center_x, continue_y, button_width, button_height)
#     main_menu_button = pygame.Rect(center_x, main_menu_y, button_width, button_height)
#     exit_button = pygame.Rect(center_x, exit_y, button_width, button_height)

#     # Render button texts
#     continue_text = font.render("Continue...", True, black)
#     exit_text = font.render("Exit", True, black)

#     continue_text_rect = continue_text.get_rect(center=continue_button.center)
#     exit_text_rect = exit_text.get_rect(center=exit_button.center)

#     waiting = True
#     while waiting:
#         mouse_pos = pygame.mouse.get_pos()  # Get mouse position

#         # Change button colors on hover
#         continue_color = button_hover if continue_button.collidepoint(mouse_pos) else button_color
#         exit_color = button_hover if exit_button.collidepoint(mouse_pos) else button_color

#         # Draw buttons
#         screen.fill(white)  # Clear screen
#         pygame.draw.rect(screen, continue_color, continue_button, border_radius=10)
#         pygame.draw.rect(screen, exit_color, exit_button, border_radius=10)

#         # Draw button text
#         screen.blit(continue_text, continue_text_rect)
#         screen.blit(exit_text, exit_text_rect)

#         pygame.display.update()

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:  # Mouse click event
#                 if continue_button.collidepoint(event.pos):
#                     return
#                 if exit_button.collidepoint(event.pos):
#                     pygame.quit()
#                     exit()

#     return None

def scene_wait_for_continue(screen):
    """Display a 'Press SPACE to continue...' prompt and wait for the player to press SPACE."""
    font = pygame.font.Font(None, 36)
    prompt_text = font.render("Press SPACE to continue...", True, (255, 255, 255))
    prompt_rect = prompt_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    
    while True:
        screen.fill((0, 0, 0))  # Black background
        screen.blit(prompt_text, prompt_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return "continue"  # Exit the function when SPACE is pressed