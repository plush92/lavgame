import pygame
import random
import os

# Constants
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
ROAD_WIDTH = int(WIDTH * 0.7)
MARGIN = (WIDTH - ROAD_WIDTH) // 2
LANE_WIDTH = ROAD_WIDTH // 4
OBSTACLE_SPEED = 2.5
SPAWN_RATE = 40

class PreGameScene:
    """Displays a convertible moving across the screen."""
    def __init__(self):
        assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))
        
        # Load and scale convertible
        self.convertible = pygame.image.load(os.path.join(assets_dir, "convertibleright.png"))
        self.convertible = pygame.transform.scale(self.convertible, (200, 100))
        self.convertible_rect = self.convertible.get_rect(midleft=(-200, int(HEIGHT * 0.77)))  # Move car lower on the screen
        
        self.car_speed = 5  # Speed of the convertible
        self.show_scene = True  # Flag to keep scene running
    
    def update(self):
        """Moves the convertible across the screen."""
        if self.convertible_rect.left < WIDTH:  # Move until it's fully off-screen right
            self.convertible_rect.x += self.car_speed
        else:
            self.show_scene = False  # Exit the scene when the car moves off-screen
    
    def draw(self, screen):
        """Draws the convertible."""
        # Removed the screen.fill call to avoid overriding the background
        screen.blit(self.convertible, self.convertible_rect)  # Draw the convertible

    def title_sequence(self):
        """Displays a fade-in and fade-out title sequence."""
        font = pygame.font.Font(None, 72)
        text_surface = font.render("On the road...", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        alpha = 0  # Start fully transparent
        fade_in = True  # Start with fade-in
        clock = pygame.time.Clock()
        
        while alpha >= 0:
            screen.fill((0, 0, 0))  # Black background
            text_surface.set_alpha(alpha)  # Set transparency
            screen.blit(text_surface, text_rect)  # Draw the text
            pygame.display.flip()
            
            if fade_in:
                alpha += 10  # Increase alpha faster for fade-in
                if alpha >= 255:  # Fully visible
                    fade_in = False  # Start fade-out
                    pygame.time.delay(1000)  # Pause for 1 second
            else:
                alpha -= 10  # Decrease alpha faster for fade-out
            
            clock.tick(30)  # Control frame rate

    def load_highway_background(self):
        """Loads and scales the highway background image."""
        assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))
        highway_path = os.path.join(assets_dir, "highway.jpeg")
        
        try:
            highway_background = pygame.image.load(highway_path)
            highway_background = pygame.transform.scale(highway_background, (WIDTH, HEIGHT))  # Scale to fit screen
            return highway_background
        except pygame.error as e:
            print(f"Error loading highway background: {e}")
            pygame.quit()
            exit()
    
    def load_highway_background_front(self):
        """Loads and scales the highway background image."""
        assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))
        highway_path = os.path.join(assets_dir, "highwaybackgroundfront.png")
        
        try:
            highway_background = pygame.image.load(highway_path)
            highway_background = pygame.transform.scale(highway_background, (WIDTH, HEIGHT))  # Scale to fit screen
            return highway_background
        except pygame.error as e:
            print(f"Error loading highway background: {e}")
            pygame.quit()
            exit()

    def move_convertible(self):
        """Handles the animation of the convertible moving across the screen."""
        highway_background = self.load_highway_background()  # Load the highway background
        
        clock = pygame.time.Clock()
        
        while self.show_scene:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            self.update()
            
            # Draw the background and the convertible
            screen.blit(highway_background, (0, 0))  # Draw the highway background
            self.draw(screen)
            
            pygame.display.flip()
            clock.tick(60)
        
        print("Convertible animation complete.")

    def show_convertible_front(self):
        """Displays a screen with the convertible front image and a speech bubble for the text."""
        assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))
        convertible_front = pygame.image.load(os.path.join(assets_dir, "convertiblefront.png"))
        convertible_front = pygame.transform.scale(convertible_front, (250, 150))  # Scale the image
        convertible_front_rect = convertible_front.get_rect(center=(WIDTH // 2 - 120, HEIGHT // 2 + 140))
        highway_background_front = self.load_highway_background_front()  # Load the highway background
        
        clock = pygame.time.Clock()
        show_front = True
        
        # Typing effect setup
        font = pygame.font.Font(None, 28)  # Smaller font size
        message = "Honey, please don't get distracted with gambling and fast food!!"
        displayed_text = ""
        typing_index = 0
        typing_speed = 1  # Number of characters per frame (changed to an integer for simplicity)
        
        # Speech bubble dimensions
        bubble_width = 250
        bubble_height = 90
        bubble_rect = pygame.Rect(
            (WIDTH // 2 - bubble_width // 2, HEIGHT // 4 - bubble_height // 2),
            (bubble_width, bubble_height)
        )
        bubble_pointer = [(WIDTH // 2, HEIGHT // 4 + bubble_height // 2),  # Bottom center of bubble
                          (WIDTH // 2 - 20, HEIGHT // 4 + bubble_height // 2 + 30),  # Left point of pointer
                          (WIDTH // 2 + 20, HEIGHT // 4 + bubble_height // 2 + 30)]  # Right point of pointer
        
        def render_wrapped_text(surface, text, font, color, rect):
            """Renders text that wraps within a given rectangle."""
            words = text.split(' ')
            lines = []
            current_line = ""
            
            for word in words:
                test_line = f"{current_line} {word}".strip()
                if font.size(test_line)[0] <= rect.width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            
            y_offset = rect.top
            for line in lines:
                line_surface = font.render(line, True, color)
                surface.blit(line_surface, (rect.left, y_offset))
                y_offset += font.get_linesize()
        
        while show_front:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    show_front = False  # Exit the screen when SPACE is pressed
            
            # Update the displayed text for the typing effect
            if typing_index < len(message):
                typing_index += typing_speed
                displayed_text = message[:int(typing_index)]  # Ensure slicing uses an integer
            
            # Draw the screen
            screen.blit(highway_background_front, (0, 0))  # Draw the highway background
            screen.blit(convertible_front, convertible_front_rect)  # Draw the image
            
            # Draw the speech bubble
            pygame.draw.rect(screen, (255, 255, 255), bubble_rect, border_radius=10)  # Bubble rectangle
            pygame.draw.polygon(screen, (255, 255, 255), bubble_pointer)  # Bubble pointer
            
            # Render and draw the wrapped text inside the bubble
            render_wrapped_text(screen, displayed_text, font, (0, 0, 0), bubble_rect.inflate(-20, -20))
            
            pygame.display.flip()
            clock.tick(60)
        
        print("Convertible front screen complete.")

    def handle_events(self, events):
        """Handles events and runs the pre-game animation."""
        self.title_sequence()  # Play the title sequence before the animation
        self.move_convertible()  # Run the convertible animation
        self.show_convertible_front()  # Show the convertible front screen

# Start the animation
if __name__ == "__main__":
    pygame.init()
    pre_game = PreGameScene()
    pre_game.handle_events()
