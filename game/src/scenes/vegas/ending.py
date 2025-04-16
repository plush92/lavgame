import pygame
import time
from src.scenes.vegas.paper import Paper
from src.scene_wait_for_continue import scene_wait_for_continue
from src.scenes.driving.driving import start_driving

class EndingSequence:
    def __init__(self, screen, width, height, tim, lav):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        self.font_large = pygame.font.Font(None, 60)
        self.font_medium = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 30)
        self.GOLD = (255, 215, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.PURPLE = (128, 0, 128)
        self.papers = [Paper() for _ in range(50)]  # Create 50 papers
        self.heart_timer = 0
        self.heart_stage = 0  # 0: red heart, 1: blue heart, 2: purple heart
        self.text_stage = 0  # Track which text is being displayed
        self.text_timer = 0
        self.tim = tim
        self.lav = lav

        # Load heart images
        self.red_heart = pygame.image.load("src/assets/redheart.png").convert_alpha()
        self.blue_heart = pygame.image.load("src/assets/blueheart.png").convert_alpha()
        self.purple_heart = pygame.image.load("src/assets/purpleheart.png").convert_alpha()

        # Scale heart images
        self.red_heart = pygame.transform.scale(self.red_heart, (60, 60))
        self.blue_heart = pygame.transform.scale(self.blue_heart, (60, 60))
        self.purple_heart = pygame.transform.scale(self.purple_heart, (100, 100))

    def draw_text(self, text, font, color, x, y, center=True, scale=1.0):
        """Draw text with a popping effect."""
        font_size = int(font.get_height() * scale)  # Use get_height() to get the font size
        temp_font = pygame.font.Font(None, font_size)
        surface = temp_font.render(text, True, color)
        rect = surface.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surface, rect)

    def update_papers(self):
        """Update and draw papers flying out."""
        for paper in self.papers[:]:
            if paper.update():
                self.papers.remove(paper)
            else:
                paper.draw()

    def draw_heart(self, dt):
        """Draw the heart animation."""
        self.heart_timer += dt
        if self.heart_stage == 0:  # Red heart from Tim
            self.screen.blit(self.red_heart, (self.WIDTH // 2 - 80, self.HEIGHT // 2 - 30))
            if self.heart_timer > 1.5:
                self.heart_stage = 1
                self.heart_timer = 0
        elif self.heart_stage == 1:  # Blue heart from Lav
            self.screen.blit(self.blue_heart, (self.WIDTH // 2 + 20, self.HEIGHT // 2 - 30))
            if self.heart_timer > 1.5:
                self.heart_stage = 2
                self.heart_timer = 0
        elif self.heart_stage == 2:  # Purple heart merging
            self.screen.blit(self.purple_heart, (self.WIDTH // 2 - 50, self.HEIGHT // 2 - 50))

    def draw_characters(self, dt):
        """Keep characters visible during the ending."""
        # Move Lav slightly to the right to avoid overlap with the purple heart
        lav_offset_x = 50  # Adjust this value as needed
        lav_rect = self.lav.rect.copy()
        lav_rect.x += lav_offset_x

        self.tim.draw(self.screen, dt)  # Draw Tim in his original position
        self.screen.blit(self.lav.image, lav_rect)  # Draw Lav with the adjusted position

    def draw_text_sequence(self, dt):
        """Display text sequentially with a popping effect."""
        texts = [
            ("CONGRATULATIONS!", self.font_large, self.GOLD, 100),
            ("You've earned... her love <3", self.font_medium, self.WHITE, 150),
            ("Hope you like CVS runs at midnight!", self.font_small, self.WHITE, 200),
        ]
        if self.text_stage < len(texts):
            self.text_timer += dt
            if self.text_timer > 2:  # Delay between text lines
                self.text_stage += 1
                self.text_timer = 0
        for i in range(self.text_stage):
            text, font, color, y = texts[i]
            self.draw_text(text, font, color, self.WIDTH // 2, y, center=True, scale=1.2 if i == self.text_stage - 1 else 1.0)

    def play(self, dt):
        """Handles the ending sequence with flying papers, heart animation, and text."""
        self.screen.fill((0, 0, 0))  # Black background
        self.update_papers()
        self.draw_characters(dt)
        self.draw_heart(dt)
        self.draw_text_sequence(dt)

        # Check if the ending sequence is complete
        if self.heart_stage == 2 and self.text_stage >= 3:  # All hearts and text displayed
            # Add a delay to ensure the final line is visible
            if not hasattr(self, "final_text_timer"):
                self.final_text_timer = 0  # Initialize the timer
            self.final_text_timer += dt

            if self.final_text_timer > 2:  # Wait 2 seconds before prompting
                result = scene_wait_for_continue(self.screen)  # Prompt the user to continue
                if result == "continue":
                    start_driving()  # Transition to the next scene
