import pygame
from pygame.sprite import Sprite
from boss_bullet import BossBullet

class BossEnemy(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.game = ai_game  
        self.image = pygame.image.load('images/enemy4.png')
        self.image = pygame.transform.scale(self.image, 
                                          (self.image.get_width()*2, 
                                           self.image.get_height()*2))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen.get_rect().centerx
        self.rect.top = 20 
        
        self.x = float(self.rect.x)
        self.health = self.settings.boss_health
        self.last_shot = 0  
        self.bullets = pygame.sprite.Group()

    def update(self):
        """Actualizar posición y disparos del jefe"""
        
        self.x += (self.settings.boss_speed * self.settings.fleet_direction)
        self.rect.x = self.x
        
  
        if self.rect.right >= self.screen.get_rect().right or self.rect.left <= 0:
            self.settings.fleet_direction *= -1
       
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.settings.boss_fire_frequency:
            self._fire_bullet()
            self.last_shot = now

    def _fire_bullet(self):
        """Disparar una bala verde"""
        new_bullet = BossBullet(self.game, self.rect.centerx, self.rect.bottom)  
        self.bullets.add(new_bullet)