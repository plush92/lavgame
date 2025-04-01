import pygame  # Import the pygame library for game development
import random  # Import the random library for random number generation
import os  # Import the os library for file path operations
from src.scenes.driving.pregame import PreGameScene
from src.scenes.driving.drivingscene import DrivingScene

# Constants
WIDTH, HEIGHT = 800, 600  # Screen dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window
ROAD_WIDTH = int(WIDTH * 0.7)  # Width of the road (70% of the screen width)
MARGIN = (WIDTH - ROAD_WIDTH) // 2  # Margin on the left and right of the road
LANE_WIDTH = ROAD_WIDTH // 4  # Width of each lane (road divided into 4 lanes)
OBSTACLE_SPEED = 2.5  # Speed at which obstacles move down the screen
SPAWN_RATE = 50  # Number of frames between spawning new obstacles

def main():
    clock = pygame.time.Clock()  # Create a clock object to control the frame rate
    pre_game = PreGameScene()  # Create the pre-game scene
    driving_scene = DrivingScene()  # Create the driving scene
    
    while pre_game.show_scene:  # Loop while the pre-game scene is active
        events = pygame.event.get()  # Get all events
        pre_game.handle_events(events)  # Handle events for the pre-game scene
        screen.fill((0, 0, 0))  # Clear the screen
        pre_game.draw(screen)  # Draw the pre-game scene
        pygame.display.flip()  # Update the display
        clock.tick(60)  # Limit the frame rate to 60 FPS
    
    while driving_scene.running:  # Loop while the driving scene is active
        events = pygame.event.get()  # Get all events
        driving_scene.handle_events(events)  # Handle events for the driving scene
        driving_scene.update()  # Update the driving scene
        driving_scene.draw(screen)  # Draw the driving scene
        pygame.display.flip()  # Update the display
        clock.tick(60)  # Limit the frame rate to 60 FPS
    
    print("Exited driving scene. Returning to main menu...")  # Print a message when exiting the driving scene

def start_driving():
    main()  # Start the main game loop
    import src.main_menu  # Import the main menu module
    src.main_menu.main_menu()  # Return to the main menu

if __name__ == "__main__":
    start_driving()  # Run the game if this script is executed directly
