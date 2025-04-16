# Imports
import pygame
import sys
import random
import time
from pygame.math import Vector2
from src.scenes.vegas.paper import Paper
from src.scenes.vegas.wall import Wall
from src.scenes.vegas.screenshaker import ScreenShaker
from src.scenes.vegas.character import Character
from src.scenes.vegas.speechbubble import SpeechBubble
from src.scenes.vegas.dynamictext import DynamicText
from src.scenes.vegas.ending import EndingSequence

# Initialize pygame, intial screen variables, colors, font
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tim and Lav in Vegas")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
BRICK_COLOR = (165, 42, 42)
GRAY = (150, 150, 150)

# Fonts
font_small = pygame.font.SysFont('Arial', 20, bold=False)
font_medium = pygame.font.SysFont('Arial', 28, bold=False)
font_large = pygame.font.SysFont('Arial', 36, bold=False)

# Game states
STATE_DIALOGUE = 0
STATE_WALL_GAME = 1
STATE_ENDING = 2

# Create characters
tim = Character(name="tim", x=400, y=500, color=(255, 0, 0), image_path="src/assets/tim.png")
lav = Character(name="lav", x=400, y=300, color=(255, 255, 0), image_path="src/assets/lav.png")

# Create wall
wall = Wall(WIDTH, HEIGHT)

# Flash effect settings
FLASH_DURATION = 500  # ms
DIALOGUE_SPEED = 2400  # milliseconds

# Casino background image
casino_image = pygame.image.load("src/assets/casino.png")

# Screen shaker
screen_shaker = ScreenShaker()

# Ending sequence
ending = EndingSequence(screen, WIDTH, HEIGHT, tim, lav)

# Function to create divorce papers
def create_papers(count=50):
    """Create divorce papers for the ending"""
    return [Paper() for _ in range(count)] # Create a list of papers

# Game instructions
instructions = [
    {"text": "Move with W-A-S-D"},
    {"text": "Click to swing hammer"},
]

# Dialogue system
dialogues = [
    {"speaker": "Lav", "text": "I don't know about this tim…"},
    {"speaker": "Lav", "text": "This is obviously an extremely unideal situation for me"},
    {"speaker": "Lav", "text": "But I feel….like…. I don't know"},
    {"speaker": "Tim", "text": "I love you"},
    {"speaker": "Lav", "text": "you are crazy and I don't trust you… yet."},
]

# Function to draw text on the screen
def draw_text(text, font, color, x, y, centered=False, bold=False):
    if bold:
        temp_font = pygame.font.SysFont('Arial', 20, bold=True)  # Create a bold version
    else:
        temp_font = font  # Use the original font
    rendered_text = font.render(text, True, color) # Render the text
    position = (x - rendered_text.get_width()//2, y) if centered else (x, y) # Center the text if needed
    screen.blit(rendered_text, position) # Blit the text to the screen

# Function to handle dialogue state
def handle_dialogue_state(dt, game_vars): # Handle the dialogue state logic
    """Handle the dialogue state logic"""
    # Update dialogue timer
    game_vars["dialogue_timer"] += dt # Increment the dialogue timer
    if game_vars["dialogue_timer"] >= DIALOGUE_SPEED: # If the timer exceeds the dialogue speed
        game_vars["dialogue_timer"] = 0 # Reset the timer
        game_vars["current_dialogue"] += 1 # Move to the next dialogue
        if game_vars["current_dialogue"] >= len(dialogues): # If all dialogues are done
            game_vars["flash_active"] = True # Start flash effect
            game_vars["flash_timer"] = 0 # Reset flash timer
            
    # Handle flash effect
    if game_vars["flash_active"]: # If flash effect is active
        game_vars["flash_timer"] += dt  # Increment the flash timer
        if game_vars["flash_timer"] >= FLASH_DURATION / 1000.0: # If the flash duration is over
            game_vars["flash_active"] = False # Stop flash effect
            game_vars["game_state"] = STATE_WALL_GAME # Move to wall game state
    
    # Draw characters
    tim.draw(screen, dt) 
    lav.draw(screen, dt)
    
    # Draw dialogue using speech bubble
    if game_vars["current_dialogue"] < len(dialogues): # If there are dialogues left
        dialogue = dialogues[game_vars["current_dialogue"]] # Get the current dialogue
        speaker_name = dialogue["speaker"] # Get the speaker name
        speaker_character = tim if speaker_name == "Tim" else lav # Get the character object
        bubble = SpeechBubble(speaker_character, dialogue["text"], font_small) # Create a speech bubble
        bubble.draw(screen) # Draw the speech bubble on the screen
    
    # Draw flash
    if game_vars["flash_active"]: # If flash effect is active
        alpha = max(0, min(255, 255 - (game_vars["flash_timer"] / FLASH_DURATION) * 255)) # Calculate alpha value for the flash effect
        flash_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) # Create a surface for the flash effect
        flash_surface.fill((255, 255, 255, alpha)) # Fill the surface with white color and alpha value
        screen.blit(flash_surface, (0, 0)) # Blit the flash surface to the screen

# Encouragement texts cycling
encouragement_texts = [
    "Her walls are up! You must break through!",
    "Her spirit cries for true connection!",
    "This is your destiny!",
    "Only true effort can break this barrier!",
    "Her heart is locked, but you have the key!"
]
encouragement_index = 0  # Track which text is displayed
encouragement_rendering = DynamicText(encouragement_texts[0], font_small, GOLD, 150, 10, bold=True)

# Function to handle wall game state
def handle_wall_game_state(dt, game_vars):
    global encouragement_index
    # Update player
    tim.move(dt)
    tim.update(dt)
    wall.update(dt)
    
    # Check for wall hit
    if tim.check_wall_hit(wall):
        print("Hit detected!")  # Debug print
        screen_shaker.shake(10, 0.5)  # Shake for 0.5 seconds with intensity 10
        wall.hit()  # Hit the wall

        # Cycle encouragement text
        encouragement_index = (encouragement_index + 1) % len(encouragement_texts)
        encouragement_rendering.text = encouragement_texts[encouragement_index]  # Update displayed text
        encouragement_rendering.trigger_animation(pop_scale=1.5, shake_intensity=5, duration=0.5)
    encouragement_rendering.update(dt)

    # Check for wall destruction ONLY after updating and drawing
    if wall.is_destroyed and wall.fade_alpha <= 0:
        print("Wall destroyed. Transitioning to ending state")  # Debug print
        game_vars["game_state"] = STATE_ENDING
        ending.papers = create_papers()  # Pass papers to the ending sequence
    
    # Update screen shake effect
    screen_shaker.update(dt)
    offset_x, offset_y = screen_shaker.get_offset()
    
    # Draw everything with applied screen shake
    wall.draw(screen, offset_x, offset_y)
    tim.draw(screen, dt, offset_x, offset_y)
    # lav.draw(screen, dt, offset_x, offset_y)

    # Draw encouragement texts, looping after every hit.
    encouragement_rendering.draw(screen)

    # Draw instructions at the bottom left
    bottom_y = screen.get_height() - 100  # Adjust to fit instructions
    for i, instr in enumerate(instructions):
        draw_text(instr["text"], font_small, WHITE, 10, bottom_y + i * 30)

# Function to handle ending state
def handle_ending_state(dt, game_vars):
    """Handle the ending state logic."""
    ending.play(dt)  # Play the ending sequence

# Function to handle events
def handle_events(game_vars):
    """Handle pygame events"""
    for event in pygame.event.get(): # Check for events
        if event.type == pygame.QUIT: # Quit event
            return False 
                
        elif event.type == pygame.KEYDOWN: # Key press event
            if event.key == pygame.K_ESCAPE: # Escape key
                return False
                    
            # Skip dialogue with space
            elif event.key == pygame.K_SPACE and game_vars["game_state"] == STATE_DIALOGUE: # Space key
                game_vars["current_dialogue"] += 1 # Skip to next dialogue
                if game_vars["current_dialogue"] >= len(dialogues): # If all dialogues are done
                    game_vars["flash_active"] = True # Start flash effect
                    game_vars["flash_timer"] = 0 # Reset flash timer
                        
        elif event.type == pygame.MOUSEBUTTONDOWN and game_vars["game_state"] == STATE_WALL_GAME: # Mouse click event
            if tim.swing(): # If the player swings the hammer
                if game_vars["wall_broken"]: # If the wall is broken
                    game_vars["game_state"] = STATE_ENDING # Go to ending state
                    game_vars["papers"] = create_papers() # Create papers for the ending
    
    return True # Keep the game running

# Main game loop
def vegas():
    """Main game loop"""
    # Game variables
    game_vars = {
        "game_state": STATE_DIALOGUE,
        "current_dialogue": 0,
        "dialogue_timer": 0,
        "flash_active": False,
        "flash_timer": 0,
        "wall_broken": False,
        "papers": []
    }

    # Clock and time variables
    clock = pygame.time.Clock() # Create a clock object for controlling the frame rate
    last_time = pygame.time.get_ticks() # Get the current time in milliseconds
    
    # Game loop
    running = True
    while running:
        # Calculate delta time
        current_time = pygame.time.get_ticks()
        dt = (current_time - last_time) / 1000.0
        last_time = current_time
        
        # Handle events
        running = handle_events(game_vars)
        
        # Draw background
        screen.blit(casino_image, (0, 0))
        
        # Handle state-specific logic
        if game_vars["game_state"] == STATE_DIALOGUE:
            handle_dialogue_state(dt, game_vars)
        elif game_vars["game_state"] == STATE_WALL_GAME:
            handle_wall_game_state(dt, game_vars)
        elif game_vars["game_state"] == STATE_ENDING:
            handle_ending_state(dt, game_vars)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)

# start the game
def start_vegas():
    """Main function"""
    try:
        vegas() 
    except Exception as e:
        print(f"Error: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    start_vegas()