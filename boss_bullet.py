import pygame
from pygame.sprite import Sprite

class BossBullet(Sprite):
    def __init__(self, ai_game, x, y):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = (0, 255, 0)  # Verde
        
        self.rect = pygame.Rect(0, 0, 15, 30)
        self.rect.centerx = x
        self.rect.top = y
        self.y = float(self.rect.y)

    def update(self):
        self.y += self.settings.boss_bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)