import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.bullet_width = self.screen.get_rect().width * .02
        self.bullet_height = self.screen.get_rect().height * .04

        # Load the alien image and set its scale and rect attribute. 
        self.image = pygame.image.load('images/bullet.png')
        self.image = pygame.transform.scale(
            self.image,(self.bullet_width, self.bullet_height))
        self.rect = self.image.get_rect()


        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.bullet_width,
            self.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Ship Lazer sound
        self.lazer = pygame.mixer.Sound('Sounds/lazer.wav')
        self.lazer.play()


        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        self.mask = pygame.mask.from_surface(self.image)
        # Update the decimal position of the bullet
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y

class AlienBullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, x, y):
        """Create a bullet object at the ship's current position."""
        super().__init__()

        self.bullet_speed = 2

        # Load the alien image and set its scale and rect attribute. 
        self.image = pygame.image.load('images/alien_bullet.png')
        # self.image = pygame.transform.scale(
        #     self.image,(self.bullet_width, self.bullet_height))
        self.rect = self.image.get_rect()


        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, .02, .04)
        self.rect.center = [x, y]

        # Ship Lazer sound
        self.lazer = pygame.mixer.Sound('Sounds/lazer.wav')
        self.lazer.play()


        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        self.mask = pygame.mask.from_surface(self.image)
        # Update the decimal position of the bullet
        self.y += self.bullet_speed
        # Update the rect position
        self.rect.y = self.y





