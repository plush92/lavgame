import pygame
import os
from src.scenes.fight.KitchenFirstScene import KitchenFirstScene
from src.scenes.fight.KitchenSecondScene import KitchenSecondScene
from src.scenes.fight.FridgeMinigameScene import FridgeMinigameScene
from src.scenes.fight.FightScene import FightScene
from src.scenes.fight.GameOver import GameOver
from src.scenes.fight.kitchenprop import KitchenProp
from src.scenes.fight.constants import WIDTH, HEIGHT, PLAY_AREA_LEFT, PLAY_AREA_RIGHT, PLAY_AREA_TOP, PLAY_AREA_BOTTOM

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("LavGame")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Initialize game objects
        self.dialog_system, self.player, self.dad, self.kitchen, self.props = KitchenProp.create_game_objects()
        self.dialog_system.dialogs = self.dialog_system.dialog_first  # Start with dialog_first
        self.fridge_minigame = None
        self.tortellini_found = False

        # State management
        self.states = {
            "KITCHEN_FIRST": KitchenFirstScene(),
            "FRIDGE_MINIGAME": FridgeMinigameScene(WIDTH, HEIGHT, "src/assets/fridge_background.png"),
            "KITCHEN_SECOND": KitchenSecondScene(),
            "FIGHT": FightScene(),
            "GAME_OVER": GameOver(),
        }
        self.current_state = self.states["KITCHEN_FIRST"]
        self.running = True
    
    def show_intro_screen(self):
        """Display a black screen with the text 'With Dad...' before the game starts."""
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        intro_text = self.font.render("With Dad...", True, (255, 255, 255))  # White text
        text_rect = intro_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(intro_text, text_rect)  # Draw the text on the screen
        pygame.display.flip()  # Update the display
        pygame.time.delay(2000)  # Pause for 2 seconds

    def change_state(self, state_name):
        """Change the current game state."""
        if state_name == "KITCHEN_SECOND":
            self.dialog_system.dialogs = self.dialog_system.dialog_second  # Switch to dialog_second
        self.current_state = self.states[state_name]

    def handle_events(self, event):
        """Delegate event handling to the current state."""
        self.current_state.handle_events(event, self)

    def update(self):
        """Delegate updates to the current state."""
        self.current_state.update(self)

    def draw(self):
        """Delegate rendering to the current state."""
        self.current_state.draw(self.screen, self)

    def run(self):
        """Main game loop."""
        self.show_intro_screen()  # Show the intro screen before starting the game
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_events(event)

            self.update()
            self.screen.fill((255, 255, 255))  # Clear the screen
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

def start_fight():
    game = Game()  # This runs the fight scene when called
    game.run()

if __name__ == "__main__":
    start_fight()