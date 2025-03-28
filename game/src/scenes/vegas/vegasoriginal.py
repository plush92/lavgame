import pygame
import sys
import random
import time
from pygame.math import Vector2
from src.scenes.vegas.paper import Paper
from src.scenes.vegas.player import Player
from src.scenes.vegas.wall import Wall
from src.scenes.vegas.character import Character

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
font_small = pygame.font.SysFont('Arial', 20)
font_medium = pygame.font.SysFont('Arial', 28)
font_large = pygame.font.SysFont('Arial', 36)

# Game states
STATE_DIALOGUE = 0
STATE_WALL_GAME = 1
STATE_ENDING = 2
game_state = STATE_DIALOGUE

# Create characters, dialogue, and dialogue options
tim = Character("Tim", WIDTH * 0.7, HEIGHT * 0.5, BLUE)
lav = Character("Lav", WIDTH * 0.3, HEIGHT * 0.5, RED)
# Create wall and player
paper = Paper()
player = Player()
wall = Wall(WIDTH, HEIGHT)
papers = []

# Dialogue system
dialogues = [ # List of dialogues
    {"speaker": "Lav", "text": "I don't know about this tim…"},
    {"speaker": "Lav", "text": "This is obviously an extremely unideal situation for me"},
    {"speaker": "Lav", "text": "But I feel….like…. I don't know"},
    {"speaker": "Tim", "text": "I love you"},
    {"speaker": "Lav", "text": "you are crazy and I don't trust you… yet."},
]
current_dialogue = 0 # Index of the current dialogue in the list of dialogues
dialogue_timer = 0 # Timer for displaying dialogues in milliseconds (ms)
DIALOGUE_SPEED = 2400  # milliseconds

# Flash effect
flash_active = False
flash_timer = 0
flash_duration = 500  # ms

# Vegas background elements
slot_machines = []
for i in range(5): # Create 5 slot machines
    slot_machines.append({ # Each slot machine is a dictionary
        'pos': Vector2(random.randint(50, WIDTH-50), random.randint(HEIGHT-200, HEIGHT-100)), # Position of the slot machine, in pixels, from top-left corner, x and y
        'size': Vector2(40, 60), # Size of the slot machine, width x height, in pixels
        'color': (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)) # Color of the slot machine, RGB, 0-255, random light colors only (no dark colors)
    })

lights = [] # Ceiling lights
for i in range(20): # Create 20 ceiling lights
    lights.append({ # Each light is a dictionary
        'pos': Vector2(random.randint(0, WIDTH), random.randint(0, 100)), # Position of the light, in pixels, from top-left corner, x and y
        'radius': random.randint(3, 8), # Radius of the light, in pixels
        'color': (random.randint(200, 255), random.randint(200, 255), 0), # Color of the light, RGB, 0-255, random light colors only (no dark colors)
        'blink_timer': random.randint(0, 1000), # Timer for blinking, in milliseconds
        'on': True # Whether the light is on or off
    })

# Casino background image
casino_image = pygame.image.load("assets/casino.jpeg")
image_rect = casino_image.get_rect()

# Game loop
def vegas(): # main game loop
    #initial variables
    global game_state, current_dialogue, dialogue_timer, flash_active, flash_timer, wall_broken
    global papers
    clock = pygame.time.Clock() # Create a clock object to control the frame rate
    last_time = pygame.time.get_ticks() # Get the time at the start of the game
    wall_broken = False # Whether the wall has been broken

    running = True # Boolean to control the game loop
    while running: # Main game loop
        # Calculate delta time
        current_time = pygame.time.get_ticks() # Get the current time
        dt = current_time - last_time # Calculate the time since the last frame
        last_time = current_time # Set the last time to the current time
        
        # Event handling
        for event in pygame.event.get(): # Get the list of events that have occurred since the last frame
            if event.type == pygame.QUIT: # If the user clicks the close button
                running = False # Stop the game loop
                
            elif event.type == pygame.KEYDOWN: # If the user presses a key
                if event.key == pygame.K_ESCAPE: # If the key is the escape key
                    running = False # Stop the game loop
                    
                # Skip dialogue with space
                elif event.key == pygame.K_SPACE and game_state == STATE_DIALOGUE: # If the key is the space key
                    current_dialogue += 1 # Skip to the next dialogue
                    if current_dialogue >= len(dialogues): # If there are no more dialogues
                        flash_active = True # Activate the flash effect
                        flash_timer = 0 # Reset the flash timer
                        
            elif event.type == pygame.MOUSEBUTTONDOWN and game_state == STATE_WALL_GAME: # If the user clicks the mouse
                if player.swing(): # If the player successfully swings the hammer
                    wall.hit(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) # Hit the wall at the mouse position
                    wall_broken = wall.hit(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) # Check if the wall has been broken
                    if wall_broken: # If the wall has been broken
                        game_state = STATE_ENDING # Change the game state to the ending state
                        for _ in range(50): # Create 50 divorce papers
                            papers.append(Paper()) # Add a new paper to the list of papers
                    hit_successful = wall.hit(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        
        # Update game state
        if game_state == STATE_DIALOGUE: # If the game state is the dialogue state
            # Update dialogue timer
            dialogue_timer += dt # Add the time since the last frame to the dialogue timer
            if dialogue_timer >= DIALOGUE_SPEED: # If the dialogue timer is greater than the dialogue speed
                dialogue_timer = 0 # Reset the dialogue timer
                current_dialogue += 1 # Move to the next dialogue
                if current_dialogue >= len(dialogues): # If there are no more dialogues
                    flash_active = True # Activate the flash effect
                    flash_timer = 0 # Reset the flash timer
                    
            # Handle flash effect
            if flash_active: # If the flash effect is active
                flash_timer += dt # Add the time since the last frame to the flash timer
                if flash_timer >= flash_duration: # If the flash timer is greater than the flash duration
                    flash_active = False # Deactivate the flash effect 
                    game_state = STATE_WALL_GAME # Change the game state to the wall game state
                    
        elif game_state == STATE_WALL_GAME: # If the game state is the wall game state
            # Movement controls
            keys = pygame.key.get_pressed() # Get the list of keys that are currently pressed
            direction = Vector2(0, 0) # Create a vector to store the movement direction
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: # If the left arrow key or the 'a' key is pressed
                direction.x = -1 # Set the x component of the direction vector to -1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: # If the right arrow key or the 'd' key is pressed
                direction.x = 1 # Set the x component of the direction vector to 1
            if keys[pygame.K_UP] or keys[pygame.K_w]: # If the up arrow key or the 'w' key is pressed
                direction.y = -1 # Set the y component of the direction vector to -1
            if keys[pygame.K_DOWN] or keys[pygame.K_s]: # If the down arrow key or the 's' key is pressed
                direction.y = 1 # Set the y component of the direction vector to 1
                
            if direction.length() > 0: # If the length of the direction vector is greater than 0
                direction = direction.normalize() # Normalize the direction vector
                
            player.move(direction) # Move the player in the specified direction
            player.update(dt) # Update the player

            if wall.breaking and wall.update(dt): # If the wall is breaking and the wall update function returns true
                wall_broken = True # Set the wall broken flag to true
                game_state = STATE_ENDING # Change the game state to the ending state
                # Create divorce papers for the ending
                for _ in range(50): # Create 50 divorce papers
                    papers.append(Paper()) # Add a new paper to the list of papers
            # If wall is breaking but animation not complete yet
            elif wall.breaking: # If the wall is breaking
                wall.update(dt) # Update the wall
            
        elif game_state == STATE_ENDING: # If the game state is the ending state
            # Update papers
            for paper in papers[:]: # For each paper in the list of papers
                if paper.update(): # If the paper update function returns true
                    papers.remove(paper) # Remove the paper from the list of papers
        
        # Update blinking lights
        for light in lights: # For each light in the list of lights
            light['blink_timer'] += dt # Add the time since the last frame to the blink timer
            if light['blink_timer'] > 1000: # If the blink timer is greater than 1000
                light['blink_timer'] = 0 # Reset the blink timer
                light['on'] = not light['on'] # Toggle the light on/off
                
        # Drawing
        # Draw casino background
        screen.fill(BLACK) # Fill the screen with a black background
        # screen.blit(casino_image, (0, 0)) # Fill the screen with a black background
        
        # Draw carpet pattern
        for y in range(0, HEIGHT, 40): # For each row of the carpet
            for x in range(0, WIDTH, 40): # For each column of the carpet
                if (x + y) % 80 == 0: # If the sum of the x and y coordinates is divisible by 80
                    pygame.draw.rect(screen, (100, 0, 100), (x, y, 40, 40)) # Draw a purple square
        
        # Draw ceiling lights
        for light in lights: # For each light in the list of lights
            if light['on']: # If the light is on
                pygame.draw.circle(screen, light['color'],  # Draw the light
                                (int(light['pos'].x), int(light['pos'].y)),  # Position of the light
                                light['radius']) # Radius of the light
                # Light glow
                pygame.draw.circle(screen, (255, 255, 100, 50),  # Draw the light glow
                                (int(light['pos'].x), int(light['pos'].y)),  # Position of the light
                                light['radius'] * 3) # Radius of the light glow
        
        # Draw slot machines
        for machine in slot_machines: # For each slot machine in the list of slot machines
            pygame.draw.rect(screen, machine['color'],  # Draw the slot machine
                            (machine['pos'].x, machine['pos'].y,  # Position of the slot machine
                            machine['size'].x, machine['size'].y)) # Size of the slot machine
            # Screen
            pygame.draw.rect(screen, BLACK,  # Draw the screen of the slot machine
                            (machine['pos'].x + 5, machine['pos'].y + 5,  # Position of the screen
                            machine['size'].x - 10, machine['size'].y / 2 - 5)) # Size of the screen
        
        # Draw state-specific elements
        if game_state == STATE_DIALOGUE: # If the game state is the dialogue state
            # Draw characters
            tim.draw() # Draw Tim
            lav.draw() # Draw Lav
            
            # Draw dialogue
            if current_dialogue < len(dialogues): # If there are more dialogues to display
                dialogue = dialogues[current_dialogue] # Get the current dialogue
                speaker_text = font_small.render(f"{dialogue['speaker']}:", True, WHITE) # Render the speaker text
                dialogue_text = font_small.render(dialogue['text'], True, WHITE) # Render the dialogue text
                
                # Background for dialogue
                text_box = pygame.Rect(WIDTH//2 - 300, HEIGHT - 150, 600, 100) # Create a rectangle for the dialogue text
                pygame.draw.rect(screen, (0, 0, 50), text_box) # Draw the rectangle
                pygame.draw.rect(screen, GOLD, text_box, 3) # Draw the outline of the rectangle
                
                # Display text
                screen.blit(speaker_text, (text_box.x + 20, text_box.y + 20)) # Draw the speaker text
                screen.blit(dialogue_text, (text_box.x + 20, text_box.y + 50)) # Draw the dialogue text
            
            # Draw flash
            if flash_active: # If the flash effect is active
                alpha = max(0, min(255, 255 - (flash_timer / flash_duration) * 255)) # Calculate the alpha value for the flash effect
                flash_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) # Create a surface for the flash effect
                flash_surface.fill((255, 255, 255, alpha)) # Fill the surface with a white color and the calculated alpha value
                screen.blit(flash_surface, (0, 0)) # Draw the flash surface to the screen
                
        elif game_state == STATE_WALL_GAME: # If the game state is the wall game state
            # Draw characters on either side of wall
            tim.pos.x = WIDTH * 0.2 # Set Tim's x position
            lav.pos.x = WIDTH * 0.8 # Set Lav's x position
            tim.draw() # Draw Tim
            lav.draw() # Draw Lav
            
            # Draw wall
            wall.draw(screen) # Draw the wall
            
            # Draw player
            player.draw() # Draw the player
            
            # Instructions
            instr1 = font_small.render("Break the wall! Move with WASD/Arrows", True, WHITE) # Render the instructions text
            instr2 = font_small.render("Click to swing the hammer", True, WHITE) # Render the instructions text
            screen.blit(instr1, (10, 10)) # Draw the instructions text
            screen.blit(instr2, (10, 40)) # Draw the instructions text
            
        elif game_state == STATE_ENDING: # If the game state is the ending state
            # Draw papers
            for paper in papers: # For each paper in the list of papers
                paper.draw() # Draw the paper
                
            # Draw characters reunited
            tim.pos.x = WIDTH * 0.4 # Set Tim's x position
            lav.pos.x = WIDTH * 0.6 # Set Lav's x position
            tim.draw() # Draw Tim
            lav.draw() # Draw Lav
            
            # Draw ending text
            congrats = font_large.render("Congratulations!", True, GOLD) # Render the ending text in large font with a gold color 
            screen.blit(congrats, (WIDTH//2 - congrats.get_width()//2, 100)) # Draw the ending text at the center of the screen with an offset of 100 pixels from the top of the screen
            
            earned = font_medium.render("You've earned....her love", True, WHITE) # Render the ending text in medium font with a white color 
            screen.blit(earned, (WIDTH//2 - earned.get_width()//2, 150)) # Draw the ending text at the center of the screen with an offset of 150 pixels from the top of the screen
            
            stuck = font_medium.render("and now you're stuck with her!", True, WHITE) # Render the ending text in medium font with a white color
            screen.blit(stuck, (WIDTH//2 - stuck.get_width()//2, 190)) # Draw the ending text at the center of the screen with an offset of 190 pixels from the top of the screen
            
            cvs = font_medium.render("Hope you like CVS runs at midnight!", True, WHITE) # Render the ending text in medium font with a white color
            screen.blit(cvs, (WIDTH//2 - cvs.get_width()//2, 230)) # Draw the ending text at the center of the screen with an offset of 230 pixels from the top of the screen
            
            restart = font_small.render("Press ESC to quit", True, WHITE) # Render the restart text in small font with a white color
            screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT - 50)) # Draw the restart text at the center of the screen with an offset of 50 pixels from the bottom of the screen
        
        # Update display
        pygame.display.flip() # Update the display
        clock.tick(60) # Cap the frame rate at 60 frames per second

# Main function
def start_vegas(): # main function
    try: # Try to run the game
        app = vegas() 
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    start_vegas()