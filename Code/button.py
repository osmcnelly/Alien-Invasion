import pygame

class Button:

    def __init__(self, ai_game, msg):
        """initialize the button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (8, 80, 128)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _change_button_color(self):
        """Changes the button color when the button is clicked"""  
        self.button_color = (66, 94, 112)

    def _reset_button_color(self):
        """
        Used to change button color back when a different button is selected
        """
        self.button_color = (8, 80, 128)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the bottom."""
        self.msg_image = self.font.render(msg, True, self.text_color, 
                self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def _update_msg_position(self):
        """Center the text on the button if the button moves."""
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

