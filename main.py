import pygame
import sys
import random

from config import *
from entities import Car, Obstacle
from environment import *
from visual_effects import *
from game_mechanics import generate_obstacles

def main():
    car = Car()
    obstacles = []
    particles = []
    clouds = [] 
    
    for _ in range(3):
        clouds.append(Cloud())
    
    game_over = False
    score = 0
    
    start_time = pygame.time.get_ticks()
    day_cycle_start = start_time  
    last_obstacle_time = start_time
    obstacle_frequency = 2000  
    
    sky_color = SKY_COLORS[0]
    cloud_color = CLOUD_COLORS[0]
    
    special_effects = {
        "speed_multiplier": 1.0,
        "score_multiplier": 1.0,
        "special_mode": False
    }
    
    while not game_over:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    car.move_left()
                if event.key == pygame.K_RIGHT:
                    car.move_right()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            car.accelerate()
        if keys[pygame.K_DOWN]:
            car.brake()
        
        special_effects = apply_special_effects_recursive(car, obstacles, score)
        
        sky_color, cloud_color, clouds = update_sky_recursive(current_time, day_cycle_start, clouds)
        
        for cloud in clouds:
            cloud.update(car.speed)
        
        last_obstacle_time, obstacle_frequency = generate_obstacles(
            obstacles, elapsed_time, last_obstacle_time, obstacle_frequency
        )
        
        car.update()
        
        road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
        particles = update_particles_recursive(particles, car.speed, road_left, ROAD_WIDTH)
        
        for obstacle in obstacles[:]:
            obstacle.update(car.speed * special_effects["speed_multiplier"])
            
            if car.get_rect().colliderect(obstacle.get_rect()):
                game_over = True
            
            if not obstacle.passed and obstacle.y > car.y + car.height:
                obstacle.passed = True
                score += int(SCORE_INCREMENT * special_effects["score_multiplier"])
            
            if obstacle.y > SCREEN_HEIGHT:
                obstacles.remove(obstacle)
        
        draw_sky(screen, sky_color, cloud_color, clouds)
        
        draw_road(screen)
        
        draw_particles(screen, particles)
        
        car.draw(screen)
        
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        draw_score(screen, score)
        draw_speed(screen, car.speed)
        
        if special_effects["special_mode"]:
            font = pygame.font.SysFont(None, 28)
            text = font.render("MODO TURBO!", True, (255, 0, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 20))
        
        pygame.display.flip()
        clock.tick(60)
    
    show_game_over(screen, score)
    main()  

if __name__ == "__main__":
    main()