import pygame
import random
import math
import sys
from src.scenes.fight.speechbubble import SpeechBubble

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

# Dialog class
class DialogSystem:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.dialog_index = 0
        self.active = True
        self.dialog_first = [
            {"speaker": "Tim", "text": "So hungry. Can't wait to eat some tortellini!"},
            {"speaker": "Tim", "text": "...Oh, hey dad"},
            {"speaker": "Dad", "text": "The prodigal son! I am a god and therefore you are the messiah, oh anointed one!"},
            {"speaker": "Tim", "text": "I am actually better and stronger than you"}
        ]

        self.dialog_second = [
            #Open fridge to look for tortellini*
            {"speaker": "Tim", "text": "Found it!"},
            {"speaker": "Dad", "text": "You've done some innocuous thing that has made me irrationally angry!"},
            {"speaker": "Tim", "text": "Your anger has made me angry!"},
            {"speaker": "Dad", "text": "You are my son you must obey me!"},
            {"speaker": "Tim", "text": "I have an oppositionally defiant personality because I was both spoiled rotten and ignored!"},
            {"speaker": "Dad", "text": "I don't have the proper skills needed to manage my emotions so my anger is building!"},
            {"speaker": "Tim", "text": "And because you don't, I never learned them either and so my anger is also building!"},
            {"speaker": "Dad", "text": "Ahhh!"},
            {"speaker": "Tim", "text": "Grrrr!"},
            # {"speaker": "Narrator", "text": "Fight ensues..."},
        ]

        self.dialogs = self.dialog_first

    def draw(self, surface, characters):
        """
        Draw the current dialogue using the SpeechBubble class.

        Args:
            surface (pygame.Surface): The surface to draw on.
            characters (dict): A dictionary mapping character names to their instances.
        """
        if not self.active or self.dialog_index >= len(self.dialogs): # Check if dialog is active and index is valid
            return False

        # Get the current dialogue
        dialog = self.dialogs[self.dialog_index] # Get the current dialog
        speaker_name = dialog["speaker"] # Get the speaker's name
        text = dialog["text"] # Get the text to display

        # Get the character instance for the speaker
        character = characters.get(speaker_name, None)

        # Create and draw the speech bubble
        if character:
            bubble = SpeechBubble(character, text, self.font)
            bubble.draw(surface)
        else:
            print(f"Warning: Character '{speaker_name}' not found for dialogue.")

        return True

    def next_dialog(self):
            """
            Advance to the next dialogue in the sequence.

            Returns:
                str or None: A string indicating the next game state (e.g., "FIGHTING"),
                            or None if there is no special transition.
            """
            if self.dialog_index < len(self.dialogs) - 1:
                self.dialog_index += 1
                print(f"Advancing to dialogue index {self.dialog_index}")  # Debugging
                return None  # No special transition
            else:
                self.active = False  # End of dialogue
                print("Dialogue finished.")  # Debugging
                return "FIGHTING"  # Example: Transition to the fighting state