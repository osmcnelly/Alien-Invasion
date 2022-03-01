import pygame
class Settings:
    """A Class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800


        self.bg = pygame.image.load("images/background.jpg")

        self.bg = pygame.transform.scale(
            self.bg,(self.screen_width, self.screen_height))
        self.bg_rect = self.bg.get_rect()
        self.bg_rect = self.bg_rect.move((0, 0))

        # Ship Settings
        self.ship_limit = 3

        # Bullet Settings
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (235, 235, 35)
        self.bullets_allowed = 3

        # Alien Settings
        self.fleet_drop_speed = 200

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        self.difficulty_level = 'easy'

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        # Scoring
        self.alien_points = 50

        if self.difficulty_level == 'easy':
            self.ship_limit = 5
            self.bullets_allowed = 10
            self.ship_speed = 0.75
            self.bullet_speed = 1.5
            self.alien_speed = 0.5
        elif self.difficulty_level == 'medium':
            self.ship_limit = 3
            self.bullets_allowed = 5
            self.ship_speed = 1.5
            self.bullet_speed = 3.0
            self.alien_speed = 1.0
        elif self.difficulty_level == 'difficult':
            self.ship_limit = 2
            self.bullets_allowed = 3
            self.ship_speed = 3.0
            self.bullet_speed = 6.0
            self.alien_speed = 2.0

        # Scoring
        self.alien_points = 50

        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
       
    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

    def set_difficulty(self, diff_setting):
        if diff_setting == 'easy':
            print('easy')
        elif diff_setting == 'medium':
            pass
        elif diff_setting == 'difficult':
            pass

        