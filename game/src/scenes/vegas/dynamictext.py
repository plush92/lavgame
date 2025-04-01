import random
import pygame

class DynamicText:
    def __init__(self, text, font, color, x, y, bold=False):
        """Initialize the dynamic text object."""
        self.text = text
        self.base_font = font
        self.color = color
        self.x = x
        self.y = y
        self.bold = bold

        # Animation properties
        self.scale = 1.0  # Normal size
        self.shake_intensity = 0  # No shake by default
        self.animation_timer = 0  # Timer for animations
        
        # Store the original font size
        self.original_size = self.base_font.get_height()

    def trigger_animation(self, pop_scale=2, shake_intensity=5, duration=0.5):
        """Trigger a pop and shake animation."""
        self.scale = pop_scale
        self.shake_intensity = shake_intensity
        self.animation_timer = duration

    def update(self, dt):
        """Update text animations over time."""
        if self.animation_timer > 0:
            self.animation_timer -= dt  # Decrease timer
            if self.animation_timer <= 0:
                self.scale = 1.0  # Reset scale
                self.shake_intensity = 0  # Reset shake

        # Smoothly shrink back to normal
        if self.scale > 1.0:
            self.scale -= dt * 2  
            self.scale = max(1.0, self.scale)

        # Reduce shake intensity over time
        if self.shake_intensity > 0:
            self.shake_intensity -= dt * 10  
            self.shake_intensity = max(0, self.shake_intensity)

    def draw(self, screen):
        """Render the animated text with shake and scaling."""
        # Ensure font size is an integer
        font_size = max(15, int(self.original_size * self.scale))
        temp_font = pygame.font.SysFont('Arial', font_size, bold=self.bold)

        # Shake effect
        shake_x = random.randint(-int(self.shake_intensity), int(self.shake_intensity)) if self.shake_intensity > 0 else 0
        shake_y = random.randint(-int(self.shake_intensity), int(self.shake_intensity)) if self.shake_intensity > 0 else 0

        # Render and draw text
        rendered_text = temp_font.render(self.text, True, self.color)
        screen.blit(rendered_text, (self.x + shake_x, self.y + shake_y))