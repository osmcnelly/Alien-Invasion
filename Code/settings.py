import pygame


class Settings:
    """A Class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen Settings
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        self.screen_bottom = self.screen.get_rect().bottom

        # Setting Background image and scaling it to fit the current screen
        self.bg = pygame.image.load("./images/background.jpg")
        self.bg = pygame.transform.scale(
            self.bg, (self.screen_width, self.screen_height))

        # Assigning the background image rect
        self.bg_rect = self.bg.get_rect()
        self.bg_rect = self.bg_rect.move((0, 0))

        # Ship Settings
        self.ship_limit = 3
        self.ship_health = 5

        # Bullet Settings
        self.bullets_allowed = 3

        # Alien Settings
        self.fleet_drop_speed = 10
        self.alien_health = 0
        self.boss_health = 5
        self.alien_bullet_speed = 4.0
        self.alien_bullets_allowed = 5

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Default difficulty if the player does not select a difficulty
        self.difficulty_level = 'rookie'

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        # Scoring

        # Three difficulty levels that increase speed and decrease ships and
        # bullets as the difficulty level increases
        if self.difficulty_level == 'rookie':
            self.ship_limit = 4
            self.bullets_allowed = 10
            self.ship_speed = 2
            self.bullet_speed = 4.0
            self.alien_speed = 1.5
            self.alien_bullet_speed = 4
            self.alien_bullets_allowed = 5
            self.alien_points = 50


        elif self.difficulty_level == 'hero':
            self.ship_limit = 3
            self.bullets_allowed = 5
            self.ship_speed = 3.0
            self.bullet_speed = 6.0
            self.alien_speed = 2.0
            self.alien_bullet_speed = 6
            self.alien_bullets_allowed = 5
            self.alien_points = 100


        elif self.difficulty_level == 'veteran':
            self.ship_limit = 2
            self.bullets_allowed = 3
            self.ship_speed = 6.0
            self.bullet_speed = 8.0
            self.alien_speed = 4.0
            self.alien_bullet_speed = 8
            self.alien_bullets_allowed = 5
            self.alien_points = 150

        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
