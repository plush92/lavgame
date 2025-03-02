import pygame
import sys
import random
import time
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.font.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)
PURPLE = (128, 0, 128)

# Game states
MENU = 0
GAMEPLAY = 1
DATE = 2
RESULTS = 3

class Character:
    def __init__(self, name, traits, interests, image_path):
        self.name = name
        self.traits = traits  # personality traits
        self.interests = interests  # hobbies and interests
        self.compatibility = 0  # compatibility score with player
        self.responses = []  # player's responses to this character
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (200, 200))
        
    def calculate_compatibility(self, player_responses):
        # Simple compatibility calculation based on matching responses
        self.compatibility = 0
        for i, response in enumerate(player_responses):
            if i < len(self.responses):
                if self.responses[i] == response:
                    self.compatibility += 20  # 20% per matching response
        return self.compatibility

class SpeedDatingGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Speed Dating Simulator")
        self.clock = pygame.time.Clock()
        self.state = MENU
        
        # Fonts
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.heading_font = pygame.font.SysFont("Arial", 32, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)
        
        # Timer
        self.timer = 60  # seconds per date
        self.last_time = time.time()
        
        # Game variables
        self.current_date_index = 0
        self.current_question_index = 0
        self.player_responses = {}
        
        # Create characters
        self.create_characters()
        
        # Create questions
        self.questions = [
            "What do you like to do in your free time?",
            "What's your idea of a perfect date?",
            "Do you prefer staying in or going out?",
            "Are you a morning person or a night owl?",
            "What's the most important quality in a relationship?"
        ]
        
        # Response options (different for each question)
        self.response_options = [
            ["Read/Watch movies", "Exercise/Sports", "Art/Music", "Travel/Adventure", "Video games"],
            ["Dinner and a movie", "Adventure activity", "Museum/Cultural event", "Beach/Park picnic", "Cozy night in"],
            ["Staying in", "Going out", "Depends on the mood", "Both equally", "Prefer outdoors"],
            ["Morning person", "Night owl", "Depends on the day", "Afternoon person", "Flexible"],
            ["Trust", "Communication", "Humor", "Independence", "Passion"]
        ]
        
        # Set preferred responses for each character (index of the response they like)
        self.alex.responses = [2, 1, 1, 3, 0]  # Art/Music, Adventure, Going out, Depends on the day, Trust
        self.jamie.responses = [0, 4, 0, 1, 2]  # Read/Movies, Cozy night, Staying in, Night owl, Humor
        self.taylor.responses = [1, 3, 4, 0, 3]  # Exercise, Beach/Park, Outdoors, Morning person, Independence
        self.morgan.responses = [3, 2, 2, 4, 1]  # Travel, Cultural, Depends on mood, Flexible, Communication
        self.jordan.responses = [4, 0, 3, 2, 4]  # Games, Dinner/Movie, Both equally, Afternoon, Passion
        
        # Buttons
        self.menu_buttons = [
            {"text": "Start Game", "rect": pygame.Rect(300, 300, 200, 50), "action": self.start_game},
            {"text": "Quit", "rect": pygame.Rect(300, 370, 200, 50), "action": self.quit_game}
        ]
        
        self.back_button = {"text": "Back", "rect": pygame.Rect(50, 520, 100, 50), "action": self.go_to_menu}
        self.next_date_button = {"text": "Next Date", "rect": pygame.Rect(600, 520, 150, 50), "action": self.next_date}
        
    def create_characters(self):
        # In a real game, you would use actual images
        default_img = "character.png"  # Replace with an actual image path
        
        try:
            # Create a default image if none is available
            pygame.draw.rect(pygame.Surface((200, 200)), PURPLE, (0, 0, 200, 200))
            pygame.image.save(pygame.Surface((200, 200)), default_img)
        except:
            pass
        
        self.alex = Character(
            "Alex", 
            ["Creative", "Outgoing", "Spontaneous"],
            ["Art", "Music", "Travel"],
            default_img
        )
        
        self.jamie = Character(
            "Jamie", 
            ["Thoughtful", "Quiet", "Intellectual"],
            ["Reading", "Movies", "Cooking"],
            default_img
        )
        
        self.taylor = Character(
            "Taylor", 
            ["Athletic", "Adventurous", "Energetic"],
            ["Sports", "Hiking", "Fitness"],
            default_img
        )
        
        self.morgan = Character(
            "Morgan", 
            ["Balanced", "Curious", "Empathetic"],
            ["Photography", "Travel", "Psychology"],
            default_img
        )
        
        self.jordan = Character(
            "Jordan", 
            ["Tech-savvy", "Humorous", "Relaxed"],
            ["Gaming", "Technology", "Films"],
            default_img
        )
        
        self.characters = [self.alex, self.jamie, self.taylor, self.morgan, self.jordan]
        random.shuffle(self.characters)  # Randomize order
        
    def start_game(self):
        self.state = GAMEPLAY
        self.current_date_index = 0
        self.current_question_index = 0
        self.player_responses = {char.name: [] for char in self.characters}
        self.timer = 60
        
    def next_date(self):
        self.current_date_index += 1
        self.current_question_index = 0
        self.timer = 60
        
        if self.current_date_index >= len(self.characters):
            self.calculate_results()
            self.state = RESULTS
            
    def calculate_results(self):
        for character in self.characters:
            character.calculate_compatibility(self.player_responses[character.name])
        
        # Sort characters by compatibility
        self.characters.sort(key=lambda x: x.compatibility, reverse=True)
        
    def go_to_menu(self):
        self.state = MENU
    
    def quit_game(self):
        pygame.quit()
        sys.exit()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit_game()
                
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Handle menu buttons
                    if self.state == MENU:
                        for button in self.menu_buttons:
                            if button["rect"].collidepoint(mouse_pos):
                                button["action"]()
                    
                    # Handle back button
                    if self.state in [GAMEPLAY, RESULTS]:
                        if self.back_button["rect"].collidepoint(mouse_pos):
                            self.back_button["action"]()
                    
                    # Handle next date button
                    if self.state == GAMEPLAY and self.current_question_index >= len(self.questions):
                        if self.next_date_button["rect"].collidepoint(mouse_pos):
                            self.next_date_button["action"]()
                    
                    # Handle response options
                    if self.state == GAMEPLAY and self.current_question_index < len(self.questions):
                        current_character = self.characters[self.current_date_index]
                        options = self.response_options[self.current_question_index]
                        
                        for i, option in enumerate(options):
                            rect = pygame.Rect(150, 300 + (i * 50), 500, 40)
                            if rect.collidepoint(mouse_pos):
                                self.player_responses[current_character.name].append(i)
                                self.current_question_index += 1
                                break
    
    def update(self):
        # Update timer
        current_time = time.time()
        if self.state == GAMEPLAY and self.current_question_index < len(self.questions):
            self.timer -= (current_time - self.last_time)
            
            if self.timer <= 0:
                # Auto-select a random answer if time runs out
                current_character = self.characters[self.current_date_index]
                options = self.response_options[self.current_question_index]
                random_choice = random.randint(0, len(options) - 1)
                self.player_responses[current_character.name].append(random_choice)
                self.current_question_index += 1
                self.timer = 60
        
        self.last_time = current_time
    
    def draw_menu(self):
        self.screen.fill(PINK)
        
        # Draw title
        title = self.title_font.render("Speed Dating Simulator", True, PURPLE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        
        # Draw description
        desc1 = self.text_font.render("Meet 5 interesting singles and find your perfect match!", True, BLACK)
        desc2 = self.text_font.render("Answer questions and see who you're most compatible with.", True, BLACK)
        self.screen.blit(desc1, (SCREEN_WIDTH//2 - desc1.get_width()//2, 180))
        self.screen.blit(desc2, (SCREEN_WIDTH//2 - desc2.get_width()//2, 210))
        
        # Draw buttons
        for button in self.menu_buttons:
            pygame.draw.rect(self.screen, PURPLE, button["rect"])
            pygame.draw.rect(self.screen, BLACK, button["rect"], 2)
            
            text = self.text_font.render(button["text"], True, WHITE)
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)
    
    def draw_gameplay(self):
        self.screen.fill(WHITE)
        
        if self.current_date_index < len(self.characters):
            current_character = self.characters[self.current_date_index]
            
            # Draw character info
            self.screen.blit(current_character.image, (50, 50))
            
            name_text = self.heading_font.render(current_character.name, True, BLACK)
            self.screen.blit(name_text, (280, 50))
            
            traits_text = self.text_font.render("Traits: " + ", ".join(current_character.traits), True, BLACK)
            self.screen.blit(traits_text, (280, 100))
            
            interests_text = self.text_font.render("Interests: " + ", ".join(current_character.interests), True, BLACK)
            self.screen.blit(interests_text, (280, 140))
            
            # Draw timer
            timer_text = self.text_font.render(f"Time: {int(self.timer)} seconds", True, RED)
            self.screen.blit(timer_text, (SCREEN_WIDTH - 200, 20))
            
            # Draw progress
            progress_text = self.small_font.render(f"Date {self.current_date_index + 1} of {len(self.characters)}", True, BLACK)
            self.screen.blit(progress_text, (20, 20))
            
            # Draw question or next date button
            if self.current_question_index < len(self.questions):
                question_text = self.text_font.render(self.questions[self.current_question_index], True, BLUE)
                self.screen.blit(question_text, (50, 250))
                
                # Draw response options
                options = self.response_options[self.current_question_index]
                for i, option in enumerate(options):
                    rect = pygame.Rect(150, 300 + (i * 50), 500, 40)
                    hover = rect.collidepoint(pygame.mouse.get_pos())
                    
                    pygame.draw.rect(self.screen, GRAY if hover else WHITE, rect)
                    pygame.draw.rect(self.screen, BLACK, rect, 2)
                    
                    option_text = self.text_font.render(option, True, BLACK)
                    self.screen.blit(option_text, (rect.x + 10, rect.y + 5))
            else:
                # All questions answered, show next date button
                complete_text = self.text_font.render("Date complete! Ready to meet the next person?", True, GREEN)
                self.screen.blit(complete_text, (50, 250))
                
                pygame.draw.rect(self.screen, GREEN, self.next_date_button["rect"])
                pygame.draw.rect(self.screen, BLACK, self.next_date_button["rect"], 2)
                
                text = self.text_font.render(self.next_date_button["text"], True, WHITE)
                text_rect = text.get_rect(center=self.next_date_button["rect"].center)
                self.screen.blit(text, text_rect)
        
        # Draw back button
        pygame.draw.rect(self.screen, RED, self.back_button["rect"])
        pygame.draw.rect(self.screen, BLACK, self.back_button["rect"], 2)
        
        text = self.text_font.render(self.back_button["text"], True, WHITE)
        text_rect = text.get_rect(center=self.back_button["rect"].center)
        self.screen.blit(text, text_rect)
    
    def draw_results(self):
        self.screen.fill(PINK)
        
        # Draw title
        title = self.heading_font.render("Your Dating Results", True, PURPLE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))
        
        # Draw matches in order of compatibility
        for i, character in enumerate(self.characters):
            y_pos = 100 + (i * 90)
            
            # Draw box
            pygame.draw.rect(self.screen, WHITE, (50, y_pos, SCREEN_WIDTH - 100, 80))
            pygame.draw.rect(self.screen, BLACK, (50, y_pos, SCREEN_WIDTH - 100, 80), 2)
            
            # Draw rank
            rank_text = self.heading_font.render(f"#{i+1}", True, BLACK)
            self.screen.blit(rank_text, (70, y_pos + 20))
            
            # Draw mini-image
            mini_img = pygame.transform.scale(character.image, (60, 60))
            self.screen.blit(mini_img, (120, y_pos + 10))
            
            # Draw name
            name_text = self.heading_font.render(character.name, True, BLACK)
            self.screen.blit(name_text, (200, y_pos + 10))
            
            # Draw compatibility
            compat_text = self.text_font.render(f"Compatibility: {character.compatibility}%", True, 
                                             GREEN if character.compatibility >= 60 else 
                                             BLUE if character.compatibility >= 40 else RED)
            self.screen.blit(compat_text, (200, y_pos + 45))
        
        # Best match message
        if len(self.characters) > 0:
            best_match = self.characters[0]
            if best_match.compatibility >= 80:
                message = f"You and {best_match.name} are a perfect match!"
            elif best_match.compatibility >= 60:
                message = f"You and {best_match.name} have great chemistry!"
            elif best_match.compatibility >= 40:
                message = f"You and {best_match.name} might make good friends."
            else:
                message = "No strong connections this time. Try again!"
                
            msg_text = self.text_font.render(message, True, PURPLE)
            self.screen.blit(msg_text, (SCREEN_WIDTH//2 - msg_text.get_width()//2, 550))
        
        # Draw back button
        pygame.draw.rect(self.screen, RED, self.back_button["rect"])
        pygame.draw.rect(self.screen, BLACK, self.back_button["rect"], 2)
        
        text = self.text_font.render(self.back_button["text"], True, WHITE)
        text_rect = text.get_rect(center=self.back_button["rect"].center)
        self.screen.blit(text, text_rect)
    
    def draw(self):
        if self.state == MENU:
            self.draw_menu()
        elif self.state == GAMEPLAY:
            self.draw_gameplay()
        elif self.state == RESULTS:
            self.draw_results()
            
        pygame.display.flip()
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

# Main function
def main():
    try:
        game = SpeedDatingGame()
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        pygame.quit()
        sys.exit(1)

def start_date():
    main()  # Runs the driving scene
    import src.main_menu  # Import main menu module
    src.main_menu.main_menu()  # Call the main menu again

if __name__ == "__main__":
    start_date()