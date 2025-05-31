import pygame
import os

class OceanBackground:
    def __init__(self, screen):
        self.screen = screen
       
        image_path = os.path.join('images', 'ocean_bg.png')
        
        
        print("\n[DEBUG] Buscando imagen en:", os.path.abspath(image_path))
        print("[DEBUG] ¿Existe el archivo?:", os.path.exists(image_path))
        
        try:
           
            print("[DEBUG] Intentando cargar la imagen...")
            self.bg_image = pygame.image.load(image_path).convert()
            
            print("[DEBUG] ¡Imagen cargada correctamente!")
            print(f"[DEBUG] Dimensiones originales: {self.bg_image.get_width()}x{self.bg_image.get_height()}")
          
            self.bg_image = pygame.transform.scale(
                self.bg_image, 
                (screen.get_width(), screen.get_height()))
          
            print(f"[DEBUG] Dimensiones escaladas: {self.bg_image.get_width()}x{self.bg_image.get_height()}")
            
        except pygame.error as e:
            
            print("[DEBUG] ERROR al cargar imagen:", str(e))
            
            
            self.bg_image = None
            self.bg_color = (0, 50, 100)  
            print("[DEBUG] Usando color de fondo como fallback")
        
        self.bg_y = 0
    
    def update(self):
        if self.bg_image:
            
            print("[DEBUG] Dibujando imagen de fondo (posición y:", self.bg_y, ")") if self.bg_y == 0 else None
            
            self.bg_y = (self.bg_y + 0.5) % self.screen.get_height()
            self.screen.blit(self.bg_image, (0, self.bg_y))
            self.screen.blit(self.bg_image, (0, self.bg_y - self.screen.get_height()))
        else:
         
            print("[DEBUG] Dibujando fondo de color sólido")
            self.screen.fill(self.bg_color)