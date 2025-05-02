import pygame
import random
from config import *

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 6)
        self.color = (255, 255, 255, random.randint(30, 100))  
        self.speed = random.uniform(1, 3)
        self.lifetime = random.randint(20, 60)  
    
    def update(self, car_speed):
        self.y += car_speed * self.speed / 3
        self.lifetime -= 1
    
    def draw(self, surface):
        if self.lifetime > 0:
            s = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.circle(s, self.color, (self.size // 2, self.size // 2), self.size // 2)
            surface.blit(s, (int(self.x), int(self.y)))

class Cloud:
    def __init__(self):
        self.width = random.randint(100, 200)
        self.height = random.randint(30, 60)
        self.x = random.randint(-100, SCREEN_WIDTH + 100)
        self.y = random.randint(20, 150)
        self.speed = random.uniform(0.1, 0.5)
        
    def update(self, car_speed):
        self.x -= (self.speed * car_speed / 2)
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(0, 100)
            self.y = random.randint(20, 150)
    
    def draw(self, surface, color):
        cloud_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        elipse_positions = [
            (self.width // 4, self.height // 2, self.width // 2, self.height),
            (self.width // 2, self.height // 3, self.width // 3, self.height // 2),
            (3 * self.width // 4, self.height // 2, self.width // 2, self.height),
            (self.width // 2, self.height // 2, self.width // 2, self.height // 2)
        ]
        for pos in elipse_positions:
            alpha_color = color + (200,)  # Adicionar transparência
            pygame.draw.ellipse(cloud_surface, alpha_color, pygame.Rect(pos))
        
        surface.blit(cloud_surface, (self.x, self.y))

def update_particles_recursive(particles, car_speed, road_left, road_width):
    particles = [p for p in particles if p.lifetime > 0]
    
    if len(particles) < MAX_PARTICLES and random.random() < 0.3:  
        x_options = [
            road_left,  
            road_left + road_width,  
            road_left + road_width // 3, 
            road_left + 2 * road_width // 3  
        ]
        x = random.choice(x_options) + random.randint(-5, 5)  
        y = random.randint(0, SCREEN_HEIGHT // 2)  
        
        particles.append(Particle(x, y))
    
    for particle in particles:
        particle.update(car_speed)
    
    return particles

def update_sky_recursive(current_time, start_time, clouds):
    cycle_progress = ((current_time - start_time) % DAY_CYCLE_DURATION) / DAY_CYCLE_DURATION
    
    color_count = len(SKY_COLORS)
    current_index = int(cycle_progress * color_count)
    next_index = (current_index + 1) % color_count
    
    color_progress = (cycle_progress * color_count) - current_index
    
    current_sky = SKY_COLORS[current_index]
    next_sky = SKY_COLORS[next_index]
    sky_color = (
        int(current_sky[0] + (next_sky[0] - current_sky[0]) * color_progress),
        int(current_sky[1] + (next_sky[1] - current_sky[1]) * color_progress),
        int(current_sky[2] + (next_sky[2] - current_sky[2]) * color_progress)
    )
    
    current_cloud = CLOUD_COLORS[current_index]
    next_cloud = CLOUD_COLORS[next_index]
    cloud_color = (
        int(current_cloud[0] + (next_cloud[0] - current_cloud[0]) * color_progress),
        int(current_cloud[1] + (next_cloud[1] - current_cloud[1]) * color_progress),
        int(current_cloud[2] + (next_cloud[2] - current_cloud[2]) * color_progress)
    )
    
    if len(clouds) < MAX_CLOUDS and random.random() < 0.01:
        clouds.append(Cloud())
    
    return sky_color, cloud_color, clouds

def apply_special_effects_recursive(car, obstacles, score, depth=0, max_depth=3):
    
    if depth >= max_depth:
        return {
            "speed_multiplier": 1.0,
            "score_multiplier": 1.0,
            "special_mode": False
        }
    
    effects = {
        "speed_multiplier": 1.0,
        "score_multiplier": 1.0,
        "special_mode": False
    }
    
    if score > 100:
        effects["speed_multiplier"] = 1.1
        effects["score_multiplier"] = 1.5
    
    if score > 250:
        effects["speed_multiplier"] = 1.2
        effects["score_multiplier"] = 2.0
    
    if score > 500:
        effects["speed_multiplier"] = 1.3
        effects["score_multiplier"] = 2.5
        effects["special_mode"] = True
    
    next_effects = apply_special_effects_recursive(car, obstacles, score, depth + 1, max_depth)
    
    combined_effects = {
        "speed_multiplier": (effects["speed_multiplier"] + next_effects["speed_multiplier"]) / 2,
        "score_multiplier": max(effects["score_multiplier"], next_effects["score_multiplier"]),
        "special_mode": effects["special_mode"] or next_effects["special_mode"]
    }
    
    return combined_effects