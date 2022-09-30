import pygame

from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Set the alien width and height to a percentage of the screen rect's 
        # width and height. This allows the alien image to scale 
        # up and down between screen resolutions.       
        self.alien_width = self.screen.get_rect().width * .035
        self.alien_height = self.screen.get_rect().height * .048

        # Load the alien image and set its scale and rect attribute. 
        self.image = pygame.image.load('images/alien-medium.png')
        self.image = pygame.transform.scale(self.image, (
            self.alien_width, self.alien_height))
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def _change_alien_image(self):
        self.image = pygame.image.load('images/boss2.png')
        self.rect = self.image.get_rect()

    def update(self):
        """Move the alien to the right."""
        self.mask = pygame.mask.from_surface(self.image)
        self.x += (self.settings.alien_speed *
                   self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
