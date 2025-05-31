import sys      
import pygame   
from settings import Settings       
from submarine import Submarine     
from bullet import Bullet           
from enemy import Enemy             
from time import sleep              
from game_stats import GameStats    
from button import Button           
from scoreboard import Scoreboard   
from background import OceanBackground
from start_screen import StartScreen
from boss_enemy import BossEnemy
import pygame.mixer  

class EnemyInvasion:
    #"""Overall class to manage game assets and behavior."""

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.settings = Settings()

        # Sonidos
        self.sounds = {
            'shoot': pygame.mixer.Sound('sounds/shoot.wav'),
            'hit': pygame.mixer.Sound('sounds/hit.wav'),
            'boss_spawn': pygame.mixer.Sound('sounds/boss_spawn.wav'),
            'boss_defeat': pygame.mixer.Sound('sounds/boss_defeat.wav'),
            'game_over': pygame.mixer.Sound('sounds/game_over.wav')
        }
        
        self.sounds['shoot'].set_volume(0.5)
        self.sounds['hit'].set_volume(0.7)
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Submarine Defense")
        
        self.screen_rect = self.screen.get_rect()
        
        self.background = OceanBackground(self.screen)
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.submarine = Submarine(self)
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        self.play_button = Button(self, "Jugar")
        self.play_button.rect.center = self.screen_rect.center 
        
        self._create_fleet()
        self.start_screen = StartScreen(self)
        self.show_start_screen = True
        self.stats.game_active = False
        
    def run_game(self):
        """Bucle principal del juego"""
        while True:
        
            if self.show_start_screen:
                self._check_start_events()
                self._draw_start_screen()
            
            else:
                self._check_events()
                
                if self.stats.game_active:
                    if hasattr(self, 'boss_active') and self.boss_active:
                       
                        self._update_boss_fight()
                    else:
                        
                        self._update_game_objects()
                
                self._update_screen()
    
    

    def _check_start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.start_screen.start_button.rect.collidepoint(mouse_pos):  
                    self.show_start_screen = False
                    self.stats.game_active = True  
                    pygame.mouse.set_visible(False)
                    self.settings.initialize_dynamic_settings()  
                    self.stats.reset_stats()  
                    self.sb.prep_score() 
    
    def _draw_start_screen(self):
        """Dibuja la pantalla de inicio"""
        self.start_screen.draw()  
        pygame.display.flip()

    def _update_game_objects(self):
        """Actualiza los objetos del juego"""
        self.submarine.update()
        self._update_bullets()
        self._update_enemies()

    def _submarine_hit(self):
        """Responde al impacto de un enemigo o bala al submarino"""
        if self.stats.submarines_left > 0:
           
            self.stats.submarines_left -= 1
            self.sb.prep_submarines()
           
            self.bullets.empty()
            
            if hasattr(self, 'boss_active') and self.boss_active:
           
                if hasattr(self, 'boss'):
                    self.boss.bullets.empty()
                    self.boss.rect.centerx = self.screen_rect.centerx
                    self.boss.rect.top = 20
                    self.boss.x = float(self.boss.rect.x)
            else:
             
                self.enemies.empty()
                self._create_fleet()
            
            self.submarine.center_submarine()
            sleep(0.5)
        else:
       
            self.stats.game_active = False
            if hasattr(self, 'boss'):
                del self.boss
            if hasattr(self, 'boss_active'):
                self.boss_active = False
            pygame.mouse.set_visible(True)
            self._show_game_over()

    def _check_enemies_bottom(self):
        
        screen_rect = self.screen.get_rect()
        for enemy in self.enemies.sprites():
            if enemy.rect.bottom >= screen_rect.bottom:
             
                self._submarine_hit()
                break

    def _update_enemies(self):
       
        self._check_fleet_edges()
        self.enemies.update()

        if pygame.sprite.spritecollideany(self.submarine, self.enemies):
            self._submarine_hit()
        self._check_enemies_bottom()


    def _create_fleet(self):
        """Create the fleet of enemies."""

        enemy = Enemy(self)
        enemy_width, enemy_height = enemy.rect.size
        available_space_x = self.settings.screen_width - (2 * enemy_width)
        number_enemies_x = available_space_x // (2 * enemy_width)

        submarine_height = self.submarine.rect.height
        available_space_y = (self.settings.screen_height - (3 * enemy_height) - submarine_height)
        number_rows = available_space_y // (2 * enemy_height)

     
        for row_number in range(number_rows):
            for enemy_number in range(number_enemies_x):
                self._create_enemy(enemy_number, row_number)


    def _check_fleet_edges(self):
       
        for enemy in self.enemies.sprites():
            if enemy.check_edges():
                self._change_fleet_direction()
                break



    def _change_fleet_direction(self):
  
        for enemy in self.enemies.sprites():
            enemy.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1



    def _create_enemy(self, enemy_number, row_number):

        enemy = Enemy(self)
        enemy_width, enemy_height = enemy.rect.size
        enemy.x = enemy_width + 2 * enemy_width * enemy_number
        enemy.rect.x = enemy.x
        enemy.rect.y = enemy.rect.height + 2 * enemy.rect.height * row_number
        self.enemies.add(enemy)


    def _check_events(self):
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
              
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)



    def _check_play_button(self, mouse_pos):
      
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:

            self.settings.initialize_dynamic_settings()

            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_submarines()

            self.enemies.empty()
            self.bullets.empty()

            self._create_fleet()
            self.submarine.center_submarine()

            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):

        if event.key == pygame.K_RIGHT:
        
            self.submarine.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.submarine.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()  
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()       


    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
      
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.sounds['shoot'].play()


    def _show_game_over(self):
        """Muestra pantalla de Game Over y reinicia al nivel 1"""
  
        self.sounds['game_over'].play()
        self.bullets.empty()
        if hasattr(self, 'enemies'):
            self.enemies.empty()
        if hasattr(self, 'boss'):
            del self.boss  
        if hasattr(self, 'boss_active'):
            self.boss_active = False
        
        try:
            bg = pygame.image.load('images/game_over.png')
            bg = pygame.transform.scale(bg, (self.settings.screen_width, self.settings.screen_height))
            self.screen.blit(bg, (0, 0))
        except:
            self.screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 72)
            text = font.render("GAME OVER", True, (255, 0, 0))
            self.screen.blit(text, (self.screen_rect.centerx - 150, self.screen_rect.centery - 100))

        self.restart_button = Button(self, "Jugar de nuevo")
        self.restart_button.rect.centerx = self.screen_rect.centerx
        self.restart_button.rect.centery = self.screen_rect.centery + 75
        self.restart_button.draw_button()

        pygame.display.flip()
        self._wait_for_restart()
        
    def _wait_for_restart(self):
        """Espera input para reiniciar"""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.restart_button.rect.collidepoint(mouse_pos):
                        waiting = False
                        self._restart_game()


    def _restart_game(self):
        """Reinicia completamente el juego al nivel 1"""
        
        self.settings.current_level = 1  
        self.settings.initialize_dynamic_settings()
        self.settings.initialize_level_settings()
        
        self.stats.reset_stats()
        self.stats.score = 0
        self.stats.level = 1
        
        self.bullets.empty()
        self.enemies.empty()
        if hasattr(self, 'boss'):
            del self.boss
        if hasattr(self, 'boss_active'):
            self.boss_active = False
        
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_submarines()
        
        self._create_fleet()
        self.submarine.center_submarine()
        
        self.stats.game_active = True
        pygame.mouse.set_visible(False)

    def _update_boss_fight(self):
        """Actualiza la lógica durante la pelea con el jefe"""

        self.submarine.update()

        self.boss.update()

        self._update_bullets()
        
  
        self._update_boss_bullets()
        
        self._check_boss_collisions()
        self._check_boss_bullet_collisions()


    def _check_bullet_enemy_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        
        if collisions:
            self.sounds['hit'].play()
            for enemies in collisions.values():
                self.stats.score += self.settings.alien_points * len(enemies)
                self.sb.prep_score()
                self.sb.check_high_score()

        if not self.enemies:
            if self.settings.current_level < self.settings.max_levels:
                self._advance_level()  
            else:
                self._spawn_boss()  

    def _spawn_boss(self):
        """Activar el jefe final"""
        self.boss = BossEnemy(self)
        self.boss_active = True
        self.boss.bullets = pygame.sprite.Group()
        self.sounds['boss_spawn'].play()  
        print("¡APARECIÓ EL JEFE FINAL!")

    def _check_boss_collisions(self):
        """Verifica colisiones entre balas y el jefe"""
        if hasattr(self, 'boss'):
            collisions = pygame.sprite.spritecollide(
                self.boss, self.bullets, True)
            
            if collisions:
                self.sounds['hit'].play()
                self.boss.health -= len(collisions)
                if self.boss.health <= 0:
                    self.sounds['boss_defeat'].play()
                    
                    self.stats.score += self.settings.boss_points
                    self.sb.prep_score()  
                    self.sb.check_high_score()  
                    self._show_victory_screen()
                    self.boss_active = False

    def _advance_level(self):
        """Avanzar al siguiente nivel normal"""
        self.show_level_transition()
        self.settings.current_level += 1
        self.stats.level += 1
        self._load_level()

    def _check_keyup_events(self, event):

        if event.key == pygame.K_RIGHT:
            self.submarine.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.submarine.moving_left = False

    def _update_bullets(self):
        """Actualiza la posición de las balas y elimina las que salen de pantalla"""
      
        self.bullets.update()
        
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        if hasattr(self, 'boss_active') and self.boss_active:
            self._check_boss_collisions()
        else:
            self._check_bullet_enemy_collisions()
    
    def _update_screen(self):
        """Actualiza imágenes en la pantalla y cambia a la pantalla nueva"""
       
        self.background.update()
       
        self.submarine.blitme()
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.enemies.draw(self.screen)
        
        if hasattr(self, 'boss_active') and self.boss_active:
           
     
            for bullet in self.boss.bullets.sprites():
                bullet.draw_bullet()
    
        self.sb.show_score()
        
        if not self.stats.game_active and not self.show_start_screen:
            if hasattr(self, 'restart_button'):
                self.restart_button.draw_button()
        
        pygame.display.flip()

    def show_level_transition(self):
        """Muestra la pantalla de transición entre niveles"""
      
        try:
            bg = pygame.image.load('images/menu_bg.png')
            bg = pygame.transform.scale(bg, (self.settings.screen_width, self.settings.screen_height))
            self.screen.blit(bg, (0, 0))
        except:
            self.screen.fill((0, 20, 40))  
            
        font = pygame.font.Font(None, 120)
        level_text = f"Nivel {self.stats.level}"
        text_surface = font.render(level_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.screen_rect.center)
        
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
        
        pygame.time.delay(3000)
    
    def _show_victory_screen(self):
        """Muestra la pantalla de victoria con fondo del menú y texto a la derecha"""
       
        try:
            bg = pygame.image.load('images/menu_bg.png')
            bg = pygame.transform.scale(bg, (self.settings.screen_width, self.settings.screen_height))
            self.screen.blit(bg, (0, 0))
        except:
            self.screen.fill((0, 20, 40))  
        
        font_large = pygame.font.Font(None, 100)  
        font_medium = pygame.font.Font(None, 60)  
        text_color = (255, 255, 255)              
        right_margin = self.settings.screen_width - 200  
        
        messages = [
            ("¡VICTORIA!", font_large),
            (f"Puntuación: {self.stats.score}", font_medium),
            ("Presiona Q para salir", font_medium)
        ]
        
        y_position = 150  
        
        for msg, font in messages:
            text_surface = font.render(msg, True, text_color)
          
            text_rect = text_surface.get_rect(right=right_margin, top=y_position)
            self.screen.blit(text_surface, text_rect)
            y_position += 80 
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        waiting = False
                        pygame.quit()
                        sys.exit()

    def _load_level(self):
        """Carga la configuración del nivel actual"""
        self.settings.initialize_level_settings()  
        self.background.bg_color = self.settings.bg_color
        self._create_fleet()
        self.submarine.center_submarine()
        self.bullets.empty()

    def _update_boss_bullets(self):
        """Actualizar balas del jefe"""
        self.boss.bullets.update()
       
        for bullet in self.boss.bullets.copy():
            if bullet.rect.top > self.settings.screen_height:
                self.boss.bullets.remove(bullet)
        
        for bullet in self.boss.bullets.sprites():
            bullet.draw_bullet()

    def _check_boss_bullet_collisions(self):
        """Verificar colisiones con balas del jefe"""
        if hasattr(self, 'boss') and pygame.sprite.spritecollideany(self.submarine, self.boss.bullets):
            self._submarine_hit()
            if hasattr(self, 'boss'):
                self.boss.bullets.empty()

if __name__ == '__main__':
   
    ai = EnemyInvasion()
    ai.run_game()