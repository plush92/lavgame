import pygame
import random
import math
import sys

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
        self.dialogs = [
            {"speaker": "Tim", "text": "Oh hey dad"},
            {"speaker": "Dad", "text": "The prodigal son! I am a god and therefore you are the messiah, oh anointed one!"},
            {"speaker": "Tim", "text": "I am actually better and stronger than you"},
            {"speaker": "Tim", "text": "*opens fridge to look for tortellini*"},
            {"speaker": "Dad", "text": "You've done some innocuous thing that has made me irrationally angry!"},
            {"speaker": "Tim", "text": "Your anger has made me angry!"},
            {"speaker": "Dad", "text": "You are my son you must obey me!"},
            {"speaker": "Tim", "text": "I have an oppositionally defiant personality because I was both spoiled rotten and ignored!"},
            {"speaker": "Dad", "text": "I don't have the proper skills needed to manage my emotions so my anger is building!"},
            {"speaker": "Tim", "text": "And because you don't, I never learned them either and so my anger is also building!"},
            {"speaker": "Dad", "text": "Ahhh!"},
            {"speaker": "Tim", "text": "Grrrr!"},
            {"speaker": "Narrator", "text": "Fight ensues..."},
        ]

    def draw(self, surface):
        if not self.active or self.dialog_index >= len(self.dialogs):
            return False
            
        # Dialog box
        box_height = 150
        pygame.draw.rect(surface, WHITE, (50, self.height - box_height - 50, self.width - 100, box_height))
        pygame.draw.rect(surface, BLACK, (50, self.height - box_height - 50, self.width - 100, box_height), 2)
        
        dialog = self.dialogs[self.dialog_index]
        
        # Speaker label
        speaker_color = BLUE if dialog["speaker"] == "Tim" else RED if dialog["speaker"] == "Dad" else GREEN
        speaker_text = self.font.render(dialog["speaker"] + ":", True, speaker_color)
        surface.blit(speaker_text, (70, self.height - box_height - 40))
        
        # Dialog text - with word wrap
        words = dialog["text"].split(' ')
        line = ""
        y_offset = 0
        for word in words:
            test_line = line + word + " "
            text_width = self.font.size(test_line)[0]
            if text_width < self.width - 150:
                line = test_line
            else:
                text = self.font.render(line, True, BLACK)
                surface.blit(text, (70, self.height - box_height - 5 + y_offset))
                y_offset += 30
                line = word + " "
        
        text = self.font.render(line, True, BLACK)
        surface.blit(text, (70, self.height - box_height - 5 + y_offset))
        
        # Continue prompt
        continue_text = self.small_font.render("Press SPACE to continue...", True, GRAY)
        surface.blit(continue_text, (self.width - 230, self.height - 80))
        
        return True

    def next_dialog(self):
        self.dialog_index += 1
        if self.dialog_index >= len(self.dialogs):
            self.active = False
            return False
        
        # Special handling: When reaching the fridge dialog, trigger fridge minigame
        if self.dialog_index == 3:  # *opens fridge to look for tortellini*
            return "FRIDGE_MINIGAME"
        elif self.dialog_index == len(self.dialogs) - 1:  # Fight ensues
            return "FIGHTING"
        
        return True