import random

class ScreenShaker:
    def __init__(self):
        self.shake_duration = 0
        self.shake_intensity = 10
    
    def shake(self, intensity, duration):
        """Triggers a screen shake effect with given intensity and duration."""
        self.shake_duration = duration
        self.shake_intensity = intensity
    
    def update(self, dt):
        """Reduce shake duration over time."""
        if self.shake_duration > 0:
            self.shake_duration -= dt
            if self.shake_duration < 0:
                self.shake_duration = 0
    
    def get_offset(self):
        """Returns random screen offset if shaking, otherwise (0, 0)."""
        if self.shake_duration > 0:
            return (random.randint(-self.shake_intensity, self.shake_intensity),
                    random.randint(-self.shake_intensity, self.shake_intensity))
        return (0, 0)

    def reset(self):
        """Resets the shake effect."""
        self.shake_duration = 0
        self.shake_intensity = 10
        # Reset shake intensity to default
        # This can be adjusted based on game events or player actions
        # For example, you can increase the intensity after a certain event
        # self.shake_intensity = 20  # Example of increasing intensity
  