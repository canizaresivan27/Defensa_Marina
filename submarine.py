import pygame
from pygame.sprite import Sprite


class Submarine(Sprite):
    # """A class to manage the submarine."""
    def __init__(self, ai_game):
        
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings    
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('images/submarine.png')
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False


    def center_submarine(self):
        """Center the submarine on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)


    def update(self):
 
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.submarine_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.submarine_speed

        self.rect.x = self.x


    def blitme(self):

        self.screen.blit(self.image, self.rect)