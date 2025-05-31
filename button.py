# button.py
import pygame.font

class Button:
    def __init__(self, ai_game, msg):
        """Inicializa los atributos del botón"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        # Configuración 
        self.width, self.height = 250, 60
        self.button_color = (0, 120, 180)
        self.text_color = (255, 255, 200)
        self.hover_color = (0, 180, 240)
        self.font = pygame.font.Font(None, 48)
        self.padding = 20
        self.rect = pygame.Rect(0, 0, self.width, self.height)  # Rectángulo completo
        self._prep_msg(msg)
      
        self.is_hovered = False

    def _prep_msg(self, msg):
        """Convierte msg en una imagen y centra el texto en el botón"""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.rect.width = max(self.width, self.msg_image_rect.width + self.padding)
        self.rect.height = max(self.height, self.msg_image_rect.height + self.padding)

    def draw_button(self):
        """Dibuja el botón y luego el mensaje"""
        current_color = self.hover_color if self.is_hovered else self.button_color
        
        pygame.draw.rect(self.screen, current_color, self.rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 2, border_radius=10)  
        
        self.msg_image_rect.center = self.rect.center
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def check_hover(self, mouse_pos):
        """Actualiza el estado hover del botón"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered