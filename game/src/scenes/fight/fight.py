import pygame
import random
import math
import sys
from src.scenes.fight.character import Character
from src.scenes.fight.dialogue import DialogSystem
from src.scenes.fight.fridgeitem import FridgeItem
from src.scenes.fight.kitchenprop import KitchenProp
from src.scenes.fight.kitchen import Kitchen
from src.scenes.fight.FridgeMiniGame import FridgeMinigame
from src.scenes.fight.speechbubble import SpeechBubble
from src.scene_wait_for_continue import scene_wait_for_continue # Import the reusable function
import os

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

# Define the assets directory
assets_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets", "fridge_background.png"))
# Game assets
fridge_minigame = FridgeMinigame(WIDTH, HEIGHT, assets_path)

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

# GAMEPLAY FUNCTIONS
# -------------------------------------------

def handle_kitchen_first_scene_events(event, player, fridge, game_state, fridge_collision_debounce):
    """Handle events in kitchen state"""
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and fridge_collision_debounce == 0:
        # Check if player is near fridge
        if abs(player.x - fridge.x) < player.width + 20 and abs(player.y - fridge.y) < player.height + 20:
            game_state = DIALOG
            # Position characters for dialog
            player.x = 200
            player.y = HEIGHT//2
            
    return game_state

def handle_fridge_minigame_scene_events(event, fridge_minigame, game_state, tortellini_found, dialog_system):
    """Handle events in fridge minigame state."""
    # Delegate event handling to the FridgeMinigame class
    if fridge_minigame.handle_event(event):
        # If the tortellini is found, transition back to the dialog state
        game_state = DIALOG
        dialog_system.dialog_index += 1  # Move to the next dialog
        dialog_system.active = True
        tortellini_found = True

    return game_state, tortellini_found

def handle_kitchen_second_scene_events(event, dialog_system, game_state):
    """Handle events in dialog state"""
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        result = dialog_system.next_dialog()
        if result == "WALK_TO_FRIDGE":
            game_state = KITCHEN  # Return to the kitchen to allow the player to walk to the fridge
        elif result == "FRIDGE_MINIGAME":
            game_state = FRIDGE_MINIGAME
        elif result == "FIGHTING" or result == False:
            game_state = FIGHTING
        
    return game_state

def handle_fight_scene_events(event, player, dad, game_state):
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
    running = True
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

def kitchen_first_scene(screen, player, dad, kitchen, props, small_font, game_state):
    """Update and draw kitchen state."""
    # Draw kitchen background
    kitchen.draw(screen)

    # Draw debugging grid for the kitchen (optional)
    # kitchen.draw_debug(screen, grid_size=50, color=(0, 255, 0))  # Green grid for debugging

    # Draw collision boxes for debugging
    for prop in props:
        prop.draw_debug(screen)
    
    # Draw player
    player.draw(screen)

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

    # Move the player using the move method
    player.move(dx, dy, props)

    # Check collision with the fridge
    fridge = next(prop for prop in props if prop.type == "fridge")
    if fridge.check_collision(player.x, player.y, player.width, player.height):
        print("Collision with fridge! Initiating tortellini minigame...")
        game_state = FRIDGE_MINIGAME

    # Draw instruction
    instruction_text = small_font.render("Use ARROW KEYS to move, SPACE to interact", True, BLACK)
    # screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT - 30))

    return game_state

def fridge_minigame_scene(screen, fridge_minigame, tortellini_found, small_font, font, player):
    """Update and draw fridge minigame state."""
    # Draw the fridge minigame using the FridgeMinigame instance
    fridge_minigame.draw(screen)

    # Draw instructions
    instruction_text1 = small_font.render("Move your mouse over an item and click to select", True, BLACK)
    instruction_text2 = small_font.render("Find the tortellini!", True, BLACK)
    screen.blit(instruction_text1, (WIDTH // 2 - instruction_text1.get_width() // 2, 30))
    screen.blit(instruction_text2, (WIDTH // 2 - instruction_text2.get_width() // 2, 60))

    # # If tortellini is found, display a success message
    if fridge_minigame.tortellini_found:
            bubble = SpeechBubble(player, "Mmm. Can't wait to make this tortellini!", font)
            bubble.draw(screen)

def kitchen_second_scene(screen, kitchen, player, dad, cabinets, table, fridge, dialog_system):
    """Update and draw dialog state"""
    # Draw kitchen background for dialog
    kitchen.draw(screen)
    
    # Draw kitchen props in background
    # for cabinet in cabinets:
    #     cabinet.draw(screen)
    
    table.draw(screen)
    fridge.draw(screen)
    
    # Draw characters for dialog
    player.draw(screen)
    dad.draw(screen)
    
    # Draw and process dialog
    dialog_system.draw(screen)

    # Position characters for the fight when transitioning to FIGHTING
    if dialog_system.dialog_index == len(dialog_system.dialogs) - 1:  # Last dialog before fight
        player.x = fridge.x + fridge.width + 20  # Player next to the fridge
        player.y = fridge.y + fridge.height // 2 - player.height // 2
        dad.x = table.x + table.width + 20  # Dad on the other side of the table
        dad.y = table.y + table.height // 2 - dad.height // 2

def fight_scene(screen, player, dad, cabinets, table, fridge, small_font):
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
    if player.health <= 0 or dad.health <= 0:
        return GAME_OVER  # Transition to GAME_OVER state
    return FIGHTING

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
    
    # Fridge minigame instance
    fridge_minigame = None
    tortellini_found = False

    # Path to assets
    # fridge_background_path = os.path.join(os.path.dirname(__file__), "assets", "fridge_background.png")
    
    # Main game loop
    running = True
    fridge_collision_debounce = 0
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle state-specific events
            if game_state == KITCHEN:
                game_state = handle_kitchen_events(event, player, fridge, game_state, fridge_collision_debounce)
            elif game_state == DIALOG:
                game_state = handle_dialog_events(event, dialog_system, game_state)
            elif game_state == FRIDGE_MINIGAME:
                # Make sure fridge_minigame is initialized when we enter this state
                if fridge_minigame is None:
                    fridge_minigame = FridgeMinigame(WIDTH, HEIGHT, assets_path)
                game_state, tortellini_found = handle_fridge_minigame_events(event, fridge_minigame, game_state, tortellini_found, dialog_system)
            elif game_state == FIGHTING:
                game_state = handle_fighting_events(event, player, dad, game_state)
            elif game_state == GAME_OVER:
                game_state, running = handle_game_over_events(event, player, dad, dialog_system, game_state)
        
        # Clear the screen
        screen.fill(WHITE)
        
        # Update and draw based on game state
        props = [fridge, table] + cabinets
        
        if game_state == KITCHEN:
            game_state = kitchen_first_scene(screen, player, dad, kitchen, props, small_font, game_state)
            
            # Initialize fridge_minigame if transitioning to FRIDGE_MINIGAME
            if game_state == FRIDGE_MINIGAME and fridge_minigame is None:
                print("Initializing fridge_minigame...")
                fridge_minigame = FridgeMinigame(WIDTH, HEIGHT, assets_path)
                
            # Debounce for fridge interaction
            if fridge_collision_debounce > 0:
                fridge_collision_debounce -= 1
                
        elif game_state == DIALOG:
            kitchen_second_scene(screen, kitchen, player, dad, cabinets, table, fridge, dialog_system)
            
            # Handle transition to fighting state
            if game_state == FIGHTING:
                # Reset positions for fight
                player.x = WIDTH // 3
                player.y = HEIGHT // 2
                dad.x = 2 * WIDTH // 3
                dad.y = HEIGHT // 2
                
        elif game_state == FRIDGE_MINIGAME:
            # Make sure fridge_minigame is initialized when we enter this state
            if fridge_minigame is None:
                print("Initializing fridge_minigame in update...")
                fridge_minigame = FridgeMinigame(WIDTH, HEIGHT, assets_path)
            fridge_minigame_scene(screen, fridge_minigame, tortellini_found, small_font, font, player)
            
        elif game_state == FIGHTING:
            game_state = fight_scene(screen, player, dad, cabinets, table, fridge, small_font)
                
        elif game_state == GAME_OVER:
            result = scene_wait_for_continue(screen)
            if result == "continue":
                return "continue"
        
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