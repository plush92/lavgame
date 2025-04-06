# IMPORTS
# -------------------------------------------
import pygame
import random
import math
import sys
from src.scenes.fight.character import Character
from src.scenes.fight.dialogue import DialogSystem
from src.scenes.fight.fridgeitem import FridgeItem
from src.scenes.fight.kitchenprop import KitchenProp
from src.scenes.fight.kitchen import Kitchen

# CONSTANTS & GLOBAL VARIABLES
# -------------------------------------------

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
LIGHT_BLUE = (135, 206, 235)
BROWN = (139, 69, 19)
LIGHT_GRAY = (220, 220, 220)
YELLOW = (255, 255, 0)

# Game states
KITCHEN = 0
FRIDGE_MINIGAME = 1
DIALOG = 2
FIGHTING = 3
GAME_OVER = 4

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Movement boundaries
PLAY_AREA_TOP = 50
PLAY_AREA_BOTTOM = HEIGHT - 50
PLAY_AREA_LEFT = 50
PLAY_AREA_RIGHT = WIDTH - 50

# SCREEN SETUP FUNCTIONS
# -------------------------------------------

def initialize_game():
    """Initialize pygame and set up the game window"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fight Scene")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    
    return screen, clock, font, small_font

def create_game_objects():
    """Create all game objects including characters and props"""
    # Call the create_game_objects method from KitchenProp
    dialog_system, player, dad, kitchen, props = KitchenProp.create_game_objects()
    fridge, table, *cabinets = props  # Unpack the props list
    return dialog_system, player, dad, kitchen, fridge, table, cabinets
    # Create dialog system
    # dialog_system = DialogSystem(WIDTH, HEIGHT)
    
    # # Create characters 
    # player = Character(200, HEIGHT//2, BLUE, is_player=True, image_path=("mc_walk_f1.png"), name="Tim")
    # dad = Character(WIDTH - 250, HEIGHT//2, RED, is_player=False, name="Dad")

    # # Create kitchen background
    # kitchen = Kitchen(WIDTH, HEIGHT, "assets/kitchen.png")
    
    # # Create kitchen props
    # fridge = KitchenProp(WIDTH - 150, 100, 100, 200, LIGHT_GRAY, "fridge", render_image=False)
    # table = KitchenProp(WIDTH//2 - 125, HEIGHT//2, 250, 75, None, "table", render_image=False)
    
    # return dialog_system, player, dad, kitchen, fridge, table, cabinets

# GAMEPLAY FUNCTIONS
# -------------------------------------------

def setup_fridge_minigame():
    """Set up the fridge minigame with items"""
    fridge_items = []
    tortellini_found = False
    
    # Create food items
    num_items = 12
    grid_cols = 3
    grid_rows = 4
    item_width = 40
    item_height = 40
    grid_spacing_x = (WIDTH - 200) // grid_cols
    grid_spacing_y = (HEIGHT - 200) // grid_rows
    
    # Place one tortellini randomly
    tortellini_pos = random.randint(0, num_items - 1)
    
    for i in range(num_items):
        col = i % grid_cols
        row = i // grid_cols
        x = 100 + col * grid_spacing_x
        y = 100 + row * grid_spacing_y
        
        item_type = "tortellini" if i == tortellini_pos else "other"
        fridge_items.append(FridgeItem(x, y, item_type))
    
    return fridge_items, tortellini_found

def handle_kitchen_events(event, player, fridge, game_state, fridge_collision_debounce):
    """Handle events in kitchen state"""
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and fridge_collision_debounce == 0:
        # Check if player is near fridge
        if abs(player.x - fridge.x) < player.width + 20 and abs(player.y - fridge.y) < player.height + 20:
            game_state = DIALOG
            # Position characters for dialog
            player.x = 200
            player.y = HEIGHT//2
            
    return game_state

def handle_dialog_events(event, dialog_system, game_state):
    """Handle events in dialog state"""
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        result = dialog_system.next_dialog()
        if result == "FRIDGE_MINIGAME":
            game_state = FRIDGE_MINIGAME
        elif result == "FIGHTING" or result == False:
            game_state = FIGHTING
        
    return game_state

def handle_fridge_minigame_events(event, fridge_items, game_state, tortellini_found, dialog_system):
    """Handle events in fridge minigame state"""
    if event.type == pygame.MOUSEBUTTONDOWN:
        # Check if mouse is over any item
        mouse_pos = pygame.mouse.get_pos()
        for item in fridge_items:
            if (mouse_pos[0] > item.x and mouse_pos[0] < item.x + item.width and
                mouse_pos[1] > item.y and mouse_pos[1] < item.y + item.height):
                if item.item_type == "tortellini":
                    tortellini_found = True
                    # Continue dialog after a brief pause
                    pygame.time.set_timer(pygame.USEREVENT, 1500)  # 1.5 seconds
                break
    
    # Return to dialog after finding tortellini
    if event.type == pygame.USEREVENT:
        pygame.time.set_timer(pygame.USEREVENT, 0)  # Cancel the timer
        game_state = DIALOG
        dialog_system.dialog_index += 1  # Skip the fridge dialog
    
    return game_state, tortellini_found

def handle_fighting_events(event, player, dad, game_state):
    """Handle events in fighting state"""
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        player.punching = True
        player.punch_timer = 10  # Punch duration
        
        # Check if punch hits dad and is in range
        if player.can_punch(dad):
            dad.health -= 10
            # Knockback effect
            if player.direction == 1:  # Facing right
                dad.x += 20
            else:  # Facing left
                dad.x -= 20
    
    return game_state

def handle_game_over_events(event, player, dad, dialog_system, game_state):
    """Handle events in game over state"""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            # Reset game
            player.health = 100
            dad.health = 100
            dialog_system.dialog_index = 0
            dialog_system.active = True
            game_state = KITCHEN
            player.x = 200
            player.y = HEIGHT//2
            dad.x = WIDTH - 300
            dad.y = HEIGHT//2
        elif event.key == pygame.K_q:
            running = False
    
    return game_state, running

def update_kitchen_state(screen, player, dad, kitchen, props, small_font, game_state):
    """Update and draw kitchen state."""
    # Draw kitchen background
    kitchen.draw(screen)

    # Draw debugging grid for the kitchen (optional)
    kitchen.draw_debug(screen, grid_size=50, color=(0, 255, 0))  # Green grid for debugging

    # Draw collision boxes for debugging
    for prop in props:
        prop.draw_debug(screen)
    # Debug props list
    print(f"Props: {[prop.type for prop in props]}")  # Debugging
    
    # Draw player and dad
    player.draw(screen)
    dad.draw(screen)

    # Player movement with arrow keys
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT]:
        print("Left key pressed")  # Debugging
        dx = -1
    if keys[pygame.K_RIGHT]:
        print("Right key pressed")  # Debugging
        dx = 1
    if keys[pygame.K_UP]:
        print("Up key pressed")  # Debugging
        dy = -1
    if keys[pygame.K_DOWN]:
        print("Down key pressed")  # Debugging
        dy = 1
    
    print(f"dx: {dx}, dy: {dy}, direction: {player.direction}")  # Debugging

    # Move the player using the move method
    player.move(dx, dy, props)

    # # Restrict player to the floor area
    # floor = next(prop for prop in props if prop.type == "floor")
    # if not floor.check_collision(player.x, player.y, player.width, player.height):
    #     # If the player is outside the floor area, revert the movement
    #     player.x -= dx * player.speed
    #     player.y -= dy * player.speed

    # # Prevent the player from moving through the table
    # table = next(prop for prop in props if prop.type == "table")
    # if table.check_collision(player.x, player.y, player.width, player.height):
    #     # If the player collides with the table, revert the movement
    #     player.x -= dx * player.speed
    #     player.y -= dy * player.speed

    # Check collision with the fridge
    fridge = next(prop for prop in props if prop.type == "fridge")
    if fridge.check_collision(player.x, player.y, player.width, player.height):
        print("Collision with fridge! Initiating tortellini minigame...")
        game_state = FRIDGE_MINIGAME

    # Draw instruction
    instruction_text = small_font.render("Use ARROW KEYS to move, SPACE to interact", True, GRAY)
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT - 30))

    return game_state

def update_dialog_state(screen, player, dad, cabinets, table, fridge, dialog_system):
    """Update and draw dialog state"""
    # Draw kitchen background for dialog
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, HEIGHT))
    
    # Draw kitchen props in background
    for cabinet in cabinets:
        cabinet.draw(screen)
    
    table.draw(screen)
    fridge.draw(screen)
    
    # Draw characters for dialog
    player.draw(screen)
    dad.draw(screen)
    
    # Draw and process dialog
    dialog_system.draw(screen)

def update_fridge_minigame_state(screen, fridge_items, tortellini_found, small_font, font):
    """Update and draw fridge minigame state"""
    # Draw fridge background
    pygame.draw.rect(screen, (230, 240, 250), (0, 0, WIDTH, HEIGHT))
    
    # Draw fridge shelves
    for i in range(4):
        pygame.draw.rect(screen, (200, 200, 200), (50, 150 + i*100, WIDTH - 100, 5))
    
    # Draw fridge items
    for item in fridge_items:
        item.draw(screen)
    
    # Draw cursor for selection
    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.circle(screen, BLACK, mouse_pos, 5, 1)
    
    # Draw instructions
    instruction_text1 = small_font.render("Move your mouse over an item and click to select", True, BLACK)
    instruction_text2 = small_font.render("Find the tortellini!", True, BLACK)
    screen.blit(instruction_text1, (WIDTH//2 - instruction_text1.get_width()//2, 30))
    screen.blit(instruction_text2, (WIDTH//2 - instruction_text2.get_width()//2, 60))
    
    # If tortellini is found
    if tortellini_found:
        found_text = font.render("You found the tortellini!", True, GREEN)
        screen.blit(found_text, (WIDTH//2 - found_text.get_width()//2, HEIGHT//2 - 50))

def update_fighting_state(screen, player, dad, cabinets, table, fridge, small_font):
    """Update and draw fighting state"""
    # Draw kitchen background for fight
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, HEIGHT))
    
    # Draw kitchen props in background (faded)
    s = pygame.Surface((WIDTH, HEIGHT))
    s.set_alpha(128)
    s.fill(LIGHT_BLUE)
    
    for cabinet in cabinets:
        cabinet.draw(s)
    
    table.draw(s)
    fridge.draw(s)
    
    screen.blit(s, (0, 0))
    
    # Draw boundary for fight area
    pygame.draw.rect(screen, GRAY, 
                    (PLAY_AREA_LEFT, PLAY_AREA_TOP, 
                     PLAY_AREA_RIGHT - PLAY_AREA_LEFT, 
                     PLAY_AREA_BOTTOM - PLAY_AREA_TOP), 2)
    
    # Player movement with arrow keys
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT]:
        dx = -1
    if keys[pygame.K_RIGHT]:
        dx = 1
    if keys[pygame.K_UP]:
        dy = -1
    if keys[pygame.K_DOWN]:
        dy = 1
    
    player.move(dx, dy)
    
    # Dad AI: move toward player
    if abs(dad.x - player.x) > 100:  # If too far, move toward player
        dad_dx = 0.5 if dad.x < player.x else -0.5
    else:  # If close enough, move randomly
        dad_dx = random.choice([-0.5, 0, 0.5])
    
    dad_dy = random.choice([-0.5, 0, 0.5])
    dad.move(dad_dx, dad_dy)
    
    # Dad occasionally tries to punch player
    if random.random() < 0.01 and dad.can_punch(player):
        dad.punching = True
        dad.punch_timer = 10
        player.health -= 5
    
    # Keep characters in play area
    player.x = max(PLAY_AREA_LEFT, min(player.x, PLAY_AREA_RIGHT - player.width))
    player.y = max(PLAY_AREA_TOP, min(player.y, PLAY_AREA_BOTTOM - player.height))
    dad.x = max(PLAY_AREA_LEFT, min(dad.x, PLAY_AREA_RIGHT - dad.width))
    dad.y = max(PLAY_AREA_TOP, min(dad.y, PLAY_AREA_BOTTOM - dad.height))
    
    # Punch timer
    if player.punch_timer > 0:
        player.punch_timer -= 1
    else:
        player.punching = False
        
    if dad.punch_timer > 0:
        dad.punch_timer -= 1
    else:
        dad.punching = False
    
    # Draw health bars
    pygame.draw.rect(screen, BLACK, (10, 10, 204, 24), 2)
    pygame.draw.rect(screen, GREEN, (12, 12, player.health * 2, 20))
    
    pygame.draw.rect(screen, BLACK, (WIDTH - 214, 10, 204, 24), 2)
    pygame.draw.rect(screen, GREEN, (WIDTH - 212, 12, dad.health * 2, 20))
    
    player_label = small_font.render("Tim", True, BLUE)
    dad_label = small_font.render("Dad", True, RED)
    screen.blit(player_label, (10, 40))
    screen.blit(dad_label, (WIDTH - 214, 40))
    
    # Draw characters
    player.draw(screen)
    dad.draw(screen)

    # Draw instruction text
    fight_instruction = small_font.render("Arrow keys to move, SPACE to punch!", True, BLACK)
    screen.blit(fight_instruction, (WIDTH//2 - fight_instruction.get_width()//2, HEIGHT - 30))
    
    # Game over conditions
    game_state = GAME_OVER if player.health <= 0 or dad.health <= 0 else FIGHTING
    return game_state

def update_game_over_state(screen, player, font, small_font):
    """Update and draw game over state"""
    # Display game over text
    if player.health <= 0:
        outcome_text = font.render("Dad wins! Your search for tortellini ends in defeat!", True, RED)
    else:
        outcome_text = font.render("You win! Dad respects your tortellini-finding skills!", True, BLUE)
        
    game_over_text = font.render("Game Over!", True, BLACK)
    restart_text = small_font.render("Press R to restart or Q to quit", True, GRAY)
    
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
    screen.blit(outcome_text, (WIDTH//2 - outcome_text.get_width()//2, HEIGHT//2))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))

# MAIN GAME FUNCTION
# -------------------------------------------

def main():
    # Initialize game
    screen, clock, font, small_font = initialize_game()
    
    # Create game objects
    dialog_system, player, dad, kitchen, fridge, table, cabinets = create_game_objects()
    
    # Game state
    game_state = KITCHEN
    
    # Fridge minigame items
    fridge_items = []
    tortellini_found = False
    
    # Main game loop
    running = True
    fridge_collision_debounce = 0
    
    while running:
        # print(f"Current game state: {game_state}")  # Debugging game state
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle state-specific events
            if game_state == KITCHEN:
                props = [fridge, table] + cabinets
                
                game_state = update_kitchen_state(screen, player, dad, kitchen, props, small_font, game_state)
            
                # Debounce for fridge interaction
                if fridge_collision_debounce > 0:
                    fridge_collision_debounce -= 1

            elif game_state == DIALOG:
                game_state = handle_dialog_events(event, dialog_system, game_state)
                if game_state == FRIDGE_MINIGAME:
                    fridge_items, tortellini_found = setup_fridge_minigame()
                elif game_state == FIGHTING:
                    # Reset positions for fight
                    player.x = WIDTH // 3
                    player.y = HEIGHT // 2
                    dad.x = 2 * WIDTH // 3
                    dad.y = HEIGHT // 2
            
            elif game_state == FRIDGE_MINIGAME:
                game_state, tortellini_found = handle_fridge_minigame_events(
                    event, fridge_items, game_state, tortellini_found, dialog_system)
            
            elif game_state == FIGHTING:
                game_state = handle_fighting_events(event, player, dad, game_state)
            
            elif game_state == GAME_OVER:
                game_state, running = handle_game_over_events(
                    event, player, dad, dialog_system, game_state)
        
        # Clear the screen
        screen.fill(WHITE)
        
        # Update and draw based on game state
        if game_state == KITCHEN:
            # Flatten cabinets into the props list
            props = [fridge, table] + cabinets
            # print(f"Props to render: {[prop.type for prop in props]}")  # Debugging
            game_state = update_kitchen_state(screen, player, dad, kitchen, props, small_font, game_state)
            # Update kitchen state
            fridge_collision = update_kitchen_state(screen, player, dad, kitchen, props, small_font, game_state)

            # Debounce for fridge interaction
            if fridge_collision_debounce > 0:
                fridge_collision_debounce -= 1
                
        elif game_state == DIALOG:
            update_dialog_state(screen, player, dad, cabinets, table, fridge, dialog_system)
            
        elif game_state == FRIDGE_MINIGAME:
            update_fridge_minigame_state(screen, fridge_items, tortellini_found, small_font, font)
        
        elif game_state == FIGHTING:
            game_state = update_fighting_state(screen, player, dad, cabinets, table, fridge, small_font)
                
        elif game_state == GAME_OVER:
            update_game_over_state(screen, player, font, small_font)
        
        # Update display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(60)

    # Quit the game
    pygame.quit()
    sys.exit()

def start_fight():
    main()  # This runs the fight scene when called

if __name__ == "__main__":
    start_fight()