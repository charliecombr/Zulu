import pygame
import random
from config import *

class Car:
    def __init__(self):
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 20
        self.lane = 1  # 0: esquerda, 1: meio, 2: direita
        self.speed = 5
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
    
    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
    
    def move_right(self):
        if self.lane < 2:
            self.lane += 1
    
    def accelerate(self):
        if self.speed < MAX_SPEED:
            self.speed += SPEED_INCREMENT
    
    def brake(self):
        if self.speed > MIN_SPEED:
            self.speed -= SPEED_DECREMENT
    
    def update(self):
        road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
        target_x = road_left + (self.lane * LANE_WIDTH) + (LANE_WIDTH - self.width) // 2
        
        if self.x < target_x:
            self.x = min(self.x + 10, target_x)
        elif self.x > target_x:
            self.x = max(self.x - 10, target_x)
    
    def draw(self, surface):
        self.image.fill((0, 0, 0, 0))
        
        body_width = self.width - 4
        body_height = self.height - 10
        body_rect = pygame.Rect(2, 5, body_width, body_height)
        pygame.draw.rect(self.image, RED, body_rect, border_radius=8)
        
        dark_red = (180, 0, 0)
        roof_width = int(body_width * 0.7)
        roof_height = int(body_height * 0.5)
        roof_x = (self.width - roof_width) // 2
        roof_y = int(body_height * 0.15)
        roof_rect = pygame.Rect(roof_x, roof_y, roof_width, roof_height)
        pygame.draw.rect(self.image, dark_red, roof_rect, border_radius=6)
        
        window_color = (150, 200, 255)
        window_width = int(roof_width * 0.8)
        window_height = int(roof_height * 0.6)
        window_x = (self.width - window_width) // 2
        window_y = roof_y + int(roof_height * 0.2)
        pygame.draw.rect(self.image, window_color, 
                         (window_x, window_y, window_width, window_height),
                         border_radius=3)
        
        headlight_color = (255, 255, 100)
        headlight_width = int(body_width * 0.15)
        headlight_height = int(body_height * 0.06)
        left_headlight_x = 4
        right_headlight_x = self.width - headlight_width - 4
        headlight_y = 8
        pygame.draw.rect(self.image, headlight_color, 
                         (left_headlight_x, headlight_y, headlight_width, headlight_height))
        pygame.draw.rect(self.image, headlight_color, 
                         (right_headlight_x, headlight_y, headlight_width, headlight_height))
        
        taillight_color = (150, 0, 0)
        taillight_width = int(body_width * 0.15)
        taillight_height = int(body_height * 0.06)
        left_taillight_x = 4
        right_taillight_x = self.width - taillight_width - 4
        taillight_y = self.height - headlight_height - 8
        pygame.draw.rect(self.image, taillight_color, 
                         (left_taillight_x, taillight_y, taillight_width, taillight_height))
        pygame.draw.rect(self.image, taillight_color, 
                         (right_taillight_x, taillight_y, taillight_width, taillight_height))
        
        wheel_color = BLACK
        wheel_width = int(self.width * 0.2)
        wheel_height = int(self.height * 0.12)
        wheel_offset_x = -3  
        
        pygame.draw.rect(self.image, wheel_color, 
                         (wheel_offset_x, int(self.height * 0.2), 
                          wheel_width, wheel_height), border_radius=3)
        
        pygame.draw.rect(self.image, wheel_color, 
                         (self.width - wheel_width - wheel_offset_x, int(self.height * 0.2), 
                          wheel_width, wheel_height), border_radius=3)
        
        pygame.draw.rect(self.image, wheel_color, 
                         (wheel_offset_x, int(self.height * 0.7), 
                          wheel_width, wheel_height), border_radius=3)
        
        pygame.draw.rect(self.image, wheel_color, 
                         (self.width - wheel_width - wheel_offset_x, int(self.height * 0.7), 
                          wheel_width, wheel_height), border_radius=3)
        
        surface.blit(self.image, (self.x, self.y))
    
    def get_rect(self):
        collision_margin = 5
        return pygame.Rect(
            self.x + collision_margin, 
            self.y + collision_margin, 
            self.width - (2 * collision_margin), 
            self.height - (2 * collision_margin)
        )


class Obstacle:
    def __init__(self, lane):
        self.width = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT
        self.lane = lane
        road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
        self.x = road_left + (lane * LANE_WIDTH) + (LANE_WIDTH - self.width) // 2
        self.y = -self.height
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.passed = False
        
        self.car_style = random.randint(0, 2)
        
        self.color = self.generate_random_color()
        
        self.draw_obstacle_car()
    
    def generate_random_color(self):
        colors = [
            (0, 0, 255),      # Azul
            (0, 180, 0),      # Verde
            (0, 180, 255),    # Ciano
            (200, 180, 0),    # Amarelo
            (128, 0, 255),    # Roxo
            (0, 128, 128),    # Verde-azulado
            (70, 70, 200),    # Azul escuro
            (255, 128, 0),    # Laranja
            (0, 100, 50),     # Verde escuro
            (100, 100, 100)   # Cinza
        ]
        return random.choice(colors)
    
    def draw_obstacle_car(self):
        self.image.fill((0, 0, 0, 0))  
        
        body_width = self.width - 4
        body_height = self.height - 10
        body_rect = pygame.Rect(2, 5, body_width, body_height)
        pygame.draw.rect(self.image, self.color, body_rect, border_radius=8)
        
        if self.car_style == 0:  # Sedan
            dark_color = tuple([max(0, c - 70) for c in self.color])
            roof_width = int(body_width * 0.7)
            roof_height = int(body_height * 0.5)
            roof_x = (self.width - roof_width) // 2
            roof_y = int(body_height * 0.15)
            roof_rect = pygame.Rect(roof_x, roof_y, roof_width, roof_height)
            pygame.draw.rect(self.image, dark_color, roof_rect, border_radius=6)
            
            window_color = (150, 200, 255)
            window_width = int(roof_width * 0.8)
            window_height = int(roof_height * 0.6)
            window_x = (self.width - window_width) // 2
            window_y = roof_y + int(roof_height * 0.2)
            pygame.draw.rect(self.image, window_color, 
                            (window_x, window_y, window_width, window_height),
                            border_radius=3)
        
        elif self.car_style == 1:  # SUV / Van
            dark_color = tuple([max(0, c - 70) for c in self.color])
            roof_width = int(body_width * 0.85)
            roof_height = int(body_height * 0.7)
            roof_x = (self.width - roof_width) // 2
            roof_y = int(body_height * 0.1)
            roof_rect = pygame.Rect(roof_x, roof_y, roof_width, roof_height)
            pygame.draw.rect(self.image, dark_color, roof_rect, border_radius=6)
            
            window_color = (150, 200, 255)
            window_width = int(roof_width * 0.3)
            window_height = int(roof_height * 0.5)
            
            front_window_x = roof_x + 2
            window_y = roof_y + int(roof_height * 0.15)
            pygame.draw.rect(self.image, window_color, 
                            (front_window_x, window_y, window_width, window_height),
                            border_radius=2)
            
            back_window_x = roof_x + roof_width - window_width - 2
            pygame.draw.rect(self.image, window_color, 
                            (back_window_x, window_y, window_width, window_height),
                            border_radius=2)
        
        else:  # Esportivo
            dark_color = tuple([max(0, c - 70) for c in self.color])
            roof_width = int(body_width * 0.6)
            roof_height = int(body_height * 0.35)
            roof_x = (self.width - roof_width) // 2
            roof_y = int(body_height * 0.2)
            roof_rect = pygame.Rect(roof_x, roof_y, roof_width, roof_height)
            pygame.draw.rect(self.image, dark_color, roof_rect, border_radius=8)
            
            window_color = (150, 200, 255)
            window_width = int(roof_width * 0.85)
            window_height = int(roof_height * 0.7)
            window_x = (self.width - window_width) // 2
            window_y = roof_y + int(roof_height * 0.15)
            pygame.draw.rect(self.image, window_color, 
                            (window_x, window_y, window_width, window_height),
                            border_radius=4)
            
            spoiler_height = 5
            spoiler_width = int(body_width * 0.7)
            spoiler_x = (self.width - spoiler_width) // 2
            spoiler_y = body_height
            pygame.draw.rect(self.image, dark_color, 
                            (spoiler_x, spoiler_y, spoiler_width, spoiler_height))
        
        
        headlight_color = (255, 255, 100)
        headlight_width = int(body_width * 0.15)
        headlight_height = int(body_height * 0.06)
        left_headlight_x = 4
        right_headlight_x = self.width - headlight_width - 4
        headlight_y = 8
        pygame.draw.rect(self.image, headlight_color, 
                        (left_headlight_x, headlight_y, headlight_width, headlight_height))
        pygame.draw.rect(self.image, headlight_color, 
                        (right_headlight_x, headlight_y, headlight_width, headlight_height))
        
        taillight_color = (150, 0, 0)
        taillight_width = int(body_width * 0.15)
        taillight_height = int(body_height * 0.06)
        left_taillight_x = 4
        right_taillight_x = self.width - taillight_width - 4
        taillight_y = self.height - headlight_height - 8
        pygame.draw.rect(self.image, taillight_color, 
                        (left_taillight_x, taillight_y, taillight_width, taillight_height))
        pygame.draw.rect(self.image, taillight_color, 
                        (right_taillight_x, taillight_y, taillight_width, taillight_height))
        
        wheel_color = BLACK
        wheel_width = int(self.width * 0.18)
        wheel_height = int(self.height * 0.1)
        wheel_offset_x = -2  
        
        pygame.draw.rect(self.image, wheel_color, 
                        (wheel_offset_x, int(self.height * 0.2), 
                        wheel_width, wheel_height), border_radius=3)
        
        pygame.draw.rect(self.image, wheel_color, 
                        (self.width - wheel_width - wheel_offset_x, int(self.height * 0.2), 
                        wheel_width, wheel_height), border_radius=3)
        
        pygame.draw.rect(self.image, wheel_color, 
                        (wheel_offset_x, int(self.height * 0.7), 
                        wheel_width, wheel_height), border_radius=3)
        
        pygame.draw.rect(self.image, wheel_color, 
                        (self.width - wheel_width - wheel_offset_x, int(self.height * 0.7), 
                        wheel_width, wheel_height), border_radius=3)
    
    def update(self, speed):
        self.y += speed
    
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
    
    def get_rect(self):
        collision_margin = 5
        return pygame.Rect(
            self.x + collision_margin, 
            self.y + collision_margin, 
            self.width - (2 * collision_margin), 
            self.height - (2 * collision_margin)
        )