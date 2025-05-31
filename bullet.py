import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
 

    def __init__(self, ai_game):

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = (255, 255, 255)

        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)

        self.rect.midtop = ai_game.submarine.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        """Mueve la bala hacia arriba"""
        self.y -= self.settings.bullet_speed  
        self.rect.y = self.y  

    def draw_bullet(self):
        #"""Draw the bullets to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)