class Settings:
    def __init__(self):
        
        self.screen_width = 1500
        self.screen_height = 800
        self.bg_color = (0, 50, 100)  
        self.submarine_limit = 2

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60) 
        self.bullets_allowed = 20        

        self.boss_bullet_speed = 2.0
        self.boss_bullet_color = (0, 255, 0) 
        self.boss_fire_frequency = 1000
        self.fleet_drop_speed = 10

        self.speedup_scale = 1.5

        self.score_scale = 1.5

        self.initialize_dynamic_settings()

        # Configuración de niveles
        self.max_levels = 3
        self.level_data = {
            1: {
                'enemy_image': 'images/enemy.png',
                'enemy_speed': 1.0,
                'bg_color': (0, 50, 100),
                'points': 50
            },
            2: {
                'enemy_image': 'images/enemy2.png',
                'enemy_speed': 1.5,
                'bg_color': (0, 30, 70),
                'points': 75
            },
            3: {
                'enemy_image': 'images/enemy3.png',
                'enemy_speed': 2.0,
                'bg_color': (0, 10, 40),
                'points': 100
            }
        }
        self.current_level = 1
        self.initialize_dynamic_settings()
        self.boss_health = 35 
        self.boss_speed = 1.2
        self.boss_points = 1000  


    def initialize_dynamic_settings(self):

        self.submarine_speed = 2.0
        self.bullet_speed = 3.0
        self.enemy_speed = 2.0
 
        self.fleet_direction = 1

        self.alien_points = 50

    def initialize_level_settings(self):
        """Carga configuración específica del nivel actual"""
        level = self.level_data[self.current_level]
        self.enemy_speed = level['enemy_speed']
        self.bg_color = level['bg_color']
        self.alien_points = level['points']

    def increase_speed(self):

        self.submarine_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.enemy_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
