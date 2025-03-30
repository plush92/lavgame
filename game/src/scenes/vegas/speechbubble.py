import pygame

class SpeechBubble:
    """
    A class to create and display speech bubbles for character dialogues.
    """
    def __init__(self, character, text, font, padding=10, max_width=300, bg_color=(255, 255, 255), text_color=(0, 0, 0), outline_color=(0, 0, 0)):
        self.character = character  # The character speaking
        self.text = text  # The dialogue text
        self.font = font  # Font for rendering
        self.padding = padding  # Padding around text
        self.max_width = max_width  # Maximum width for text wrapping
        self.bg_color = bg_color  # Background color of speech bubble
        self.text_color = text_color  # Text color
        self.outline_color = outline_color  # Outline color
        self.outline_width = 2  # Width of the outline
        
        # Calculate bubble position and size
        self._prepare_bubble()
        
    def _prepare_bubble(self):
        """Prepare the speech bubble by calculating text dimensions and wrapping if needed"""
        # Determine if the text needs to be wrapped
        speaker_prefix = f"{self.character.name.capitalize()}: "
        full_text = speaker_prefix + self.text
        
        # Check if text exceeds max width
        test_surface = self.font.render(full_text, True, self.text_color)
        if test_surface.get_width() > self.max_width:
            self.wrapped_lines = self._wrap_text(full_text)
        else:
            self.wrapped_lines = [full_text]
        
        # Calculate text height based on number of lines
        line_height = self.font.get_linesize()
        self.text_height = line_height * len(self.wrapped_lines)
        
        # Find the widest line
        self.text_width = max(self.font.render(line, True, self.text_color).get_width() for line in self.wrapped_lines)
        
        # Create the bubble rectangle
        self.bubble_width = self.text_width + (self.padding * 2)
        self.bubble_height = self.text_height + (self.padding * 2)
        
    def _wrap_text(self, text):
        """Wrap text to fit within max_width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            # Try adding the next word
            test_line = ' '.join(current_line + [word])
            test_width = self.font.render(test_line, True, self.text_color).get_width()
            
            if test_width <= self.max_width:
                current_line.append(word)
            else:
                # If current line already has words, finish it and start a new one
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # If the word itself is too long, just add it anyway
                    lines.append(word)
                    current_line = []
        
        # Add the last line if there's anything left
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines
        
    def _calculate_position(self):
        """Calculate the position of the speech bubble relative to the character"""
        # Position the bubble above the character by default
        x = self.character.rect.centerx - (self.bubble_width / 2)
        y = self.character.rect.top - self.bubble_height - 10
        
        # Ensure the bubble stays within screen bounds (assuming screen size is known)
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()
        
        # Adjust x if out of bounds
        if x < 10:
            x = 10
        elif x + self.bubble_width > screen_width - 10:
            x = screen_width - self.bubble_width - 10
            
        # If bubble would be off the top of the screen, position it below the character
        if y < 10:
            y = self.character.rect.bottom + 10
            
        return pygame.Rect(x, y, self.bubble_width, self.bubble_height)
    
    def _draw_tail(self, screen, bubble_rect):
        """Draw a tail connecting the bubble to the character"""
        # Points for the triangle tail
        char_center_x = self.character.rect.centerx
        
        if bubble_rect.bottom < self.character.rect.top:
            # Bubble is above character
            points = [
                (bubble_rect.centerx, bubble_rect.bottom),
                (bubble_rect.centerx - 10, bubble_rect.bottom - 5),
                (bubble_rect.centerx + 10, bubble_rect.bottom - 5)
            ]
        else:
            # Bubble is below character
            points = [
                (bubble_rect.centerx, bubble_rect.top),
                (bubble_rect.centerx - 10, bubble_rect.top + 5),
                (bubble_rect.centerx + 10, bubble_rect.top + 5)
            ]
            
        pygame.draw.polygon(screen, self.bg_color, points)
        pygame.draw.polygon(screen, self.outline_color, points, 1)

    def draw(self, screen):
        """Draw the speech bubble with text"""
        # Calculate bubble position
        bubble_rect = self._calculate_position()
        
        # Draw bubble background
        pygame.draw.rect(screen, self.bg_color, bubble_rect, border_radius=8)
        pygame.draw.rect(screen, self.outline_color, bubble_rect, self.outline_width, border_radius=8)
        
        # Draw the connecting tail
        self._draw_tail(screen, bubble_rect)
        
        # Draw text
        for i, line in enumerate(self.wrapped_lines):
            text_surface = self.font.render(line, True, self.text_color)
            text_x = bubble_rect.x + self.padding
            text_y = bubble_rect.y + self.padding + (i * self.font.get_linesize())
            screen.blit(text_surface, (text_x, text_y))