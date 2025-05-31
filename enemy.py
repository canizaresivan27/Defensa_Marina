import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
      
        enemy_image = self.settings.level_data[self.settings.current_level]['enemy_image']
        try:
            self.image = pygame.image.load(enemy_image)
        except:
  
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))  
            print(f"Error: No se encontró {enemy_image}")
        
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
    
    def update(self):
      
        self.x += (self.settings.enemy_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
       
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True