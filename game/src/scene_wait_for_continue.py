import pygame
WIDTH, HEIGHT = 800, 600  # Screen size
WINDOW_SIZE = (WIDTH, HEIGHT)  # Window size
screen = pygame.display.set_mode(WINDOW_SIZE)  # Screen object

def scene_wait_for_continue():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.Font(None, 50)
    
    black = (0, 0, 0)
    white = (255, 255, 255)
    button_color = (200, 200, 200)  # Light gray
    button_hover = (170, 170, 170)  # Darker gray on hover

    screen.fill(white)

    # Button dimensions
    button_width, button_height = 200, 60
    center_x = (screen.get_width() - button_width) // 2

    # Button positions
    continue_y = 250
    main_menu_y = continue_y + 80
    exit_y = main_menu_y + 80

    # Create button rects
    continue_button = pygame.Rect(center_x, continue_y, button_width, button_height)
    main_menu_button = pygame.Rect(center_x, main_menu_y, button_width, button_height)
    exit_button = pygame.Rect(center_x, exit_y, button_width, button_height)

    # Render button texts
    continue_text = font.render("Continue...", True, black)
    main_menu_text = font.render("Main Menu", True, black)
    exit_text = font.render("Exit", True, black)

    continue_text_rect = continue_text.get_rect(center=continue_button.center)
    main_menu_text_rect = main_menu_text.get_rect(center=main_menu_button.center)
    exit_text_rect = exit_text.get_rect(center=exit_button.center)

    waiting = True
    while waiting:
        mouse_pos = pygame.mouse.get_pos()  # Get mouse position

        # Change button colors on hover
        continue_color = button_hover if continue_button.collidepoint(mouse_pos) else button_color
        main_menu_color = button_hover if main_menu_button.collidepoint(mouse_pos) else button_color
        exit_color = button_hover if exit_button.collidepoint(mouse_pos) else button_color

        # Draw buttons
        screen.fill(white)  # Clear screen
        pygame.draw.rect(screen, continue_color, continue_button, border_radius=10)
        pygame.draw.rect(screen, main_menu_color, main_menu_button, border_radius=10)
        pygame.draw.rect(screen, exit_color, exit_button, border_radius=10)

        # Draw button text
        screen.blit(continue_text, continue_text_rect)
        screen.blit(main_menu_text, main_menu_text_rect)
        screen.blit(exit_text, exit_text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Mouse click event
                if continue_button.collidepoint(event.pos):
                    return "continue"
                if main_menu_button.collidepoint(event.pos):
                    from src.main_menu import main_menu  # Call main menu function
                    main_menu()
                    return "main_menu"
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()

    return None
