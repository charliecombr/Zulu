import pygame
from config import *
from environment import *

def draw_particles(surface, particles):
    for particle in particles:
        particle.draw(surface)

def draw_sky(surface, sky_color, cloud_color, clouds):
    # Desenhar fundo do céu
    surface.fill(sky_color)
    
    # Desenhar todas as nuvens
    for cloud in clouds:
        cloud.draw(surface, cloud_color)

def draw_road(surface):
    road_left = (SCREEN_WIDTH - ROAD_WIDTH) // 2
    
    # Desenhar estrada
    pygame.draw.rect(surface, GRAY, (road_left, 0, ROAD_WIDTH, SCREEN_HEIGHT))
    
    # Desenhar linhas das faixas
    for i in range(1, 3):
        x = road_left + i * LANE_WIDTH
        pygame.draw.line(surface, WHITE, (x, 0), (x, SCREEN_HEIGHT), 3)
    
    # Desenhar bordas da estrada
    pygame.draw.line(surface, WHITE, (road_left, 0), (road_left, SCREEN_HEIGHT), 5)
    pygame.draw.line(surface, WHITE, (road_left + ROAD_WIDTH, 0), (road_left + ROAD_WIDTH, SCREEN_HEIGHT), 5)

def draw_score(surface, score):
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(text, (20, 20))

def draw_speed(surface, speed):
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Speed: {int(speed*2)} km/h", True, WHITE)
    surface.blit(text, (SCREEN_WIDTH - 180, 20))

def show_game_over(surface, score):
    surface.fill(BLACK)
    font = pygame.font.SysFont(None, 64)
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    
    surface.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                                 SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2 - 50))
    surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 
                             SCREEN_HEIGHT // 2 - score_text.get_height() // 2 + 50))
    
    restart_font = pygame.font.SysFont(None, 36)
    restart_text = restart_font.render("Pressione R para reiniciar", True, GREEN)
    surface.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                               SCREEN_HEIGHT // 2 + 120))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()