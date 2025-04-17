import pygame
import os
import math
from src.scenes.meadow.constants import WIDTH, HEIGHT

letter_text = """Timmy, this is the first birthday I have the privilege of spending with you. 
From the moment I met you, something in me starved, howled. 
A hunger I did not know my body could feel. Raw, desperate, insatiable. 
You are fire and velocity, bold and brazen, reckless and magnificent. 
But you are warmth, too. A hearth in the dead of winter. 
You are kindness. A gooey center, a young emotional loving child. 
You are loyalty carved from bone, unwavering, unshaken. 
There is nothing false in you; your very breath thrums with life, more vivid, 
more searing than anyone I have ever known. 

And you, with your ridiculous jokes and your laughter that crashes against my ribs like waves. 
I have never laughed like this before. 
Your passion burns, it devours, it lifts me into a world I never dared to believe in. 
Every moment with you is a chapter I never want to end, a storybook where the pages turn too fast.
This is the first time I have watched you step deeper into time, 
the first year I have witnessed you grow older. 
And I want more. Selfishly, endlessly. 
I want to watch the years carve their poetry into your skin, 
to trace each line, 
to hold time by its throat and beg it to slow, 
to stretch each second until I have wrung every last drop of you.
I love you. More today than yesterday, more tomorrow than today.
Happy birthday, my love."""
font_size = 11

def create_blur(surface, amount):
    scale = 1.0 / float(amount)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf

class Letter:
    def __init__(self, text=letter_text):
        self.pages = []  # List to store pages of text
        self.current_page = 0  # Track the current page
        self.font = pygame.font.SysFont("georgia", 18)  # Font for the letter
        self.color = (75, 44, 29)  # Text color
        self.letter_width = int(WIDTH * 0.75)
        self.line_height = 25  # Height of each line
        self.lines_per_page = (HEIGHT - 200) // self.line_height  # Number of lines per page

        self.scroll_y = 0
        self.scroll_speed = 20
        self.max_scroll = 0
        self.letter_width = int(WIDTH * .75)
        self.text = text.split("\n")
        self.split_into_pages(text)
        # Use assets path to locate custom fonts
        # assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")
        #Calculate the total height of the letter
        # total_text_height = len(self.text) * 15 + 100  # 15px per line + 100px for top margin
        # self.max_scroll = total_text_height - HEIGHT + 100  # 100px for top margin
        # # Try to load handwritten font - fall back to system fonts if unavailable
        # try:
        #     self.font = pygame.font.Font(os.path.join(assets_dir, "fonts", "Pacifico-Regular.ttf"), 22)
        #     self.signature_font = pygame.font.Font(os.path.join(assets_dir, "fonts", "Pacifico-Regular.ttf"), 28)
        #     self.date_font = pygame.font.Font(os.path.join(assets_dir, "fonts", "Pacifico-Regular.ttf"), 18)
        # except:
        #     # Fallback fonts
        #     self.font = pygame.font.SysFont("georgia", 14)
        #     self.signature_font = pygame.font.SysFont("georgia", 14, italic=True)
        #     self.date_font = pygame.font.SysFont("georgia", 10, italic=True)
        
        # # Rich dark brown for text - handwritten ink look
        # self.color = (75, 44, 29)
        # self.signature_color = (139, 69, 19)  # Darker brown for signature
        # self.date_color = (102, 51, 0)  # Brown for date
        
        # # Try to load parchment background - fall back to cream color if unavailable
        # try:
        #     self.background = pygame.image.load(os.path.join(assets_dir, "parchment.png")).convert_alpha()
        #     self.background = pygame.transform.scale(self.background, (self.letter_width, HEIGHT))
        # except:
        #     self.background = None
        #     self.background_color = (255, 252, 232)  # Cream color for parchment
        
        # self.fade_in_index = 0
        # self.fade_in_timer = 0
        # self.alpha = 0  # For initial fade-in of whole letter
        # self.letter_surface = pygame.Surface((self.letter_width, HEIGHT), pygame.SRCALPHA)
        
        # # Current date for the letter
        # self.date = "April 16, 2025"
        
        # # Slight angle for letter (in degrees)
        # self.angle = 0.2
        
        # # Initialize shadow overlay
        # self.shadow = pygame.Surface((self.letter_width, HEIGHT), pygame.SRCALPHA)
        # pygame.draw.rect(self.shadow, (0, 0, 0, 30), pygame.Rect(8, 8, self.letter_width - 16, HEIGHT - 16))
        # self.shadow = create_blur(self.shadow, 5)
    
        # # Wrap the text to fit the width
        # self.max_line_width = (self.letter_width) - 20  # Margin of 50px on each side
        # self.wrapped_text = []
        
        # for paragraph in text.split("\n"):
        #     words = paragraph.split()
        #     current_line = []
        #     current_width = 0
            
        #     for word in words:
        #         test_line = " ".join(current_line + [word])
        #         test_width = self.font.size(test_line)[0]
                
        #         if test_width <= self.max_line_width:
        #             current_line.append(word)
        #             current_width = test_width
        #         else:
        #             if current_line:  # Only add if there's content
        #                 self.wrapped_text.append(" ".join(current_line))
        #             current_line = [word]
        #             current_width = self.font.size(word)[0]
            
        #     if current_line:  # Add the last line of the paragraph
        #         self.wrapped_text.append(" ".join(current_line))
            
        #     # Add a blank line between paragraphs (if not the last paragraph)
        #     if paragraph != text.split("\n")[-1]:
        #         self.wrapped_text.append("")
        
        # # Use wrapped_text instead of the original text
        # self.text = self.wrapped_text
    
    def split_into_pages(self, text):
        """Split the letter text into pages."""
        lines = text.split("\n")
        current_page = []

        for line in lines:
            if len(current_page) < self.lines_per_page:
                current_page.append(line)
            else:
                self.pages.append(current_page)
                current_page = [line]

        # Add the last page
        if current_page:
            self.pages.append(current_page)

    def handle_scroll(self, event):
        """Handle scrolling with arrow keys or mouse wheel."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.scroll_y = min(self.scroll_y + self.scroll_speed, self.max_scroll)
            elif event.key == pygame.K_UP:
                self.scroll_y = max(self.scroll_y - self.scroll_speed, 0)
        elif event.type == pygame.MOUSEWHEEL:
            self.scroll_y = max(0, min(self.scroll_y - event.y * self.scroll_speed, self.max_scroll))

    # def draw(self, screen):
    #     # Clear the letter surface
    #     self.letter_surface.fill((0, 0, 0, 0))
        
    #     # Draw the background
    #     if self.background:
    #         self.letter_surface.blit(self.background, (0, 0))
    #     else:
    #         pygame.draw.rect(self.letter_surface, self.background_color, pygame.Rect(0, 0, self.letter_width, HEIGHT))

    #     # Add a decorative border
    #     border_width = 2
    #     inner_margin = 20
    #     pygame.draw.rect(self.letter_surface, self.color, 
    #                      pygame.Rect(inner_margin, inner_margin, 
    #                                 self.letter_width - 2 * inner_margin, 
    #                                 HEIGHT - 2 * inner_margin), 
    #                      border_width)
        
    #     # Add fancy corners
    #     corner_size = 15
    #     for x, y in [(inner_margin, inner_margin), 
    #                   (self.letter_width - inner_margin - corner_size, inner_margin),
    #                   (inner_margin, HEIGHT - inner_margin - corner_size),
    #                   (self.letter_width - inner_margin - corner_size, HEIGHT - inner_margin - corner_size)]:
    #         pygame.draw.line(self.letter_surface, self.color, (x, y), (x + corner_size, y), border_width)
    #         pygame.draw.line(self.letter_surface, self.color, (x, y), (x, y + corner_size), border_width)
        
    #     # Add date at the top right
    #     date_text = self.date_font.render(self.date, True, self.date_color)
    #     self.letter_surface.blit(date_text, (self.letter_width - date_text.get_width() - 40, 40)) # 40px margin from top
        
    #     # Render the letter text line by line with a fade-in effect
    #     y_offset = 100 - self.scroll_y # Starting position for text
        
    #     # Calculate how many lines are showing currently
    #     visible_lines = min(len(self.text), self.fade_in_index + 1) # min of total lines and fade-in index, 
    #     # +1 to include the current line

    #     for i, line in enumerate(self.text): # enumerate to get line index
    #         if i < visible_lines: # only render lines that are visible
    #             # Skip empty lines but maintain spacing
    #             if not line: # empty line
    #                 y_offset += 10 # spacing
    #                 continue # skip to next line
                    
    #             # Check if this is the signature (last two lines)
    #             if i >= len(self.text) - 2: # last two lines
    #                 font_to_use = self.signature_font # signature font
    #                 color_to_use = self.signature_color # signature color
    #                 # Indent signature slightly
    #                 x_position = 60 if i == len(self.text) - 1 else 40 # last line
    #             else:
    #                 font_to_use = self.font
    #                 color_to_use = self.color
    #                 x_position = 40
                
    #             # Reduced variance for more consistent look
    #             line_angle = self.angle + (math.sin(i * 0.01) * 0.01)  # Less variation
                
    #             # Reduce the wobble amount
    #             wobble = math.sin(i * 0.1) * 2  # Less wobble
                
    #             rendered_text = font_to_use.render(line, True, color_to_use)
                
    #             # Rotate the text slightly
    #             rotated_text = pygame.transform.rotate(rendered_text, line_angle)
                
    #             # Position with wobble
    #             self.letter_surface.blit(rotated_text, (x_position, y_offset))
    #             y_offset += 15 if i >= len(self.text) - 2 else 15
        
    #     # Apply shadow effect
    #     if self.alpha >= 180:  # Only add shadow once letter is mostly visible
    #         screen.blit(self.shadow, (200, 0)) # 200px from left
            
    #     # Apply the letter surface with alpha for fade-in effect
    #     temp_surface = self.letter_surface.copy() # create a copy to apply alpha
    #     temp_surface.set_alpha(self.alpha) # set alpha for fade-in
    #     screen.blit(temp_surface, (200, 0)) # 200px from left
        
    #     # Handle fade-in timing for initial appearance
    #     if self.alpha < 255: # Fade in the entire letter
    #         self.alpha += 5  # Fade in the entire letter, adjust speed as needed
    #     else: 
    #         # Once the letter has faded in, start revealing lines
    #         self.fade_in_timer += 5 # increment timer
    #         if self.fade_in_timer > 90: # 60 frames for 1 second
    #             self.fade_in_timer = 0
    #             if self.fade_in_index < len(self.text) - 1:
    #                 self.fade_in_index += 1

    def load_letter_text(file_path):
        try:
            with open(file_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            return ""

    def draw(self, screen):
        """Render the current page of the letter."""
        screen.fill((255, 252, 232))  # Cream background

        # Render each line of the current page
        y_offset = 100
        for line in self.pages[self.current_page]:
            rendered_text = self.font.render(line, True, self.color)
            screen.blit(rendered_text, (50, y_offset))
            y_offset += self.line_height

        # Draw navigation instructions
        if self.current_page > 0:
            prev_text = self.font.render("Press LEFT for Previous Page", True, self.color)
            screen.blit(prev_text, (50, HEIGHT - 50))
        if self.current_page < len(self.pages) - 1:
            next_text = self.font.render("Press RIGHT for Next Page", True, self.color)
            screen.blit(next_text, (WIDTH - 300, HEIGHT - 50))

    def handle_navigation(self, event):
        """Handle page navigation."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and self.current_page < len(self.pages) - 1:
                self.current_page += 1
            elif event.key == pygame.K_LEFT and self.current_page > 0:
                self.current_page -= 1

class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x  # Store original coordinates for access
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.hover_growth = 1.05  # Button grows slightly on hover
        self.is_hovered = False
        self.pulse_value = 0
        self.pulse_direction = 1

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Create a pulsing effect
        self.pulse_value += 0.05 * self.pulse_direction
        if self.pulse_value > 1:
            self.pulse_value = 1
            self.pulse_direction = -1
        elif self.pulse_value < 0:
            self.pulse_value = 0
            self.pulse_direction = 1
            
        # Calculate button size based on hover state
        if self.is_hovered:
            current_width = int(self.width * self.hover_growth)
            current_height = int(self.height * self.hover_growth)
            current_x = self.x - (current_width - self.width) // 2
            current_y = self.y - (current_height - self.height) // 2
            
            # Pulse color between color and hover_color
            r = self.color[0] + (self.hover_color[0] - self.color[0]) * self.pulse_value
            g = self.color[1] + (self.hover_color[1] - self.color[1]) * self.pulse_value
            b = self.color[2] + (self.hover_color[2] - self.color[2]) * self.pulse_value
            current_color = (r, g, b)
        else:
            current_width = self.width
            current_height = self.height
            current_x = self.x
            current_y = self.y
            current_color = self.color
            
        button_rect = pygame.Rect(current_x, current_y, current_width, current_height)
        
        # Draw button with rounded corners
        pygame.draw.rect(screen, current_color, button_rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), button_rect, 2, border_radius=10)  # Border
        
        # Draw text
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (button_rect.centerx - text_surface.get_width() // 2,
                                  button_rect.centery - text_surface.get_height() // 2))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.scroll_y += 20
            elif event.key == pygame.K_UP:
                self.scroll_y = max(self.scroll_y - 20, 0)