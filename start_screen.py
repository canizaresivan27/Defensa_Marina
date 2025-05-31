import pygame
from button import Button

class StartScreen:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        try:
            self.background = pygame.image.load('images/menu_bg.png').convert()
            self.background = pygame.transform.scale(
                self.background, 
                (self.screen_rect.width, self.screen_rect.height))
        except:
            self.background = None
            self.bg_color = (0, 20, 40)  

        self.title_font = pygame.font.Font(None, 90)
        self.title_font.set_bold(True)
        
        self.header_font = pygame.font.Font(None, 50)
        self.header_font.set_bold(True)
        
        self.text_font = pygame.font.Font(None, 36)
        self.text_font.set_bold(True)
        
        # Colores
        self.title_color = (0, 255, 255)    
        self.text_color = (200, 240, 255)   
        self.highlight_color = (255, 150, 0) 
        self.outline_color = (0, 50, 100)   
        
        # Botón mejorado
        self.start_button = Button(ai_game, "INICIAR MISIÓN")
        self.start_button.rect.right = self.screen_rect.right - 50
        self.start_button.rect.top = self.screen_rect.centery + 100
        self.start_button.button_color = (0, 120, 180)
        self.start_button.hover_color = (0, 180, 240)
        self.start_button.text_color = (255, 255, 200)
        self.start_button.font = pygame.font.Font(None, 48)
        self.start_button._prep_msg("INICIAR MISIÓN")

    def draw(self):
        """Dibuja la pantalla de inicio con todas las mejoras"""
     
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(self.bg_color)
        
        title = self.title_font.render("DEFENSA SUBMARINA", True, self.title_color)
        title_rect = title.get_rect(center=(self.screen_rect.centerx, 80))
        self.screen.blit(title, title_rect)
        
        subtitle_text = "¡Repela a los calamares invasores!"
        outline_size = 3 
        
        for x in [-outline_size, 0, outline_size]:
            for y in [-outline_size, 0, outline_size]:
                if x != 0 or y != 0:
                    outline = self.header_font.render(subtitle_text, True, self.outline_color)
                    outline_rect = outline.get_rect(center=(self.screen_rect.centerx + x, 160 + y))
                    self.screen.blit(outline, outline_rect)
        
        subtitle = self.header_font.render(subtitle_text, True, self.highlight_color)
        subtitle_rect = subtitle.get_rect(center=(self.screen_rect.centerx, 160))
        self.screen.blit(subtitle, subtitle_rect)
        
        controls = [
            "CONTROLES DE SONAR:",
            "<-  -> : Navegar por las profundidades",
            "ESPACIO : Lanzar torpedos",
            "Q : Emerger a superficie"
        ]
        
        right_margin = self.screen_rect.right - 50
        y_position = 250
        
        for i, line in enumerate(controls):
            color = self.highlight_color if i == 0 else self.text_color
            text = self.text_font.render(line, True, color)
            text_rect = text.get_rect(topright=(right_margin, y_position + i * 45))
            self.screen.blit(text, text_rect)
        
        self.start_button.draw_button()
        
        warning = self.text_font.render("¡Elimina todas las amenazas para completar la misión!", 
                                      True, (255, 80, 80))
        warning_rect = warning.get_rect(bottomright=(right_margin, self.screen_rect.bottom - 50))
        self.screen.blit(warning, warning_rect)