import pygame
import sys
import os

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
LIGHT_GRAY = (230, 230, 230)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
PINK = (255, 105, 180)
APP_BG = (145, 70, 255)
APP_HEADER = (255, 79, 91)
LIGHT_BLUE = (100, 149, 237)
BROWN = (139, 69, 19)
PLAYER_BLUE = (30, 144, 255)
WALL_COLOR = (245, 222, 179)
DESK_COLOR = (160, 82, 45)
CHAIR_COLOR = (101, 67, 33)
FLOOR_COLOR = (210, 180, 140)

# Game states
INTRO = 0
SWIPING = 1
CONFIRMATION = 2
SELECTED = 3

class Profile:
    def __init__(self, name, age, description, traits, image_path):
        self.name = name
        self.age = age
        self.description = description
        self.traits = traits
        self.image_path = image_path
        self.load_image()
        
    def load_image(self):
        try:
            # Try to load the image
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, (500, 350))
        except:
            # Create a placeholder image if loading fails
            self.image = pygame.Surface((500, 350))
            self.image.fill(GRAY)
            font = pygame.font.SysFont("Arial", 32)
            text = font.render(f"{self.name}, {self.age}", True, BLACK)
            text_rect = text.get_rect(center=(250, 175))
            self.image.blit(text, text_rect)

class DatingApp:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Find Your Match")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.heading_font = pygame.font.SysFont("Arial", 32, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 20)
        self.small_font = pygame.font.SysFont("Arial", 16)
        
        # Game state
        self.state = INTRO
        self.current_profile_index = 0
        self.confirmation_level = 0
        self.intro_timer = 5 * FPS  # 5 seconds intro
        self.zoom_effect = 0  # For transition from bedroom to computer screen
        
        # Load Twitch logo
        self.twitch_logo = self.load_twitch_logo()

        # Create profiles
        self.create_profiles()
        
        # Load buttons
        self.left_button = pygame.Rect(150, 500, 80, 50)
        self.right_button = pygame.Rect(570, 500, 80, 50)
        self.like_button = pygame.Rect(350, 500, 100, 50)
        
        # Confirmation buttons
        self.yes_button = pygame.Rect(250, 400, 100, 50)
        self.no_button = pygame.Rect(450, 400, 100, 50)
        
        # Final decision buttons
        self.decision_buttons = [
            pygame.Rect(350, 420, 100, 50),  # Fixed position for "I know" button
            pygame.Rect(350, 420, 100, 50),  # Fixed position for "I know" (2nd time)
            pygame.Rect(350, 420, 100, 50)   # Fixed position for "I'm a god"
        ]
        
        # Create warning messages
        self.warning_messages = [
            "Are you sure?",
            "Ok... seriously? This does not look like a good idea.",
            "Bud, as your friend this is kinda crazy....",
            "This behavior is self-destructive and has a 4% chance of ending well for you.",
            "Ok...."
        ]
        
    def create_profiles(self):
        # Set the directory for profile pictures relative to this script's location
        img_dir = os.path.join(os.path.dirname(__file__), "profile_pics")
        
        # Ensure the directory exists
        if not os.path.exists(img_dir):
            raise FileNotFoundError(f"The directory '{img_dir}' does not exist.")
        
        # Create profiles
        self.profiles = [
            Profile(
                "Blonde", 29,
                "Outgoing and fun! Looking for something casual.",
                [
                    "Is very pretty",
                    "Is nice",
                    "Willing to do your laundry",
                    "Has had sex with several big streamers",
                    "Is rapidly approaching 30 and not eager to be a mother",
                    "Wants something casual"
                ],
                os.path.join(img_dir, "blonde.png")
            ),
            Profile(
                "Brunette", 26,
                "Smart and cute! Love a good conversation over coffee.",
                [
                    "Wears 18 pounds of makeup",
                    "Is cute",
                    "Reasonably clever",
                    "Severely unstable",
                    "Has an eating disorder",
                    "1 year away from hyper-religious psychosis"
                ],
                os.path.join(img_dir, "brunette.png")
            ),
            Profile(
                "Split-Hair Dye", 24,
                "Live streamer. Half pink, half blue hair. I'm a wild one!",
                [
                    "Crazy eyes",
                    "Drinking and pill problem",
                    "Cries on stream every night",
                    "Has been beaten and is in current litigation with ex",
                    "Extremely high libido",
                    "4 months away from shaving her head"
                ],
                os.path.join(img_dir, "split.png")
            ),
            Profile(
                "Goth", 25,
                "Married. Content creator. If you can make me laugh, you've got my attention.",
                [
                    "Has a husband",
                    "Makes you laugh",
                    "Has an OnlyFans (where she posts tasteful nudity and not anything that crazy)",
                    "Makes you laugh",
                    "Beautiful green eyes",
                    "Extremely clever and intelligent",
                    "Very tight",
                    "Makes you laugh",
                    "Has cried online and has a terrible reputation",
                    "Makes you laugh",
                    "Reasonable to assume she will let you put it in her butt"
                ],
                os.path.join(img_dir, "goth.png")
            )
        ]
    
    def load_twitch_logo(self):
        """Load the Twitch logo."""
        try:
            logo_path = os.path.join(os.path.dirname(__file__), "twitchlogo.png")
            logo = pygame.image.load(logo_path).convert_alpha()
            logo = pygame.transform.scale(logo, (80, 80))  # Resize the logo
            return logo
        except pygame.error as e:
            print(f"Error loading Twitch logo: {e}")
            return None
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Handle state-specific clicks
                    if self.state == SWIPING:
                        # Left arrow (swipe left)
                        if self.left_button.collidepoint(mouse_pos):
                            self.current_profile_index = (self.current_profile_index + 1) % len(self.profiles)
                            
                        # Right arrow (swipe right)
                        elif self.right_button.collidepoint(mouse_pos):
                            self.current_profile_index = (self.current_profile_index + 1) % len(self.profiles)
                            
                        # Like button
                        elif self.like_button.collidepoint(mouse_pos):
                            # Only allow selecting the goth girl (last profile)
                            if self.current_profile_index == len(self.profiles) - 1:
                                self.state = CONFIRMATION
                                self.confirmation_level = 0
                    
                    elif self.state == CONFIRMATION:
                        # Yes button
                        if self.yes_button.collidepoint(mouse_pos):
                            self.confirmation_level += 1
                            
                            # If all confirmations passed
                            if self.confirmation_level >= len(self.warning_messages):
                                self.state = SELECTED
                                
                        # No button (only available on first confirmation)
                        elif self.no_button.collidepoint(mouse_pos) and self.confirmation_level == 0:
                            self.state = SWIPING
                            
                        # Additional confirmation button handling
                        elif self.confirmation_level > 0:
                            button = self.decision_buttons[min(self.confirmation_level - 1, len(self.decision_buttons) - 1)]
                            if button.collidepoint(mouse_pos):
                                self.confirmation_level += 1
                                if self.confirmation_level >= len(self.warning_messages):
                                    self.state = SELECTED
                    
                    elif self.state == SELECTED:
                        # Return to main menu or next scene could go here
                        pass
    
    def update(self):
        if self.state == INTRO:
            self.intro_timer -= 1
            # Start zoom effect when half of the intro time has passed
            if self.intro_timer <= (2.5 * FPS) and self.zoom_effect < 100:
                self.zoom_effect += 0.5
            if self.intro_timer <= 0:
                self.state = SWIPING
                self.zoom_effect = 0
    
    def draw_intro(self):
        # Draw bedroom background
        self.screen.fill(WALL_COLOR)
        
        # Draw floor
        pygame.draw.rect(self.screen, FLOOR_COLOR, (0, 400, SCREEN_WIDTH, 200))
        
        # Draw desk
        desk_rect = pygame.Rect(200, 300, 400, 50)
        pygame.draw.rect(self.screen, DESK_COLOR, desk_rect)
        
        # Draw desk legs
        pygame.draw.rect(self.screen, DESK_COLOR, (220, 350, 20, 50))
        pygame.draw.rect(self.screen, DESK_COLOR, (560, 350, 20, 50))
        
        # Draw chair
        chair_rect = pygame.Rect(350, 350, 100, 30)
        pygame.draw.rect(self.screen, CHAIR_COLOR, chair_rect)
        pygame.draw.rect(self.screen, CHAIR_COLOR, (380, 380, 40, 50))
        
        # Draw computer monitor
        monitor_rect = pygame.Rect(300, 200, 200, 100)
        pygame.draw.rect(self.screen, BLACK, monitor_rect)
        
        # Draw computer screen (blue) with white border
        screen_rect = pygame.Rect(310, 210, 180, 80)
        pygame.draw.rect(self.screen, LIGHT_BLUE, screen_rect)
        
        # Draw player (blue box) sitting at desk
        player_rect = pygame.Rect(375, 300, 50, 80)
        pygame.draw.rect(self.screen, PLAYER_BLUE, player_rect)
        
        # Draw title text on screen or above the scene
        title = self.heading_font.render("Finding love online...", True, BLACK)
        subtitle = self.text_font.render("what could go wrong?", True, BLACK)
        
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        self.screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 140))
        
        # Draw transition effect if zoom is active
        if self.zoom_effect > 0:
            # Create a zoom effect towards the computer screen
            zoom_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            # Make background darker as we zoom
            zoom_surface.fill((0, 0, 0, int(self.zoom_effect * 1.5)))
            self.screen.blit(zoom_surface, (0, 0))
            
            # Calculate zoom rectangle (gets smaller as we zoom in)
            zoom_size = max(1, int(180 - (self.zoom_effect * 1.8)))
            zoom_rect = pygame.Rect(
                400 - zoom_size//2,
                250 - zoom_size//2,
                zoom_size,
                zoom_size * 0.8
            )
            
            # Draw zoom outline
            pygame.draw.rect(self.screen, WHITE, zoom_rect, 3)
            
            # Draw "zooming in" text
            if self.zoom_effect > 50:
                zoom_text = self.text_font.render("Loading dating app...", True, WHITE)
                self.screen.blit(zoom_text, (SCREEN_WIDTH//2 - zoom_text.get_width()//2, 500))
    
    def draw_app_frame(self):
        # Draw app background
        self.screen.fill(APP_BG)
        
        # Draw Twitch logo
        if self.twitch_logo:
            self.screen.blit(self.twitch_logo, (10, 10))  # Top-left corner
        
        # Draw app name
        app_name = self.heading_font.render("BROWSE", True, WHITE)
        self.screen.blit(app_name, (SCREEN_WIDTH // 2 - app_name.get_width() // 2, 15))
    
    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "

        lines.append(current_line)  # Add last line
        return lines
    
    def draw_profile_card(self, profile):
        # Improved card dimensions and positioning
        card_x = 150
        card_y = 80
        card_width = 450
        card_height = 470  # Increased card height to make more room for content
        padding = 20  # For consistent spacing inside the card

        # Draw white card background
        card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
        pygame.draw.rect(self.screen, WHITE, card_rect, border_radius=10)
        pygame.draw.rect(self.screen, GRAY, card_rect, 2, border_radius=10)

        # Draw profile image (scaled down to fit better)
        image_width = 400
        image_height = 280  # Reduce image height to make more room for text
        scaled_image = pygame.transform.scale(profile.image, (image_width, image_height))
        image_x = card_x + (card_width - image_width) // 2
        image_y = card_y + padding
        self.screen.blit(scaled_image, (image_x, image_y))

        # Draw profile info
        name_age_text = f"{profile.name}, {profile.age}"
        name_age_surface = pygame.font.Font(None, 30).render(name_age_text, True, BLACK)
        name_age_x = card_x + padding
        name_age_y = image_y + image_height + 10
        self.screen.blit(name_age_surface, (name_age_x, name_age_y))

        # Use smaller font for description to fit more text
        description_font = pygame.font.SysFont("Arial", 18)  # Smaller font for description
        
        # Wrap description text - allow more lines
        description_x = card_x + padding
        description_y = name_age_y + 30  # Below name/age
        wrapped_description = self.wrap_text(profile.description, description_font, card_width - 2 * padding)
        
        # Show more lines of description
        for i, line in enumerate(wrapped_description[:3]):  # Show up to 3 lines
            text_surface = description_font.render(line, True, BLACK)
            self.screen.blit(text_surface, (description_x, description_y + i * 22))  # Reduced line spacing

        # Position buttons lower and at the bottom of the card
        button_y = card_y + card_height - 60  # Position 60 pixels from bottom of card
        
        # Adjust buttons
        self.left_button = pygame.Rect(0, 0, 50, 50)
        self.left_button.center = (card_x + 75, button_y)
        
        self.right_button = pygame.Rect(0, 0, 50, 50)
        self.right_button.center = (card_x + card_width - 75, button_y)
        
        self.like_button = pygame.Rect(0, 0, 100, 40)
        self.like_button.center = (card_x + card_width // 2, button_y)

        # Draw buttons
        pygame.draw.circle(self.screen, RED, self.left_button.center, 25)
        pygame.draw.circle(self.screen, GREEN, self.right_button.center, 25)
        pygame.draw.rect(self.screen, PINK, self.like_button, border_radius=10)

        # Draw button text
        left_text = self.heading_font.render("✕", True, WHITE)
        right_text = self.heading_font.render("→", True, WHITE)
        like_text = self.text_font.render("SELECT", True, WHITE)

        self.screen.blit(left_text, (self.left_button.centerx - left_text.get_width()//2, 
                                    self.left_button.centery - left_text.get_height()//2))
        self.screen.blit(right_text, (self.right_button.centerx - right_text.get_width()//2, 
                                    self.right_button.centery - right_text.get_height()//2))
        self.screen.blit(like_text, (self.like_button.centerx - like_text.get_width()//2, 
                                    self.like_button.centery - like_text.get_height()//2))

    def draw_traits(self, profile):
        # Draw traits panel on the right side
        trait_panel_width = 180
        trait_panel_height = 470  # Increased to match card height
        trait_panel_x = 620
        trait_panel_y = 80
        
        trait_surface = pygame.Surface((trait_panel_width, trait_panel_height))
        trait_surface.fill(LIGHT_GRAY)
        
        title_text = self.small_font.render("About:", True, BLACK)
        trait_surface.blit(title_text, (10, 10))
        
        # Use smaller font for traits to fit more
        trait_font = pygame.font.SysFont("Arial", 14)  # Smaller font for traits
        
        y_offset = 40
        for trait in profile.traits:
            # Wrap long traits
            wrapped_lines = self.wrap_text(trait, trait_font, trait_panel_width - 20)
            
            for i, enumerate_lines in enumerate(wrapped_lines):
                if i == 0:
                    text = trait_font.render(f"• {enumerate_lines.strip()}", True, BLACK)
                else:
                    text = trait_font.render(f"  {enumerate_lines.strip()}", True, BLACK)
                
                trait_surface.blit(text, (10, y_offset))
                y_offset += 18  # Reduced line spacing
                
                # Check if we're running out of space
                if y_offset > trait_panel_height - 20:
                    remaining_text = trait_font.render("...", True, BLACK)
                    trait_surface.blit(remaining_text, (10, y_offset))
                    break
            
            # Add spacing between traits
            y_offset += 4  # Reduced spacing between traits
            
            # Check if we're running out of space
            if y_offset > trait_panel_height - 20:
                break
        
        # Show traits panel
        self.screen.blit(trait_surface, (trait_panel_x, trait_panel_y))
    
    def draw_confirmation(self):
        # Darken background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Draw confirmation dialog
        dialog_rect = pygame.Rect(200, 200, 400, 300)  # Made taller
        pygame.draw.rect(self.screen, WHITE, dialog_rect, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, dialog_rect, 2, border_radius=10)
        
        # Draw warning message (with wrapping for long messages)
        warning_message = self.warning_messages[min(self.confirmation_level, len(self.warning_messages) - 1)]
        wrapped_warning = self.wrap_text(warning_message, self.heading_font, 380)
        
        warning_y = 230
        for line in wrapped_warning:
            warning_text = self.heading_font.render(line, True, BLACK)
            warning_rect = warning_text.get_rect(center=(SCREEN_WIDTH // 2, warning_y))
            self.screen.blit(warning_text, warning_rect)
            warning_y += 40
        
        # Draw buttons
        if self.confirmation_level == 0:
            # First confirmation has Yes/No buttons
            pygame.draw.rect(self.screen, GREEN, self.yes_button, border_radius=5)
            pygame.draw.rect(self.screen, RED, self.no_button, border_radius=5)
            
            yes_text = self.text_font.render("Yes", True, WHITE)
            no_text = self.text_font.render("No", True, WHITE)
            
            self.screen.blit(yes_text, (self.yes_button.centerx - yes_text.get_width()//2, 
                                      self.yes_button.centery - yes_text.get_height()//2))
            self.screen.blit(no_text, (self.no_button.centerx - no_text.get_width()//2, 
                                     self.no_button.centery - no_text.get_height()//2))
        else:
            # Subsequent confirmations have only one button
            button_index = min(self.confirmation_level - 1, len(self.decision_buttons) - 1)
            button = self.decision_buttons[button_index]
            pygame.draw.rect(self.screen, BLUE, button, border_radius=5)
            
            button_texts = ["I know", "I know", "I'm a god"]
            text_index = min(self.confirmation_level - 1, len(button_texts) - 1)
            text = self.text_font.render(button_texts[text_index], True, WHITE)
            
            self.screen.blit(text, (button.centerx - text.get_width()//2, 
                                   button.centery - text.get_height()//2))
    
    def draw_selected(self): # Draw the final selected profile screen
        # Draw celebratory screen
        self.screen.fill(PINK)
        
        # Draw match text
        match_text = self.title_font.render("It's a Match!", True, RED)
        self.screen.blit(match_text, (SCREEN_WIDTH//2 - match_text.get_width()//2, 100))
        
        # Draw selected profile
        selected_profile = self.profiles[len(self.profiles) - 1]  # Goth girl
        
        # Draw profile image (centered and larger)
        scaled_image = pygame.transform.scale(selected_profile.image, (300, 210))
        self.screen.blit(scaled_image, (SCREEN_WIDTH//2 - scaled_image.get_width()//2, 200))
        
        # Draw profile name
        name_text = self.heading_font.render(selected_profile.name, True, BLACK)  # Changed from GRAY to BLACK
        self.screen.blit(name_text, (SCREEN_WIDTH//2 - name_text.get_width()//2, 430))
        
        # Draw continue message
        continue_text = self.text_font.render("Press any key to continue your journey...", True, BLACK)
        self.screen.blit(continue_text, (SCREEN_WIDTH//2 - continue_text.get_width()//2, 500))
    
    def draw(self):
        if self.state == INTRO:
            self.draw_intro()
        elif self.state == SWIPING:
            self.draw_app_frame()
            self.draw_profile_card(self.profiles[self.current_profile_index])
            self.draw_traits(self.profiles[self.current_profile_index])
        elif self.state == CONFIRMATION:
            self.draw_app_frame()
            self.draw_profile_card(self.profiles[self.current_profile_index])
            self.draw_traits(self.profiles[self.current_profile_index])
            self.draw_confirmation()
        elif self.state == SELECTED:
            self.draw_selected()
            
        pygame.display.flip()
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

# Main function
def start_date():
    try:
        app = DatingApp()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    start_date()